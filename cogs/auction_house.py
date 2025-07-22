import discord
from discord.ext import commands
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from replit import db
import random

from config import COLORS, is_module_enabled
from utils.helpers import create_embed, format_number
from rpg_data.game_data import ITEMS, RARITY_COLORS
import logging

logger = logging.getLogger(__name__)

class AuctionHouse(commands.Cog):
    """Player-driven auction house system for rare items and player economy."""

    def __init__(self, bot):
        self.bot = bot
        self.active_auctions = {}
        self.auction_history = {}

    async def cog_load(self):
        """Initialize auction data from database."""
        try:
            # Load active auctions
            if "active_auctions" in db:
                self.active_auctions = dict(db["active_auctions"])

            # Load auction history
            if "auction_history" in db:
                self.auction_history = dict(db["auction_history"])

            # Start auction cleanup task
            self.cleanup_task = asyncio.create_task(self.auction_cleanup_loop())
            logger.info("✅ Auction House system initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing auction house: {e}")

    async def auction_cleanup_loop(self):
        """Background task to clean up expired auctions."""
        while True:
            try:
                await self.cleanup_expired_auctions()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in auction cleanup: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error

    async def cleanup_expired_auctions(self):
        """Remove expired auctions and handle winners."""
        current_time = time.time()
        expired_auctions = []

        for auction_id, auction_data in self.active_auctions.items():
            if current_time >= auction_data['end_time']:
                expired_auctions.append(auction_id)

        for auction_id in expired_auctions:
            await self.complete_auction(auction_id)

    async def complete_auction(self, auction_id):
        """Complete an auction and transfer items/gold."""
        if auction_id not in self.active_auctions:
            return

        auction_data = self.active_auctions[auction_id]

        try:
            rpg_core = self.bot.get_cog('RPGCore')
            if not rpg_core:
                return

            # If there are bids, transfer to highest bidder
            if auction_data['bids']:
                winner_bid = max(auction_data['bids'], key=lambda x: x['amount'])
                winner_id = winner_bid['bidder_id']
                winning_amount = winner_bid['amount']

                # Get player data
                winner_data = rpg_core.get_player_data(winner_id)
                seller_data = rpg_core.get_player_data(auction_data['seller_id'])

                if winner_data and seller_data:
                    # Transfer item to winner
                    if auction_data['item_key'] in winner_data.get('inventory', {}):
                        winner_data['inventory'][auction_data['item_key']] += auction_data['quantity']
                    else:
                        winner_data['inventory'][auction_data['item_key']] = auction_data['quantity']

                    # Transfer gold to seller (minus 5% auction house fee)
                    fee = int(winning_amount * 0.05)
                    seller_amount = winning_amount - fee
                    seller_data['gold'] = seller_data.get('gold', 0) + seller_amount

                    # Refund losing bidders
                    for bid in auction_data['bids']:
                        if bid['bidder_id'] != winner_id:
                            bidder_data = rpg_core.get_player_data(bid['bidder_id'])
                            if bidder_data:
                                bidder_data['gold'] = bidder_data.get('gold', 0) + bid['amount']
                                rpg_core.save_player_data(bid['bidder_id'], bidder_data)

                    # Save winner and seller data
                    rpg_core.save_player_data(winner_id, winner_data)
                    rpg_core.save_player_data(auction_data['seller_id'], seller_data)

                    # Record in history
                    self.auction_history[auction_id] = {
                        **auction_data,
                        'winner_id': winner_id,
                        'final_price': winning_amount,
                        'completed_at': time.time()
                    }

            else:
                # No bids, return item to seller
                seller_data = rpg_core.get_player_data(auction_data['seller_id'])
                if seller_data:
                    if auction_data['item_key'] in seller_data.get('inventory', {}):
                        seller_data['inventory'][auction_data['item_key']] += auction_data['quantity']
                    else:
                        seller_data['inventory'][auction_data['item_key']] = auction_data['quantity']
                    rpg_core.save_player_data(auction_data['seller_id'], seller_data)

            # Remove from active auctions
            del self.active_auctions[auction_id]

            # Save to database
            db["active_auctions"] = self.active_auctions
            db["auction_history"] = self.auction_history

        except Exception as e:
            logger.error(f"Error completing auction {auction_id}: {e}")

    @commands.command(name="auction", aliases=["ah", "auctionhouse", "auctions", "market"])
    async def auction_house_main(self, ctx):
        """Open the main auction house interface."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        rpg_core = self.bot.get_cog('RPGCore')
        if not rpg_core:
            await ctx.send("❌ RPG system not loaded.")
            return

        player_data = rpg_core.get_player_data(str(ctx.author.id))
        if not player_data:
            await ctx.send("❌ Create a character first with `$startrpg`!")
            return

        view = AuctionMainView(str(ctx.author.id), self)
        embed = view.create_main_embed()
        await ctx.send(embed=embed, view=view)

    @commands.command(name="sell", aliases=["list", "sellitem"])
    async def sell_item(self, ctx, item_name: str, quantity: int = 1, starting_bid: int = 100, duration: int = 24):
        """Sell an item on the auction house."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        if quantity < 1 or starting_bid < 1 or duration < 1 or duration > 168:
            await ctx.send("❌ Invalid parameters! Quantity ≥ 1, Starting bid ≥ 1, Duration 1-168 hours")
            return

        rpg_core = self.bot.get_cog('RPGCore')
        if not rpg_core:
            await ctx.send("❌ RPG system not loaded.")
            return

        player_data = rpg_core.get_player_data(str(ctx.author.id))
        if not player_data:
            await ctx.send("❌ Create a character first with `$startrpg`!")
            return

        # Find item in inventory
        item_key = None
        for key, data in ITEMS.items():
            if key == item_name.lower().replace(" ", "_") or data['name'].lower() == item_name.lower():
                item_key = key
                break

        if not item_key:
            await ctx.send(f"❌ Item '{item_name}' not found!")
            return

        inventory = player_data.get('inventory', {})
        if item_key not in inventory or inventory[item_key] < quantity:
            await ctx.send(f"❌ You don't have {quantity} {ITEMS[item_key]['name']}!")
            return

        # Create auction
        auction_id = f"{ctx.author.id}_{int(time.time())}"
        end_time = time.time() + (duration * 3600)

        auction_data = {
            'auction_id': auction_id,
            'seller_id': str(ctx.author.id),
            'item_key': item_key,
            'quantity': quantity,
            'starting_bid': starting_bid,
            'current_bid': 0,
            'bids': [],
            'start_time': time.time(),
            'end_time': end_time,
            'duration_hours': duration
        }

        # Remove item from inventory
        inventory[item_key] -= quantity
        if inventory[item_key] <= 0:
            del inventory[item_key]
        player_data['inventory'] = inventory
        rpg_core.save_player_data(str(ctx.author.id), player_data)

        # Add to active auctions
        self.active_auctions[auction_id] = auction_data
        db["active_auctions"] = self.active_auctions

        item_data = ITEMS[item_key]
        embed = discord.Embed(
            title="🏛️ Auction Created!",
            description=f"**{item_data['name']}** x{quantity} is now up for auction!",
            color=RARITY_COLORS.get(item_data['rarity'], COLORS['primary'])
        )

        embed.add_field(
            name="📊 Auction Details",
            value=f"**Starting Bid:** {format_number(starting_bid)} 💰\n"
                  f"**Duration:** {duration} hours\n"
                  f"**Ends:** <t:{int(end_time)}:R>",
            inline=True
        )

        await ctx.send(embed=embed)

    @commands.command(name="bid", aliases=["placebid", "offer"])
    async def place_bid(self, ctx, auction_id: str, amount: int):
        """Place a bid on an auction."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        if amount < 1:
            await ctx.send("❌ Bid amount must be at least 1 gold!")
            return

        rpg_core = self.bot.get_cog('RPGCore')
        if not rpg_core:
            await ctx.send("❌ RPG system not loaded.")
            return

        player_data = rpg_core.get_player_data(str(ctx.author.id))
        if not player_data:
            await ctx.send("❌ Create a character first with `$startrpg`!")
            return

        if auction_id not in self.active_auctions:
            await ctx.send("❌ Auction not found or expired!")
            return

        auction_data = self.active_auctions[auction_id]

        # Check if auction is still active
        if time.time() >= auction_data['end_time']:
            await ctx.send("❌ This auction has expired!")
            return

        # Check if bidding on own auction
        if auction_data['seller_id'] == str(ctx.author.id):
            await ctx.send("❌ You cannot bid on your own auction!")
            return

        # Check minimum bid
        minimum_bid = max(auction_data['starting_bid'], auction_data['current_bid'] + 1)
        if amount < minimum_bid:
            await ctx.send(f"❌ Minimum bid is {format_number(minimum_bid)} 💰!")
            return

        # Check if player has enough gold
        current_gold = player_data.get('gold', 0)
        if current_gold < amount:
            await ctx.send(f"❌ You need {format_number(amount)} 💰 but only have {format_number(current_gold)} 💰!")
            return

        # Refund previous bid from this player
        previous_bid = None
        for bid in auction_data['bids']:
            if bid['bidder_id'] == str(ctx.author.id):
                previous_bid = bid
                break

        if previous_bid:
            player_data['gold'] += previous_bid['amount']
            auction_data['bids'].remove(previous_bid)

        # Deduct gold for new bid
        player_data['gold'] -= amount

        # Add new bid
        new_bid = {
            'bidder_id': str(ctx.author.id),
            'amount': amount,
            'timestamp': time.time()
        }
        auction_data['bids'].append(new_bid)
        auction_data['current_bid'] = amount

        # Save data
        rpg_core.save_player_data(str(ctx.author.id), player_data)
        self.active_auctions[auction_id] = auction_data
        db["active_auctions"] = self.active_auctions

        item_data = ITEMS[auction_data['item_key']]
        embed = discord.Embed(
            title="✅ Bid Placed!",
            description=f"You bid **{format_number(amount)} 💰** on **{item_data['name']}** x{auction_data['quantity']}",
            color=COLORS['success']
        )

        time_left = auction_data['end_time'] - time.time()
        embed.add_field(
            name="⏰ Time Remaining",
            value=f"<t:{int(auction_data['end_time'])}:R>",
            inline=True
        )

        await ctx.send(embed=embed)

class AuctionMainView(discord.ui.View):
    """Main auction house interface."""

    def __init__(self, user_id: str, auction_house):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.auction_house = auction_house
        self.current_page = 0
        self.items_per_page = 8
        self.current_filter = "all"

    def create_main_embed(self):
        """Create the main auction house embed."""
        embed = discord.Embed(
            title="🏛️ Plagg's Chaotic Auction House",
            description="*\"Welcome to the most disorganized marketplace in Paris! People are selling their junk here instead of buying cheese. Typical.\"*\n\n"
                       "Browse, bid, and sell rare items with other players!",
            color=COLORS['gold']
        )

        active_count = len(self.auction_house.active_auctions)
        embed.add_field(
            name="📊 Market Status",
            value=f"**Active Auctions:** {active_count}\n"
                  f"**Total Bids Today:** {self.get_daily_bid_count()}\n"
                  f"**Market Activity:** {'🔥 Hot' if active_count > 10 else '📈 Growing' if active_count > 5 else '🌱 New'}",
            inline=True
        )

        embed.add_field(
            name="💡 Quick Tips",
            value="• Use filters to find specific items\n"
                  "• Bid early to secure good deals\n"
                  "• Check auction end times\n"
                  "• 5% fee on successful sales",
            inline=True
        )

        embed.set_footer(text="💰 Use the buttons below to navigate • 🧀 Still no cheese market...")
        return embed

    def get_daily_bid_count(self):
        """Get number of bids placed today."""
        current_time = time.time()
        day_start = current_time - (current_time % 86400)

        bid_count = 0
        for auction_data in self.auction_house.active_auctions.values():
            for bid in auction_data['bids']:
                if bid['timestamp'] >= day_start:
                    bid_count += 1
        return bid_count

    @discord.ui.button(label="🔍 Browse Auctions", style=discord.ButtonStyle.primary, emoji="🔍")
    async def browse_auctions(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your auction house!", ephemeral=True)
            return

        view = AuctionBrowseView(self.user_id, self.auction_house)
        embed = view.create_browse_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="💰 Sell Item", style=discord.ButtonStyle.success, emoji="💰")
    async def sell_item(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your auction house!", ephemeral=True)
            return

        view = SellItemView(self.user_id, self.auction_house)
        embed = view.create_sell_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="📈 My Auctions", style=discord.ButtonStyle.secondary, emoji="📈")
    async def my_auctions(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your auction house!", ephemeral=True)
            return

        view = MyAuctionsView(self.user_id, self.auction_house)
        embed = view.create_my_auctions_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class AuctionBrowseView(discord.ui.View):
    """Browse active auctions interface."""

    def __init__(self, user_id: str, auction_house):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.auction_house = auction_house
        self.current_page = 0
        self.items_per_page = 5
        self.current_filter = "all"

    def create_browse_embed(self):
        """Create the browse auctions embed."""
        filtered_auctions = self.get_filtered_auctions()

        embed = discord.Embed(
            title="🔍 Browse Active Auctions",
            description=f"*\"Look at all this junk people are selling! None of it's cheese, obviously.\"*\n\n"
                       f"**Filter:** {self.current_filter.title()} | **Total:** {len(filtered_auctions)}",
            color=COLORS['info']
        )

        # Paginate auctions
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_auctions = list(filtered_auctions.items())[start_idx:end_idx]

        if not page_auctions:
            embed.add_field(
                name="📭 No Auctions",
                value="No active auctions match your filter.",
                inline=False
            )
        else:
            for auction_id, auction_data in page_auctions:
                item_data = ITEMS.get(auction_data['item_key'], {})
                item_name = item_data.get('name', auction_data['item_key'])

                time_left = auction_data['end_time'] - time.time()
                if time_left > 0:
                    hours_left = int(time_left // 3600)
                    minutes_left = int((time_left % 3600) // 60)
                    time_str = f"{hours_left}h {minutes_left}m"
                else:
                    time_str = "Expired"

                current_bid = auction_data['current_bid'] if auction_data['current_bid'] > 0 else auction_data['starting_bid']
                bid_count = len(auction_data['bids'])

                rarity_emoji = self.get_rarity_emoji(item_data.get('rarity', 'common'))

                embed.add_field(
                    name=f"{rarity_emoji} {item_name} x{auction_data['quantity']}",
                    value=f"💰 **{format_number(current_bid)}** gold ({bid_count} bids)\n"
                          f"⏰ {time_str} left\n"
                          f"🆔 `{auction_id[-8:]}`",
                    inline=True
                )

        total_pages = max(1, (len(filtered_auctions) + self.items_per_page - 1) // self.items_per_page)
        embed.set_footer(text=f"Page {self.current_page + 1}/{total_pages} • Use buttons to navigate")

        return embed

    def get_filtered_auctions(self):
        """Get auctions filtered by current filter."""
        filtered = {}
        current_time = time.time()

        for auction_id, auction_data in self.auction_house.active_auctions.items():
            if auction_data['end_time'] <= current_time:
                continue

            if self.current_filter == "all":
                filtered[auction_id] = auction_data
            else:
                item_data = ITEMS.get(auction_data['item_key'], {})
                if item_data.get('rarity', 'common') == self.current_filter:
                    filtered[auction_id] = auction_data

        return filtered

    def get_rarity_emoji(self, rarity):
        """Get emoji for rarity."""
        rarity_emojis = {
            'common': '⚪',
            'uncommon': '🟢',
            'rare': '🔵',
            'epic': '🟣',
            'legendary': '🟠',
            'mythical': '🔴',
            'divine': '⭐',
            'cosmic': '🌟'
        }
        return rarity_emojis.get(rarity, '⚪')

    @discord.ui.select(
        placeholder="🎯 Filter by rarity...",
        options=[
            discord.SelectOption(label="All Items", value="all", emoji="🔍"),
            discord.SelectOption(label="Common", value="common", emoji="⚪"),
            discord.SelectOption(label="Uncommon", value="uncommon", emoji="🟢"),
            discord.SelectOption(label="Rare", value="rare", emoji="🔵"),
            discord.SelectOption(label="Epic", value="epic", emoji="🟣"),
            discord.SelectOption(label="Legendary", value="legendary", emoji="🟠"),
        ]
    )
    async def filter_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your filter!", ephemeral=True)
            return

        self.current_filter = select.values[0]
        self.current_page = 0
        embed = self.create_browse_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="⬅️ Previous", style=discord.ButtonStyle.secondary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your navigation!", ephemeral=True)
            return

        if self.current_page > 0:
            self.current_page -= 1
            embed = self.create_browse_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="➡️ Next", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your navigation!", ephemeral=True)
            return

        filtered_auctions = self.get_filtered_auctions()
        max_pages = max(1, (len(filtered_auctions) + self.items_per_page - 1) // self.items_per_page)

        if self.current_page < max_pages - 1:
            self.current_page += 1
            embed = self.create_browse_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="🔙 Back to Main", style=discord.ButtonStyle.danger)
    async def back_to_main(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your auction house!", ephemeral=True)
            return

        view = AuctionMainView(self.user_id, self.auction_house)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class SellItemView(discord.ui.View):
    """Sell item on auction interface."""

    def __init__(self, user_id: str, auction_house):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.auction_house = auction_house
        self.selected_item = None
        self.quantity = 1
        self.starting_bid = 100
        self.duration = 24

    def create_sell_embed(self):
        """Create the sell item embed."""
        embed = discord.Embed(
            title="💰 Sell Item at Auction",
            description="*\"Selling your junk to buy more junk? The cycle continues. At least make some gold from it.\"*",
            color=COLORS['warning']
        )

        if self.selected_item:
            item_data = ITEMS.get(self.selected_item, {})
            rarity_emoji = self.get_rarity_emoji(item_data.get('rarity', 'common'))

            embed.add_field(
                name="📦 Selected Item",
                value=f"{rarity_emoji} **{item_data.get('name', self.selected_item)}**\n"
                      f"Quantity: **{self.quantity}**\n"
                      f"Starting Bid: **{format_number(self.starting_bid)} 💰**\n"
                      f"Duration: **{self.duration} hours**",
                inline=True
            )

            # Calculate fees
            estimated_fee = int(self.starting_bid * 0.05)
            embed.add_field(
                name="💳 Fees & Info",
                value=f"**Auction House Fee:** 5%\n"
                      f"**Est. Fee:** {format_number(estimated_fee)} 💰\n"
                      f"**Your Cut:** 95% of final bid",
                inline=True
            )
        else:
            embed.add_field(
                name="📋 Instructions",
                value="1. Select an item from your inventory\n"
                      "2. Set quantity and starting bid\n"
                      "3. Choose auction duration\n"
                      "4. Confirm to list",
                inline=False
            )

        return embed

    def get_rarity_emoji(self, rarity):
        """Get emoji for rarity."""
        rarity_emojis = {
            'common': '⚪',
            'uncommon': '🟢',
            'rare': '🔵',
            'epic': '🟣',
            'legendary': '🟠',
            'mythical': '🔴',
            'divine': '⭐',
            'cosmic': '🌟'
        }
        return rarity_emojis.get(rarity, '⚪')

class MyAuctionsView(discord.ui.View):
    """View player's auctions and bids."""

    def __init__(self, user_id: str, auction_house):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.auction_house = auction_house
        self.view_mode = "selling"  # "selling" or "bidding"

    def create_my_auctions_embed(self):
        """Create the my auctions embed."""
        embed = discord.Embed(
            title="📈 My Auction Activity",
            description=f"*\"Here's all your marketplace drama. Buying and selling junk like a proper hoarder.\"*",
            color=COLORS['info']
        )

        if self.view_mode == "selling":
            my_auctions = self.get_my_selling_auctions()

            if not my_auctions:
                embed.add_field(
                    name="📭 No Active Sales",
                    value="You're not currently selling anything.\nUse the **Sell Item** button to list items!",
                    inline=False
                )
            else:
                for auction_id, auction_data in my_auctions.items():
                    item_data = ITEMS.get(auction_data['item_key'], {})
                    item_name = item_data.get('name', auction_data['item_key'])

                    time_left = auction_data['end_time'] - time.time()
                    hours_left = max(0, int(time_left // 3600))

                    current_bid = auction_data['current_bid'] if auction_data['current_bid'] > 0 else auction_data['starting_bid']
                    bid_count = len(auction_data['bids'])

                    status = "🔥 Active" if bid_count > 0 else "⏳ Waiting"

                    embed.add_field(
                        name=f"📦 {item_name} x{auction_data['quantity']}",
                        value=f"💰 **{format_number(current_bid)}** gold ({bid_count} bids)\n"
                              f"⏰ {hours_left}h left | {status}\n"
                              f"🆔 `{auction_id[-8:]}`",
                        inline=True
                    )
        else:
            my_bids = self.get_my_bidding_auctions()

            if not my_bids:
                embed.add_field(
                    name="📭 No Active Bids",
                    value="You haven't placed any bids yet.\nBrowse auctions to start bidding!",
                    inline=False
                )
            else:
                for auction_id, (auction_data, my_bid) in my_bids.items():
                    item_data = ITEMS.get(auction_data['item_key'], {})
                    item_name = item_data.get('name', auction_data['item_key'])

                    time_left = auction_data['end_time'] - time.time()
                    hours_left = max(0, int(time_left // 3600))

                    is_winning = my_bid['amount'] == auction_data['current_bid']
                    status = "🏆 Winning" if is_winning else "📉 Outbid"

                    embed.add_field(
                        name=f"🎯 {item_name} x{auction_data['quantity']}",
                        value=f"🏷️ My Bid: **{format_number(my_bid['amount'])}** 💰\n"
                              f"💰 Current: **{format_number(auction_data['current_bid'])}** 💰\n"
                              f"⏰ {hours_left}h left | {status}",
                        inline=True
                    )

        return embed

    def get_my_selling_auctions(self):
        """Get auctions where user is the seller."""
        my_auctions = {}
        current_time = time.time()

        for auction_id, auction_data in self.auction_house.active_auctions.items():
            if auction_data['seller_id'] == self.user_id and auction_data['end_time'] > current_time:
                my_auctions[auction_id] = auction_data

        return my_auctions

    def get_my_bidding_auctions(self):
        """Get auctions where user has placed bids."""
        my_bids = {}
        current_time = time.time()

        for auction_id, auction_data in self.auction_house.active_auctions.items():
            if auction_data['end_time'] > current_time:
                for bid in auction_data['bids']:
                    if bid['bidder_id'] == self.user_id:
                        my_bids[auction_id] = (auction_data, bid)
                        break

        return my_bids

    @discord.ui.button(label="💰 My Sales", style=discord.ButtonStyle.primary)
    async def view_selling(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your auctions!", ephemeral=True)
            return

        self.view_mode = "selling"
        embed = self.create_my_auctions_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🎯 My Bids", style=discord.ButtonStyle.secondary)
    async def view_bidding(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your bids!", ephemeral=True)
            return

        self.view_mode = "bidding"
        embed = self.create_my_auctions_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🔙 Back to Main", style=discord.ButtonStyle.danger)
    async def back_to_main(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your auction house!", ephemeral=True)
            return

        view = AuctionMainView(self.user_id, self.auction_house)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(AuctionHouse(bot))