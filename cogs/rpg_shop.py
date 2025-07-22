import discord
from discord.ext import commands
import math
from utils.helpers import create_embed, format_number
from config import COLORS, is_module_enabled
from rpg_data.game_data import ITEMS, RARITY_COLORS
import logging

logger = logging.getLogger(__name__)

class ShopMainView(discord.ui.View):
    """Main shop interface with category buttons and enhanced features."""

    def __init__(self, user_id: str, rpg_core):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.rpg_core = rpg_core
        self.shopping_cart = {}  # item_key: {"quantity": int, "price": int, "name": str}

    @discord.ui.button(label="⚔️ Weapons", style=discord.ButtonStyle.primary, emoji="⚔️", row=0)
    async def weapons_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        view = ShopCategoryView(self.user_id, "weapon", self.rpg_core)
        embed = view.create_category_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🛡️ Armor", style=discord.ButtonStyle.primary, emoji="🛡️", row=0)
    async def armor_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        view = ShopCategoryView(self.user_id, "armor", self.rpg_core)
        embed = view.create_category_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🧪 Consumables", style=discord.ButtonStyle.primary, emoji="🧪", row=0)
    async def consumables_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        view = ShopCategoryView(self.user_id, "consumable", self.rpg_core)
        embed = view.create_category_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="💎 Accessories", style=discord.ButtonStyle.primary, emoji="💎", row=0)
    async def accessories_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        view = ShopCategoryView(self.user_id, "accessory", self.rpg_core)
        embed = view.create_category_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="✨ Artifacts", style=discord.ButtonStyle.primary, emoji="✨", row=1)
    async def artifacts_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        view = ShopCategoryView(self.user_id, "artifact", self.rpg_core)
        embed = view.create_category_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="💰 My Gold", style=discord.ButtonStyle.secondary, emoji="💰", row=1)
    async def check_gold(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        player_data = self.rpg_core.get_player_data(self.user_id)
        if not player_data:
            await interaction.response.send_message("❌ Character not found!", ephemeral=True)
            return

        cart_total = sum(cart_item['quantity'] * cart_item['price'] for cart_item in self.shopping_cart.values())

        embed = discord.Embed(
            title="💰 Your Wealth",
            description=f"**Current Gold:** `{format_number(player_data['gold'])}` 💰\n\n"
                       f"📊 **Inventory Stats:**\n"
                       f"• Total Items: `{sum(player_data.get('inventory', {}).values())}`\n"
                       f"• Unique Items: `{len(player_data.get('inventory', {}))}`\n"
                       f"• Estimated Worth: `{format_number(int(player_data['gold'] * 1.3))}` 💰\n\n"
                       f"🛒 **Cart Status:**\n"
                       f"• Items in Cart: `{sum(item['quantity'] for item in self.shopping_cart.values())}`\n"
                       f"• Cart Total: `{format_number(cart_total)}` 💰\n"
                       f"• After Purchase: `{format_number(player_data['gold'] - cart_total)}` 💰",
            color=COLORS['gold']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="🛒 View Cart", style=discord.ButtonStyle.primary, emoji="🛒", row=2)
    async def view_cart(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        if not self.shopping_cart:
            await interaction.response.send_message(
                "*\"Your cart is as empty as my enthusiasm for non-cheese items. Go add some junk to it.\"*",
                ephemeral=True
            )
            return

        view = ShoppingCartView(self.user_id, self.rpg_core, self.shopping_cart)
        embed = view.create_cart_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🏛️ Auction House", style=discord.ButtonStyle.success, emoji="🏛️", row=2)
    async def auction_house(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        await interaction.response.send_message(
            "*\"Welcome to the place where people fight over second-hand junk. Maybe you'll find something good, "
            "but I doubt it. It's probably all just as cheese-less as the main shop.\"*\n\n"
            "🚧 **Auction House coming soon!** 🚧\n"
            "Players will be able to list items and bid on rare finds.",
            ephemeral=True
        )

class ShopCategoryView(discord.ui.View):
    """Category view with item browsing and navigation."""

    def __init__(self, user_id: str, category: str, rpg_core):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.category = category
        self.rpg_core = rpg_core
        self.current_page = 0
        self.items_per_page = 8

        # Filter items by category, excluding admin/owner items and 0-price items
        self.category_items = []
        for item_key, item_data in ITEMS.items():
            if (item_data.get('type') == category and 
                'shop' in item_data.get('sources', []) and
                not item_data.get('owner_only', False) and
                not item_data.get('hidden', False) and
                not item_data.get('achievement_req') and  # Exclude achievement items
                item_data.get('price', 0) > 0):
                self.category_items.append((item_key, item_data))

        # Sort by price and rarity
        rarity_order = {'common': 1, 'uncommon': 2, 'rare': 3, 'epic': 4, 'legendary': 5, 'mythical': 6, 'divine': 7, 'cosmic': 8}
        self.category_items.sort(key=lambda x: (x[1].get('price', 0), rarity_order.get(x[1].get('rarity', 'common'), 1)))

        # Add the item select dropdown
        self.add_item(self.create_item_select())

    def create_category_embed(self):
        """Create the category listing embed."""
        max_pages = math.ceil(len(self.category_items) / self.items_per_page)

        embed = discord.Embed(
            title=f"🛒 {self.category.title()} Shop",
            description=f"Browse and purchase {self.category}s for your adventure!",
            color=COLORS['primary']
        )

        if not self.category_items:
            embed.add_field(
                name="😔 No Items Available",
                value="This category is currently empty. Check back later!",
                inline=False
            )
            return embed

        # Calculate page items
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.category_items))
        page_items = self.category_items[start_idx:end_idx]

        # Create item list
        items_text = ""
        for i, (item_key, item_data) in enumerate(page_items, start=1):
            rarity = item_data.get('rarity', 'common')
            rarity_emoji = {'common': '⚪', 'uncommon': '🟢', 'rare': '🔵', 'epic': '🟣', 'legendary': '🟠', 'mythical': '🔴', 'divine': '⭐', 'cosmic': '🌟'}.get(rarity, '⚪')

            # Format item stats
            stats = []
            if item_data.get('attack'):
                stats.append(f"⚔️{item_data['attack']}")
            if item_data.get('defense'):
                stats.append(f"🛡️{item_data['defense']}")
            if item_data.get('heal_amount'):
                stats.append(f"❤️{item_data['heal_amount']}")

            stats_str = f" `({'/'.join(stats)})`" if stats else ""

            items_text += f"`{start_idx + i}.` {rarity_emoji} **{item_data['name']}**{stats_str}\n"
            items_text += f"     💰 `{format_number(item_data.get('price', 0))}` gold\n"
            items_text += f"     📝 {item_data.get('description', 'No description')[:50]}{'...' if len(item_data.get('description', '')) > 50 else ''}\n\n"

        embed.add_field(
            name=f"📦 Available {self.category.title()}s",
            value=items_text or "No items to display.",
            inline=False
        )

        embed.set_footer(text=f"Page {self.current_page + 1} of {max_pages} | Use dropdown to select items")

        return embed

    def create_item_select(self):
        """Create the item selection dropdown with proper options."""
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.category_items))
        page_items = self.category_items[start_idx:end_idx]

        options = []
        if page_items:
            for i, (item_key, item_data) in enumerate(page_items):
                rarity_emoji = {'common': '⚪', 'uncommon': '🟢', 'rare': '🔵', 'epic': '🟣', 'legendary': '🟠', 'mythical': '🔴'}.get(item_data.get('rarity', 'common'), '⚪')
                options.append(
                    discord.SelectOption(
                        label=item_data['name'][:25],
                        value=item_key,
                        description=f"{format_number(item_data.get('price', 0))} gold",
                        emoji=rarity_emoji
                    )
                )
        else:
            options = [discord.SelectOption(label="No items", value="none", description="No items in this category")]

        select = discord.ui.Select(placeholder="🛍️ Select an item to view details...", options=options, min_values=1, max_values=1)
        select.callback = self.item_select_callback
        return select

    async def item_select_callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        select = interaction.data['values'][0]
        if select != "none":
            item_key = select
            view = ItemDetailsView(self.user_id, item_key, self.rpg_core, self.category)
            embed = view.create_item_embed()
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await interaction.response.send_message("❌ No items available in this category!", ephemeral=True)

    @discord.ui.button(label="◀️ Previous", style=discord.ButtonStyle.secondary, row=2)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        if self.current_page > 0:
            self.current_page -= 1
            embed = self.create_category_embed()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next ▶️", style=discord.ButtonStyle.secondary, row=2)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        max_pages = math.ceil(len(self.category_items) / self.items_per_page)
        if self.current_page < max_pages - 1:
            self.current_page += 1
            embed = self.create_category_embed()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🏠 Main Shop", style=discord.ButtonStyle.success, row=2)
    async def back_to_main(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        player_data = self.rpg_core.get_player_data(self.user_id)
        view = ShopMainView(self.user_id, self.rpg_core)
        embed = self.create_main_shop_embed(player_data)
        await interaction.response.edit_message(embed=embed, view=view)

    def create_main_shop_embed(self, player_data):
        """Create main shop embed."""
        embed = discord.Embed(
            title="🛒 Plagg's Cheese & Combat Shop",
            description="**Welcome to the finest shop in all dimensions!**\n\n"
                       "Here you can find everything from powerful weapons to magical cheese wheels.\n"
                       "Choose a category below to browse available items.\n\n"
                       "💰 **Shop Features:**\n"
                       "• Quality guaranteed by Plagg himself\n"
                       "• Instant delivery to your inventory\n"
                       "• Cheese-powered discounts available\n"
                       "• No returns (destroyed items stay destroyed)",
            color=COLORS['primary']
        )

        embed.add_field(
            name="🏪 Categories",
            value="⚔️ **Weapons** - Swords, bows, staves\n"
                  "🛡️ **Armor** - Protection and shields\n"
                  "🧪 **Consumables** - Potions and elixirs\n"
                  "💎 **Accessories** - Rings and amulets\n"
                  "✨ **Artifacts** - Legendary items",
            inline=True
        )

        if player_data:
            embed.add_field(
                name="💰 Your Funds",
                value=f"**Gold:** `{format_number(player_data['gold'])}`\n"
                      f"**Items:** `{sum(player_data.get('inventory', {}).values())}`",
                inline=True
            )

        embed.set_footer(text="Click a category button to start shopping!")
        return embed

class ItemDetailsView(discord.ui.View):
    """Detailed item view with purchase options."""

    def __init__(self, user_id: str, item_key: str, rpg_core, category: str):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.item_key = item_key
        self.rpg_core = rpg_core
        self.category = category
        self.quantity = 1

    def create_item_embed(self):
        """Create detailed item embed."""
        item_data = ITEMS.get(self.item_key, {})
        player_data = self.rpg_core.get_player_data(self.user_id)

        if not item_data:
            return create_embed("Error", "Item not found!", COLORS['error'])

        rarity = item_data.get('rarity', 'common')
        rarity_color = RARITY_COLORS.get(rarity, COLORS['primary'])
        rarity_emoji = {'common': '⚪', 'uncommon': '🟢', 'rare': '🔵', 'epic': '🟣', 'legendary': '🟠', 'mythical': '🔴', 'divine': '⭐', 'cosmic': '🌟'}.get(rarity, '⚪')

        embed = discord.Embed(
            title=f"{rarity_emoji} {item_data['name']}",
            description=f"**{item_data.get('description', 'A mysterious item with unknown properties.')}**",
            color=rarity_color
        )

        # Item stats
        stats_text = ""
        if item_data.get('attack'):
            stats_text += f"⚔️ **Attack:** `{item_data['attack']}`\n"
        if item_data.get('defense'):
            stats_text += f"🛡️ **Defense:** `{item_data['defense']}`\n"
        if item_data.get('heal_amount'):
            stats_text += f"❤️ **Healing:** `{item_data['heal_amount']} HP`\n"
        if item_data.get('mana_amount'):
            stats_text += f"💙 **Mana:** `{item_data['mana_amount']} MP`\n"

        if stats_text:
            embed.add_field(name="📊 Stats", value=stats_text, inline=True)

        # Item info
        info_text = f"**Type:** `{item_data['type'].title()}`\n"
        info_text += f"**Rarity:** `{rarity.title()}`\n"
        info_text += f"**Price:** `{format_number(item_data.get('price', 0))}` 💰"

        embed.add_field(name="ℹ️ Details", value=info_text, inline=True)

        # Purchase info
        total_cost = item_data.get('price', 0) * self.quantity
        can_afford = player_data['gold'] >= total_cost if player_data else False

        purchase_text = f"**Quantity:** `{self.quantity}`\n"
        purchase_text += f"**Total Cost:** `{format_number(total_cost)}` 💰\n"
        if player_data:
            purchase_text += f"**Your Gold:** `{format_number(player_data['gold'])}` 💰\n"
            if can_afford:
                purchase_text += f"**After Purchase:** `{format_number(player_data['gold'] - total_cost)}` 💰"
            else:
                needed = total_cost - player_data['gold']
                purchase_text += f"❌ **Need:** `{format_number(needed)}` more gold"

        embed.add_field(name="🛒 Purchase", value=purchase_text, inline=False)

        # Special effects
        if item_data.get('effects'):
            effects_text = ""
            for effect in item_data['effects']:
                effects_text += f"• {effect}\n"
            embed.add_field(name="✨ Special Effects", value=effects_text, inline=False)

        return embed

    @discord.ui.select(
        placeholder="📦 Select quantity...",
        options=[
            discord.SelectOption(label="1x", value="1", emoji="1️⃣"),
            discord.SelectOption(label="5x", value="5", emoji="5️⃣"),
            discord.SelectOption(label="10x", value="10", emoji="🔟"),
            discord.SelectOption(label="25x", value="25", emoji="📦"),
            discord.SelectOption(label="50x", value="50", emoji="📦"),
        ]
    )
    async def quantity_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your purchase!", ephemeral=True)
            return

        self.quantity = int(select.values[0])
        embed = self.create_item_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="➕ Add to Cart", style=discord.ButtonStyle.primary, emoji="🛒", row=2)
    async def add_to_cart(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your purchase!", ephemeral=True)
            return

        item_data = ITEMS.get(self.item_key, {})
        total_cost = item_data.get('price', 0) * self.quantity

        main_view = None
        for item in interaction.message.components:
            for child in item.children:
                if isinstance(child, discord.ui.Button) and child.callback.__qualname__.split('.')[0] == 'ShopMainView':
                   main_view = child
                   break
        if main_view is None:
            for child in interaction.message.components:
                if hasattr(child, 'shopping_cart'):
                    main_view = child
                    break

        if self.item_key in main_view.view.shopping_cart:
            main_view.view.shopping_cart[self.item_key]['quantity'] += self.quantity
        else:
            main_view.view.shopping_cart[self.item_key] = {
                'quantity': self.quantity,
                'price': item_data.get('price', 0),
                'name': item_data.get('name', 'Unknown')
            }


        plagg_responses = [
            f"Fine, I tossed {self.quantity}x {item_data.get('name', 'Unknown')} in the cart. This is getting heavy. I'd better get a big tip for this... preferably in cheese.",
            f"Another {item_data.get('name', 'item')} for the pile of junk. The cart's getting fuller, but my enthusiasm remains empty.",
            f"Added to cart. Now you have {self.quantity} more reasons to regret your purchasing decisions. You're welcome.",
            f"Cart updated. That'll be {format_number(total_cost)} gold when you're ready to make poor financial choices."
        ]

        import random
        response = random.choice(plagg_responses)

        await interaction.response.send_message(
            f"🛒 **Added to Cart!**\n\n*\"{response}\"*\n\n"
            f"**Item:** {self.quantity}x {item_data.get('name', 'Unknown')}\n"
            f"**Cost:** {format_number(total_cost)} gold\n\n"
            f"Use the 🛒 **View Cart** button from the main shop to checkout!",
            ephemeral=True
        )

    @discord.ui.button(label="✅ Buy Now", style=discord.ButtonStyle.success, emoji="💰", row=2)
    async def confirm_purchase(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your purchase!", ephemeral=True)
            return

        await interaction.response.defer()

        player_data = self.rpg_core.get_player_data(self.user_id)
        if not player_data:
            embed = create_embed("Error", "Character not found!", COLORS['error'])
            await interaction.followup.edit_message(interaction.message.id, embed=embed, view=None)
            return

        item_data = ITEMS.get(self.item_key, {})
        total_cost = item_data.get('price', 0) * self.quantity

        if player_data['gold'] < total_cost:
            needed = total_cost - player_data['gold']
            embed = create_embed(
                "Insufficient Funds",
                f"*\"Whoa there, big spender! Looks like your wallet is full of lint and sadness. "
                f"Come back when you have {format_number(needed)} more shiny coins.\"*",
                COLORS['error']
            )
            await interaction.followup.edit_message(interaction.message.id, embed=embed, view=None)
            return

        # Anti-exploit: Get fresh player data before purchase
        fresh_player_data = self.rpg_core.get_player_data(self.user_id)
        if not fresh_player_data:
            embed = create_embed("Error", "Failed to load player data!", COLORS['error'])
            await interaction.followup.edit_message(interaction.message.id, embed=embed, view=None)
            return

        # Validate gold again with fresh data
        if fresh_player_data['gold'] < total_cost:
            needed = total_cost - fresh_player_data['gold']
            embed = create_embed(
                "Insufficient Funds",
                f"*\"Whoa there, big spender! Looks like your wallet is full of lint and sadness. "
                f"Come back when you have {format_number(needed)} more shiny coins.\"*",
                COLORS['error']
            )
            await interaction.followup.edit_message(interaction.message.id, embed=embed, view=None)
            return

        # Process purchase with validation
        fresh_player_data['gold'] -= total_cost
        if 'inventory' not in fresh_player_data:
            fresh_player_data['inventory'] = {}

        if self.item_key in fresh_player_data['inventory']:
            fresh_player_data['inventory'][self.item_key] += self.quantity
        else:
            fresh_player_data['inventory'][self.item_key] = self.quantity

        # Validate the purchase was successful
        success = self.rpg_core.save_player_data(self.user_id, fresh_player_data)
        if not success:
            embed = create_embed("Error", "Failed to save purchase data!", COLORS['error'])
            await interaction.followup.edit_message(interaction.message.id, embed=embed, view=None)
            return

        plagg_responses = [
            "Alright, I took your money. The junk is in your bag now. Don't come crying to me if you have buyer's remorse.",
            "Transaction complete. You're now poorer but have more useless items. Congratulations, I guess.",
            "Money exchanged for goods. It's still not cheese, but at least the math worked out.",
            "Purchase successful. Your gold is now mine, and you have some new toys. Fair trade? Debatable."
        ]

        import random
        plagg_response = random.choice(plagg_responses)

        embed = discord.Embed(
            title="✅ Purchase Successful!",
            description=f"*\"{plagg_response}\"*",
            color=COLORS['success']
        )

        embed.add_field(
            name="🛍️ Items Purchased",
            value=f"`{self.quantity}x` **{item_data.get('name', 'Unknown')}**",
            inline=True
        )

        embed.add_field(
            name="💰 Transaction",
            value=f"**Paid:** `{format_number(total_cost)}` gold\n"
                  f"**Remaining:** `{format_number(player_data['gold'])}` gold",
            inline=True
        )

        embed.add_field(
            name="📦 Inventory",
            value=f"You now have `{player_data['inventory'][self.item_key]}x` {item_data.get('name', 'Unknown')}",
            inline=False
        )

        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=None)

    @discord.ui.button(label="🔙 Back", style=discord.ButtonStyle.secondary, emoji="⬅️", row=2)
    async def back_to_category(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your shop!", ephemeral=True)
            return

        view = ShopCategoryView(self.user_id, self.category, self.rpg_core)
        embed = view.create_category_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class ShoppingCartView(discord.ui.View):
    """Shopping cart management interface."""

    def __init__(self, user_id: str, rpg_core, shopping_cart):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.rpg_core = rpg_core
        self.shopping_cart = shopping_cart  # List of (item_key, quantity, total_price) tuples

    def create_cart_embed(self):
        """Create cart display embed."""
        embed = discord.Embed(
            title="🛒 Your Shopping Cart",
            description="*\"Look at all this junk you're buying! I hope you're happy with your non-cheese purchases.\"*",
            color=COLORS['warning']
        )

        if not self.shopping_cart:
            embed.add_field(
                name="📭 Empty Cart",
                value="Your cart is empty. Add some items to get started!",
                inline=False
            )
        else:
            cart_contents = ""
            total_cost = 0
            item_count = 0

            for item_key, cart_item in self.shopping_cart.items():
                quantity = cart_item.get('quantity', 0)
                price_per_item = cart_item.get('price', 0)
                item_name = cart_item.get('name', item_key.replace('_', ' ').title())
                line_total = price_per_item * quantity
                total_cost += line_total
                item_count += quantity

                item_data = ITEMS.get(item_key, {})
                rarity_emoji = {'common': '⚪', 'uncommon': '🟢', 'rare': '🔵', 'epic': '🟣', 'legendary': '🟠', 'mythical': '🔴'}.get(item_data.get('rarity', 'common'), '⚪')
                cart_contents += f"{rarity_emoji} **{item_name}** x{quantity} - {format_number(line_total)} 💰\n"

            embed.add_field(
                name="🛍️ Items in Cart",
                value=cart_contents,
                inline=False
            )

            embed.add_field(
                name="📊 Cart Summary",
                value=f"**Total Items:** {item_count}\n"
                      f"**Unique Types:** {len(self.shopping_cart)}\n"
                      f"**Total Cost:** {format_number(total_cost)} 💰",
                inline=True
            )

            # Get player gold for comparison
            player_data = self.rpg_core.get_player_data(self.user_id)
            player_gold = player_data.get('gold', 0) if player_data else 0

            if total_cost > player_gold:
                embed.add_field(
                    name="⚠️ Insufficient Funds",
                    value=f"You need **{format_number(total_cost - player_gold)}** more gold!",
                    inline=True
                )
            else:
                embed.add_field(
                    name="✅ Can Afford",
                    value=f"Remaining after purchase: **{format_number(player_gold - total_cost)}** 💰",
                    inline=True
                )

        return embed

    @discord.ui.button(label="✅ Checkout", style=discord.ButtonStyle.success, emoji="💳", row=1)
    async def checkout(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your cart!", ephemeral=True)
            return

        if not self.shopping_cart:
            await interaction.response.send_message("❌ Your cart is empty!", ephemeral=True)
            return

        await interaction.response.defer()

        player_data = self.rpg_core.get_player_data(self.user_id)
        if not player_data:
            await interaction.followup.send("❌ Character not found!")
            return

        # Calculate total cost
        total_cost = 0
        purchased_items = []

        for item_key, cart_item in self.shopping_cart.items():
            quantity = cart_item.get('quantity', 0)
            price_per_item = cart_item.get('price', 0)
            item_name = cart_item.get('name', item_key.replace('_', ' ').title())
            line_total = price_per_item * quantity
            total_cost += line_total

            purchased_items.append(f"• **{item_name}** x{quantity} - {format_number(line_total)} 💰")

            # Add to player inventory
            if item_key in player_data.get('inventory', {}):
                player_data['inventory'][item_key] += quantity
            else:
                player_data['inventory'][item_key] = quantity

        self.rpg_core.save_player_data(self.user_id, player_data)

        # Clear the cart
        self.shopping_cart.clear()

        plagg_responses = [
            "Alright, I processed your bulk order of junk. The money's gone, the items are yours. Don't blame me for your choices.",
            "Checkout complete! You're now significantly poorer but marginally more equipped. Congratulations?",
            "All items delivered to your already-overflowing bag. I hope you're happy with your shopping spree.",
            "Transaction successful. Your gold has found a new home, and you have a bunch of new toys. Economics!"
        ]

        import random
        plagg_response = random.choice(plagg_responses)

        embed = discord.Embed(
            title="✅ Checkout Successful!",
            description=f"*\"{plagg_response}\"*",
            color=COLORS['success']
        )

        embed.add_field(
            name="🛍️ Items Purchased",
            value="\n".join(purchased_items),
            inline=True
        )

        embed.add_field(
            name="💰 Transaction",
            value=f"**Total Paid:** {format_number(total_cost)} 💰\n"
                  f"**Remaining Gold:** {format_number(player_data['gold'])} 💰",
            inline=True
        )

        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=None)

    @discord.ui.button(label="🗑️ Clear Cart", style=discord.ButtonStyle.danger, emoji="🗑️", row=1)
    async def clear_cart(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your cart!", ephemeral=True)
            return

        self.shopping_cart.clear()

        embed = discord.Embed(
            title="🗑️ Cart Cleared",
            description="*\"There, I dumped all that junk out of your cart. Now it's as empty as your decision-making skills. Feel better?\"*",
            color=COLORS['secondary']
        )

        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="⬅️ Back to Shop", style=discord.ButtonStyle.secondary, emoji="🏪", row=1)
    async def back_to_shop(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your cart!", ephemeral=True)
            return

        # Return to main shop
        view = ShopMainView(self.user_id, self.rpg_core)
        view.shopping_cart = self.shopping_cart  # Preserve cart contents

        player_data = self.rpg_core.get_player_data(self.user_id)
        embed = view.create_main_shop_embed(player_data)
        await interaction.response.edit_message(embed=embed, view=view)

class RPGShop(commands.Cog):
    """Interactive RPG shop system with comprehensive navigation."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shop", aliases=["store", "buy", "vendor"])
    async def shop(self, ctx, *, search_term: str = None):
        """Open the interactive shop interface with improved navigation."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        rpg_core = self.bot.get_cog('RPGCore')
        if not rpg_core:
            await ctx.send("❌ RPG system not loaded.")
            return

        player_data = rpg_core.get_player_data(str(ctx.author.id))
        if not player_data:
            embed = create_embed("No Character", "Use `$startrpg` to begin your adventure!", COLORS['error'])
            await ctx.send(embed=embed)
            return

        # If search term provided, show search results
        if search_term:
            await self.show_search_results(ctx, search_term, rpg_core, player_data)
            return

        view = ShopMainView(str(ctx.author.id), rpg_core)

        embed = discord.Embed(
            title="🛒 Plagg's Cheese & Combat Shop",
            description="**Welcome to the finest shop in all dimensions!**\n\n"
                       "Here you can find everything from powerful weapons to magical cheese wheels.\n"
                       "Choose a category below to browse available items.\n\n"
                       "💰 **Shop Features:**\n"
                       "• Quality guaranteed by Plagg himself\n"
                       "• Instant delivery to your inventory\n"
                       "• Cheese-powered discounts available\n"
                       "• No returns (destroyed items stay destroyed)",
            color=COLORS['primary']
        )

        embed.add_field(
            name="🏪 Categories",
            value="⚔️ **Weapons** - Swords, bows, staves\n"
                  "🛡️ **Armor** - Protection and shields\n"
                  "🧪 **Consumables** - Potions and elixirs\n"
                  "💎 **Accessories** - Rings and amulets\n"
                  "✨ **Artifacts** - Legendary items",
            inline=True
        )

        embed.add_field(
            name="💰 Your Funds",
            value=f"**Gold:** `{format_number(player_data['gold'])}`\n"
                  f"**Items:** `{sum(player_data.get('inventory', {}).values())}`",
            inline=True
        )

        embed.set_footer(text="Click a category button to start shopping!")

        await ctx.send(embed=embed, view=view)

    async def show_search_results(self, ctx, search_term, rpg_core, player_data):
        """Show search results for shop items."""
        from rpg_data.game_data import ITEMS
        
        search_term = search_term.lower()
        matching_items = []
        
        for item_key, item_data in ITEMS.items():
            item_name = item_data.get('name', '').lower()
            item_desc = item_data.get('description', '').lower()
            item_type = item_data.get('type', '').lower()
            
            if (search_term in item_name or 
                search_term in item_desc or 
                search_term in item_type or
                search_term in item_key.lower()):
                matching_items.append((item_key, item_data))
        
        if not matching_items:
            embed = discord.Embed(
                title="🔍 No Search Results",
                description=f"*\"Couldn't find anything matching '{search_term}'. Maybe try searching for 'cheese'? Oh wait, there probably isn't any...\"*\n\n"
                           f"**Search Tips:**\n"
                           f"• Try searching by item type (weapon, armor, consumable)\n"
                           f"• Search by rarity (common, rare, legendary)\n"
                           f"• Use partial names (sword, potion, ring)",
                color=COLORS['warning']
            )
            
            # Add quick navigation buttons
            view = discord.ui.View(timeout=300)
            
            shop_button = discord.ui.Button(label="🛒 Browse Shop", style=discord.ButtonStyle.primary)
            async def shop_callback(interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message("Not your shop!", ephemeral=True)
                    return
                
                view = ShopMainView(str(ctx.author.id), rpg_core)
                embed = discord.Embed(
                    title="🛒 Plagg's Cheese & Combat Shop",
                    description="**Welcome to the finest shop in all dimensions!**\n\n"
                               "Here you can find everything from powerful weapons to magical cheese wheels.\n"
                               "Choose a category below to browse available items.",
                    color=COLORS['primary']
                )
                await interaction.response.edit_message(embed=embed, view=view)
            
            shop_button.callback = shop_callback
            view.add_item(shop_button)
            
            await ctx.send(embed=embed, view=view)
            return
        
        # Show search results
        embed = discord.Embed(
            title=f"🔍 Search Results for '{search_term}'",
            description=f"*\"Found {len(matching_items)} items. Better than finding nothing, I guess.\"*",
            color=COLORS['success']
        )
        
        # Limit to first 10 results
        display_items = matching_items[:10]
        
        for item_key, item_data in display_items:
            rarity = item_data.get('rarity', 'common')
            rarity_emoji = {'common': '⚪', 'uncommon': '🟢', 'rare': '🔵', 'epic': '🟣', 
                           'legendary': '🟠', 'mythical': '🔴', 'divine': '⭐', 'cosmic': '🌟'}.get(rarity, '⚪')
            
            price = item_data.get('price', 0)
            item_type = item_data.get('type', 'Unknown').title()
            
            embed.add_field(
                name=f"{rarity_emoji} {item_data.get('name', item_key.title())}",
                value=f"**Type:** {item_type}\n**Price:** {format_number(price)} gold\n*{item_data.get('description', 'No description')[:100]}...*",
                inline=True
            )
        
        if len(matching_items) > 10:
            embed.add_field(
                name="📋 Results Truncated", 
                value=f"Showing first 10 of {len(matching_items)} results. Be more specific!",
                inline=False
            )
        
        # Add navigation view
        view = SearchResultsView(str(ctx.author.id), rpg_core, display_items)
        await ctx.send(embed=embed, view=view)

class SearchResultsView(discord.ui.View):
    """View for handling search results."""
    
    def __init__(self, user_id, rpg_core, items):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.rpg_core = rpg_core
        self.items = items
        
        # Create item dropdown
        options = []
        for item_key, item_data in items[:25]:  # Discord limit
            rarity_emoji = {'common': '⚪', 'uncommon': '🟢', 'rare': '🔵', 'epic': '🟣', 
                           'legendary': '🟠', 'mythical': '🔴'}.get(item_data.get('rarity', 'common'), '⚪')
            
            options.append(discord.SelectOption(
                label=item_data.get('name', item_key.title())[:25],
                value=item_key,
                description=f"{format_number(item_data.get('price', 0))} gold",
                emoji=rarity_emoji
            ))
        
        if options:
            select = discord.ui.Select(placeholder="🛍️ Select item to view details...", options=options)
            select.callback = self.item_selected
            self.add_item(select)
    
    async def item_selected(self, interaction: discord.Interaction):
        if interaction.user.id != int(self.user_id):
            await interaction.response.send_message("Not your selection!", ephemeral=True)
            return
        
        item_key = interaction.data['values'][0]
        view = ItemDetailsView(self.user_id, item_key, self.rpg_core, "search")
        embed = view.create_item_embed()
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label="🛒 Browse Shop", style=discord.ButtonStyle.primary)
    async def browse_shop(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != int(self.user_id):
            await interaction.response.send_message("Not your shop!", ephemeral=True)
            return
        
        view = ShopMainView(self.user_id, self.rpg_core)
        embed = discord.Embed(
            title="🛒 Plagg's Cheese & Combat Shop",
            description="**Welcome to the finest shop in all dimensions!**",
            color=COLORS['primary']
        )
        await interaction.response.edit_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(RPGShop(bot))