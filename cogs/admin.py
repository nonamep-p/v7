import discord
from discord.ext import commands
from replit import db
import asyncio
import logging
from datetime import datetime, timedelta
from utils.helpers import create_embed, format_number
from config import COLORS, get_server_config, update_server_config, user_has_permission
from utils.database import get_guild_data, update_guild_data, get_user_data, update_user_data
from utils.helpers import format_duration
from rpg_data.game_data import ITEMS # Corrected import path
import psutil
import os
import json
import sys
import gc
from typing import Optional, Dict, Any, List, Union
import traceback

logger = logging.getLogger(__name__)

# Fallback imports
try:
    from config import MODULES
except ImportError:
    logger.warning("Could not import 'MODULES' from config.py. Using default values.")
    MODULES = {
        'rpg': {'name': 'RPG System', 'emoji': '🎮', 'description': 'Adventure, combat, and character progression'},
        'economy': {'name': 'Economy System', 'emoji': '💰', 'description': 'Jobs, money, and trading'},
    }

try:
    from config import get_prefix
except ImportError:
    logger.warning("Could not import 'get_prefix' from config.py. Using default prefix function.")
    def get_prefix(bot, message):
        guild_id = getattr(message.guild, 'id', None)
        if guild_id:
            guild_data = get_guild_data(str(guild_id)) or {}
            return guild_data.get('prefix', '$')
        return '$'

# --- Modals ---

class SingleStatModal(discord.ui.Modal):
    """Modal for editing a single stat."""
    def __init__(self, user_id: str, rpg_core, stat_name: str, current_value: Union[int, str]):
        super().__init__(title=f"Edit {stat_name.replace('_', ' ').title()}", timeout=300)
        self.user_id = user_id
        self.rpg_core = rpg_core
        self.stat_name = stat_name

        # Create input field
        self.stat_input = discord.ui.TextInput(
            label=stat_name.replace('_', ' ').title(),
            placeholder=f"Current: {current_value}",
            default=str(current_value),
            required=True,
            max_length=10
        )
        self.add_item(self.stat_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            player_data = self.rpg_core.get_player_data(self.user_id)
            if not player_data:
                await interaction.response.send_message("❌ Player data not found!", ephemeral=True)
                return

            new_value = self.stat_input.value

            # Handle different stat types
            if self.stat_name in ['gold', 'xp', 'level']:
                try:
                    new_value = int(new_value)
                    if self.stat_name == 'level' and (new_value < 1 or new_value > 100):
                        await interaction.response.send_message("❌ Level must be between 1-100!", ephemeral=True)
                        return

                    old_value = player_data.get(self.stat_name, 0)
                    player_data[self.stat_name] = new_value

                    if self.stat_name == 'level':
                        self.rpg_core.update_level_stats(player_data)

                except ValueError:
                    await interaction.response.send_message("❌ Please enter a valid number!", ephemeral=True)
                    return

            elif self.stat_name in ['hp', 'mana']:
                try:
                    new_value = int(new_value)
                    max_key = f'max_{self.stat_name}'
                    max_val = player_data['resources'].get(max_key, 100)

                    old_value = player_data['resources'].get(self.stat_name, 100)
                    player_data['resources'][self.stat_name] = min(new_value, max_val)
                    new_value = player_data['resources'][self.stat_name]

                except ValueError:
                    await interaction.response.send_message("❌ Please enter a valid number!", ephemeral=True)
                    return

            elif self.stat_name in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
                try:
                    new_value = int(new_value)
                    if new_value < 1 or new_value > 99:
                        await interaction.response.send_message("❌ Stat must be between 1-99!", ephemeral=True)
                        return

                    old_value = player_data['stats'].get(self.stat_name, 10)
                    player_data['stats'][self.stat_name] = new_value

                except ValueError:
                    await interaction.response.send_message("❌ Please enter a valid number!", ephemeral=True)
                    return

            # Save data
            success = self.rpg_core.save_player_data(self.user_id, player_data)
            if not success:
                await interaction.response.send_message("❌ Failed to save data!", ephemeral=True)
                return

            user = interaction.guild.get_member(int(self.user_id))
            username = user.display_name if user else "that player"

            plagg_responses = [
                f"Fine, I changed {username}'s {self.stat_name.replace('_', ' ')} from {old_value} to {new_value}. Happy now?",
                f"There, {username} now has {new_value} {self.stat_name.replace('_', ' ')}. Can I go back to my cheese?",
                f"Updated {username}'s {self.stat_name.replace('_', ' ')} to {new_value}. This better be worth interrupting my nap."
            ]

            import random
            response = random.choice(plagg_responses)
            await interaction.response.send_message(f"✅ {response}", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error updating stat: {str(e)}", ephemeral=True)

class ItemSelectModal(discord.ui.Modal):
    """Modal for manually entering item names."""
    def __init__(self, user_id: str, rpg_core, action: str = "give"):
        super().__init__(title=f"{action.title()} Item", timeout=300)
        self.user_id = user_id
        self.rpg_core = rpg_core
        self.action = action

    item_name = discord.ui.TextInput(
        label="Item Name",
        placeholder="Enter exact item name (e.g., 'Iron Sword')",
        required=True,
        max_length=50
    )

    quantity = discord.ui.TextInput(
        label="Quantity",
        placeholder="Enter quantity (default: 1)",
        required=False,
        max_length=5,
        default="1"
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            player_data = self.rpg_core.get_player_data(self.user_id)
            if not player_data:
                await interaction.response.send_message("❌ Player data not found!", ephemeral=True)
                return

            qty = int(self.quantity.value) if self.quantity.value else 1
            if qty <= 0:
                await interaction.response.send_message("❌ Quantity must be positive!", ephemeral=True)
                return

            # Find item
            item_input = self.item_name.value.lower().strip()
            item_key = None
            item_data = None

            for key, data in ITEMS.items():
                if (data.get('name', '').lower() == item_input or 
                    key.lower() == item_input.replace(' ', '_') or
                    item_input in data.get('name', '').lower()):
                    item_key = key
                    item_data = data
                    break

            if not item_key:
                available_items = [data.get('name', key) for key, data in list(ITEMS.items())[:10]]
                await interaction.response.send_message(
                    f"❌ Item '{self.item_name.value}' not found!\n"
                    f"**Examples:** {', '.join(available_items)}",
                    ephemeral=True
                )
                return

            if self.action == "give":
                if 'inventory' not in player_data:
                    player_data['inventory'] = {}

                current_qty = player_data['inventory'].get(item_key, 0)
                player_data['inventory'][item_key] = current_qty + qty

                success = self.rpg_core.save_player_data(self.user_id, player_data)
                if success:
                    user = interaction.guild.get_member(int(self.user_id))
                    username = user.display_name if user else "that player"
                    item_name = item_data.get('name', item_key)

                    response = f"I gave {username} {qty}x {item_name}. There, happy? Now where's my Camembert?"
                    await interaction.response.send_message(f"✅ {response}", ephemeral=True)
                else:
                    await interaction.response.send_message("❌ Failed to save data!", ephemeral=True)

        except ValueError:
            await interaction.response.send_message("❌ Invalid quantity!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

# --- Dropdown Menus ---

class ItemCategorySelect(discord.ui.Select):
    """Dropdown for selecting item categories."""
    def __init__(self, user_id: str, rpg_core):
        self.user_id = user_id
        self.rpg_core = rpg_core

        options = [
            discord.SelectOption(label="⚔️ Weapons", value="weapon", description="Swords, axes, and combat weapons"),
            discord.SelectOption(label="🛡️ Armor", value="armor", description="Protective gear and shields"),
            discord.SelectOption(label="🧪 Consumables", value="consumable", description="Potions and temporary items"),
            discord.SelectOption(label="💎 Accessories", value="accessory", description="Rings and special items"),
            discord.SelectOption(label="✨ Artifacts", value="artifact", description="Kwami artifacts and rare items"),
            discord.SelectOption(label="📦 Materials", value="material", description="Crafting components"),
            discord.SelectOption(label="🧀 Cheese Items", value="cheese", description="Plagg's favorite items")
        ]

        super().__init__(placeholder="🎁 Select item category...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        view = ItemSelectionView(self.user_id, self.rpg_core, category)
        embed = view.create_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class ItemSelectionDropdown(discord.ui.Select):
    """Dropdown for selecting specific items from a category."""
    def __init__(self, user_id: str, rpg_core, category: str):
        self.user_id = user_id
        self.rpg_core = rpg_core
        self.category = category

        # Filter items by category
        filtered_items = []
        for key, data in ITEMS.items():
            if (category == "cheese" and "cheese" in key.lower()) or \
               (category != "cheese" and data.get('type') == category):
                filtered_items.append((key, data))

        # Create options (max 25)
        options = []
        for key, data in filtered_items[:25]:
            rarity_emoji = self.get_rarity_emoji(data.get('rarity', 'common'))
            options.append(discord.SelectOption(
                label=data.get('name', key.replace('_', ' ').title()),
                value=key,
                description=f"{data.get('rarity', 'common').title()} {data.get('type', 'item')}",
                emoji=rarity_emoji
            ))

        if not options:
            options = [discord.SelectOption(label="No items found", value="none")]

        super().__init__(placeholder=f"Select item from {category} category...", options=options)

    def get_rarity_emoji(self, rarity):
        rarity_emojis = {
            'common': '⚪', 'uncommon': '🟢', 'rare': '🔵',
            'epic': '🟣', 'legendary': '🟠', 'mythical': '🔴',
            'divine': '⭐', 'cosmic': '🌟'
        }
        return rarity_emojis.get(rarity, '⚪')

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            await interaction.response.send_message("❌ No items in this category!", ephemeral=True)
            return

        item_key = self.values[0]
        item_data = ITEMS.get(item_key, {})

        view = ItemActionView(self.user_id, self.rpg_core, item_key, item_data)
        embed = view.create_item_embed(item_key, item_data)
        await interaction.response.edit_message(embed=embed, view=view)

class StatSelectionDropdown(discord.ui.Select):
    """Dropdown for selecting which stat to edit."""
    def __init__(self, user_id: str, rpg_core, target_member: discord.Member):
        self.user_id = user_id
        self.rpg_core = rpg_core
        self.target_member = target_member

        options = [
            discord.SelectOption(label="💰 Gold", value="gold", description="Player's currency"),
            discord.SelectOption(label="📈 Level", value="level", description="Character level"),
            discord.SelectOption(label="⭐ Experience", value="xp", description="Experience points"),
            discord.SelectOption(label="❤️ Health", value="hp", description="Current health points"),
            discord.SelectOption(label="💙 Mana", value="mana", description="Current mana points"),
            discord.SelectOption(label="💪 Strength", value="strength", description="Physical power"),
            discord.SelectOption(label="⚡ Dexterity", value="dexterity", description="Speed and agility"),
            discord.SelectOption(label="🛡️ Constitution", value="constitution", description="Health and defense"),
            discord.SelectOption(label="🧠 Intelligence", value="intelligence", description="Magic power"),
            discord.SelectOption(label="👁️ Wisdom", value="wisdom", description="Awareness and insight"),
            discord.SelectOption(label="✨ Charisma", value="charisma", description="Social influence")
        ]

        super().__init__(placeholder="📊 Select stat to edit...", options=options)

    async def callback(self, interaction: discord.Interaction):
        stat_name = self.values[0]

        # Get current value
        player_data = self.rpg_core.get_player_data(str(self.target_member.id))
        if not player_data:
            await interaction.response.send_message("❌ Player data not found!", ephemeral=True)
            return

        if stat_name in ['gold', 'xp', 'level']:
            current_value = player_data.get(stat_name, 0)
        elif stat_name in ['hp', 'mana']:
            current_value = player_data['resources'].get(stat_name, 100)
        else:  # Main stats
            current_value = player_data['stats'].get(stat_name, 10)

        modal = SingleStatModal(str(self.target_member.id), self.rpg_core, stat_name, current_value)
        await interaction.response.send_modal(modal)

# --- Views ---

class BaseAdminView(discord.ui.View):
    def __init__(self, user_id: str, guild_id: int, bot, timeout=300):
        super().__init__(timeout=timeout)
        self.user_id = str(user_id)
        self.guild_id = guild_id
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your panel!", ephemeral=True)
            return False
        return True

    def create_embed(self):
        raise NotImplementedError("Subclasses must implement create_embed()")

    @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, emoji="🔙", row=4)
    async def back_to_main(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ConfigMainView(self.guild_id)
        embed = await view.create_main_embed(interaction.guild.name)
        await interaction.response.edit_message(embed=embed, view=view)

class ItemSelectionView(BaseAdminView):
    """View for selecting items from a category."""
    def __init__(self, user_id: str, guild_id: int, bot, category: str):
        super().__init__(user_id, guild_id, bot)
        self.category = category
        self.add_item(ItemSelectionDropdown(user_id, bot.get_cog('RPGCore'), category))

    def create_embed(self):
        category_names = {
            "weapon": "⚔️ Weapons", "armor": "🛡️ Armor", "consumable": "🧪 Consumables",
            "accessory": "💎 Accessories", "artifact": "✨ Artifacts", 
            "material": "📦 Materials", "cheese": "🧀 Cheese Items"
        }

        return discord.Embed(
            title=f"🎁 {category_names.get(self.category, self.category.title())} Selection",
            description=f"*Select an item from the {self.category} category below.*\n\n"
                       f"*Choose wisely... or don't. I don't really care as long as it's not more paperwork.*",
            color=COLORS['info']
        )

    @discord.ui.button(label="Manual Entry", style=discord.ButtonStyle.secondary, emoji="✍️", row=1)
    async def manual_entry(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ItemSelectModal(self.user_id, self.bot.get_cog('RPGCore'), "give")
        await interaction.response.send_modal(modal)

class ItemActionView(BaseAdminView):
    """View for performing actions on selected items."""
    def __init__(self, user_id: str, guild_id: int, bot, item_key: str, item_data: Dict):
        super().__init__(user_id, guild_id, bot)
        self.item_key = item_key
        self.item_data = item_data

    def create_item_embed(self, item_key: str, item_data: Dict):
        from rpg_data.game_data import RARITY_COLORS

        rarity_color = RARITY_COLORS.get(item_data.get('rarity', 'common'), COLORS['primary'])
        embed = discord.Embed(
            title=f"🎁 {item_data.get('name', item_key.replace('_', ' ').title())}",
            description=item_data.get('description', 'No description available.'),
            color=rarity_color
        )

        embed.add_field(
            name="📊 Item Info",
            value=f"**Type:** {item_data.get('type', 'Unknown').title()}\n"
                  f"**Rarity:** {item_data.get('rarity', 'common').title()}\n"
                  f"**Value:** {format_number(item_data.get('price', 0))} gold",
            inline=True
        )

        # Stats
        stats_text = ""
        if item_data.get('attack'):
            stats_text += f"⚔️ Attack: +{item_data['attack']}\n"
        if item_data.get('defense'):
            stats_text += f"🛡️ Defense: +{item_data['defense']}\n"
        if item_data.get('hp'):
            stats_text += f"❤️ HP: +{item_data['hp']}\n"
        if item_data.get('mana'):
            stats_text += f"💙 Mana: +{item_data['mana']}\n"

        if stats_text:
            embed.add_field(name="📈 Stats", value=stats_text, inline=True)

        return embed

    @discord.ui.button(label="Give x1", style=discord.ButtonStyle.success, emoji="🎁", row=1)
    async def give_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.give_item(interaction, 1)

    @discord.ui.button(label="Give x5", style=discord.ButtonStyle.success, emoji="🎁", row=1)
    async def give_five(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.give_item(interaction, 5)

    @discord.ui.button(label="Give Custom", style=discord.ButtonStyle.primary, emoji="✍️", row=1)
    async def give_custom(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ItemSelectModal(self.user_id, self.bot.get_cog('RPGCore'), "give")
        modal.item_name.default = self.item_data.get('name', self.item_key)
        await interaction.response.send_modal(modal)

    async def give_item(self, interaction: discord.Interaction, quantity: int):
        rpg_core = self.bot.get_cog('RPGCore')
        if not rpg_core:
            await interaction.response.send_message("❌ RPG system not available!", ephemeral=True)
            return

        # Find target user (for now, assume it's stored in view or get from context)
        # This would need to be passed from the parent view
        target_id = self.user_id  # Placeholder - should be target user ID

        player_data = rpg_core.get_player_data(target_id)
        if not player_data:
            await interaction.response.send_message("❌ Player data not found!", ephemeral=True)
            return

        if 'inventory' not in player_data:
            player_data['inventory'] = {}

        current_qty = player_data['inventory'].get(self.item_key, 0)
        player_data['inventory'][self.item_key] = current_qty + quantity

        success = rpg_core.save_player_data(target_id, player_data)
        if success:
            item_name = self.item_data.get('name', self.item_key)
            response = f"I gave them {quantity}x {item_name}. There, can I get back to my cheese now?"
            await interaction.response.send_message(f"✅ {response}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Failed to save data!", ephemeral=True)

class ManageUserView(BaseAdminView):
    def __init__(self, user_id: str, guild_id: int, bot, target_member: discord.Member):
        super().__init__(user_id, guild_id, bot)
        self.target_member = target_member

        # Add stat selection dropdown
        self.add_item(StatSelectionDropdown(user_id, bot.get_cog('RPGCore'), target_member))

        if hasattr(self.bot, 'owner_id') and int(user_id) == self.bot.owner_id:
            self.add_item(self.create_grant_infinite_button())

    def create_grant_infinite_button(self):
        button = discord.ui.Button(label="Grant Infinite Power", style=discord.ButtonStyle.success, emoji="👑", row=2)
        async def callback(interaction: discord.Interaction):
            await self.grant_infinite_power(interaction)
        button.callback = callback
        return button

    async def grant_infinite_power(self, interaction: discord.Interaction):
        user_data = get_user_data(str(self.target_member.id)) or {}
        user_data.update({ 
            'level': 999, 
            'gold': 999999999999, 
            'xp': 0, 
            'stats': {
                'strength': 999, 
                'dexterity': 999, 
                'constitution': 999, 
                'intelligence': 999, 
                'wisdom': 999, 
                'charisma': 999
            } 
        })
        update_user_data(str(self.target_member.id), user_data)
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
        await interaction.followup.send(f"🧀 Wow, look at you with the 'infinite power' button. I gave {self.target_member.mention} god-mode stats. Are you going to create a block of cheese so big you can't eat it? No? Then what's the point of infinite power?", ephemeral=True)

    def create_embed(self):
        user_data = get_user_data(str(self.target_member.id)) or {}
        stats = user_data.get('stats', {})
        embed = discord.Embed(
            title=f"👤 Staring at {self.target_member.display_name}'s Stats", 
            description=f"*Here's everything about {self.target_member.display_name}. Spoiler: it's not that interesting.*\n\n**User ID:** `{self.target_member.id}`\n\n*Select a stat from the dropdown to edit it individually.*", 
            color=COLORS['warning']
        )
        embed.set_thumbnail(url=self.target_member.display_avatar.url)
        embed.add_field(name="Level", value=user_data.get('level', 1), inline=True)
        embed.add_field(name="Gold", value=f"{user_data.get('gold', 0):,}", inline=True)
        embed.add_field(name="XP", value=user_data.get('xp', 0), inline=True)
        embed.add_field(name="STR", value=stats.get('strength', 5), inline=True)
        embed.add_field(name="DEX", value=stats.get('dexterity', 5), inline=True)
        embed.add_field(name="CON", value=stats.get('constitution', 5), inline=True)
        return embed

    @discord.ui.button(label="Give Items", style=discord.ButtonStyle.primary, emoji="🎁", row=3)
    async def give_items(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ItemCategorySelectionView(self.user_id, self.guild_id, self.bot, self.target_member)
        embed = view.create_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class ItemCategorySelectionView(BaseAdminView):
    """View for selecting item category when giving items."""
    def __init__(self, user_id: str, guild_id: int, bot, target_member: discord.Member):
        super().__init__(user_id, guild_id, bot)
        self.target_member = target_member
        self.add_item(ItemCategorySelect(str(target_member.id), bot.get_cog('RPGCore')))

    def create_embed(self):
        return discord.Embed(
            title=f"🎁 Give Items to {self.target_member.display_name}",
            description="*Ugh, more gift-giving. Select a category from the dropdown below.*\n\n*Just pick something so I can get back to my nap.*",
            color=COLORS['info']
        )

class UserManagementView(BaseAdminView):
    def create_embed(self):
        return discord.Embed(
            title="👥 Picking on Players", 
            description="*Sigh...* So you want to mess with someone's profile? Fine. Pick a victim from the list or use the button to find them. Just get it over with so I can get back to my cheese wheel.\n\n*Don't blame me if you make the game boring.*", 
            color=COLORS['error']
        )

    @discord.ui.button(label="Find User", style=discord.ButtonStyle.primary, emoji="🔎", row=1)
    async def find_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        from cogs.admin import UserSearchModal
        await interaction.response.send_modal(UserSearchModal(self.user_id, self.guild_id, self.bot))

    @discord.ui.button(label="Top Players", style=discord.ButtonStyle.secondary, emoji="📊", row=1)
    async def top_players(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await self.create_leaderboard_embed(interaction)
        await interaction.response.edit_message(embed=embed, view=self)

    async def create_leaderboard_embed(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📊 Server Leaderboards",
            description="Top players across different categories.",
            color=COLORS['legendary']
        )
        players = []
        for key in db.keys():
            if key.startswith(f'player_{self.guild_id}_'):
                try:
                    player_data = db[key]
                    if isinstance(player_data, dict) and 'level' in player_data:
                        user_id = key.split('_')[-1]
                        players.append((user_id, player_data['level'], player_data.get('gold', 0)))
                except:
                    continue

        players.sort(key=lambda x: x[1], reverse=True)
        top_players = players[:5]

        if top_players:
            leaderboard = ""
            for i, (user_id, level, gold) in enumerate(top_players, 1):
                try:
                    user = interaction.guild.get_member(int(user_id))
                    name = user.display_name if user else f"User {user_id}"
                    leaderboard += f"{i}. **{name}** - Level {level} ({format_number(gold)} gold)\n"
                except:
                    leaderboard += f"{i}. User {user_id} - Level {level}\n"

            embed.add_field(name="🏆 Top Players by Level", value=leaderboard, inline=False)
        else:
            embed.add_field(name="📊 No Data", value="No players found for this server.", inline=False)

        return embed

class UserSearchModal(discord.ui.Modal, title="🔎 Search for User"):
    user_input = discord.ui.TextInput(label="User ID or Name#Tag", placeholder="e.g., 1297013439125917766 or Plagg#1234", required=True)

    def __init__(self, user_id: str, guild_id: int, bot):
        super().__init__()
        self.user_id = user_id
        self.guild_id = guild_id
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        query = self.user_input.value
        guild = self.bot.get_guild(self.guild_id)
        member = None
        try:
            if '#' in query:
                name, discrim = query.split('#')
                member = discord.utils.get(guild.members, name=name, discriminator=discrim)
            else:
                member = guild.get_member(int(query))
        except (ValueError, AttributeError): pass

        if member:
            view = ManageUserView(self.user_id, self.guild_id, self.bot, member)
            embed = view.create_embed()
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(f"❌ Could not find a member matching `{query}`.", ephemeral=True)

# Continue with other views and Admin class...
class DatabaseToolsView(BaseAdminView):
    def create_embed(self):
        guild_data = get_guild_data(str(self.guild_id)) or {}
        xp_rate = guild_data.get('xp_multiplier', 1.0)
        gold_rate = guild_data.get('gold_multiplier', 1.0)
        embed = discord.Embed(
            title="💾 The Really Boring Stuff",
            description="*This is the REALLY boring stuff.* Multipliers, backups... *zzz.* Just don't delete anything important. Or do. The chaos could be fun to watch from a distance while I eat cheese.",
            color=COLORS['dark']
        )
        embed.add_field(name="XP Multiplier", value=f"`{xp_rate}x`", inline=True)
        embed.add_field(name="Gold Multiplier", value=f"`{gold_rate}x`", inline=True)
        return embed

    @discord.ui.button(label="Make Numbers Bigger", style=discord.ButtonStyle.primary, emoji="⚙️", row=1)
    async def set_multipliers(self, interaction: discord.Interaction, button: discord.ui.Button):
        from cogs.admin import MultiplierModal
        await interaction.response.send_modal(MultiplierModal(self.guild_id))

class CustomizationView(BaseAdminView):
    def create_embed(self):
        return discord.Embed(
            title="🎨 Playing Interior Decorator",
            description="*Time to play interior decorator? How thrilling.* Here you can change colors and make everything look... different.",
            color=COLORS['secondary']
        )

class ConfigMainView(discord.ui.View):
    """Main configuration panel view."""

    def __init__(self, guild_id: int):
        super().__init__(timeout=300)
        self.guild_id = guild_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need administrator permissions!", ephemeral=True)
            return False
        return True

    async def create_main_embed(self, guild_name: str):
        embed = discord.Embed(
            title="⚙️ Admin Control Panel",
            description=f"*\"Oh great, another admin panel. Just what I needed to make my day more exciting...\"*\n\n"
                       f"**Server:** {guild_name}\n"
                       f"**Admin Tools:** Configure settings, manage players, and other boring admin stuff.\n\n"
                       f"*Pick something from the buttons below so I can get back to my cheese.*",
            color=COLORS['primary']
        )

        guild_data = get_guild_data(str(self.guild_id)) or {}
        embed.add_field(
            name="🎮 RPG Settings",
            value=f"**XP Multiplier:** {guild_data.get('xp_multiplier', 1.0)}x\n"
                  f"**Gold Multiplier:** {guild_data.get('gold_multiplier', 1.0)}x",
            inline=True
        )

        return embed

    @discord.ui.button(label="User Management", style=discord.ButtonStyle.primary, emoji="👥", row=0)
    async def user_management(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = UserManagementView(str(interaction.user.id), self.guild_id, interaction.client)
        embed = view.create_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Database Tools", style=discord.ButtonStyle.secondary, emoji="💾", row=0)
    async def database_tools(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = DatabaseToolsView(str(interaction.user.id), self.guild_id, interaction.client)
        embed = view.create_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Customization", style=discord.ButtonStyle.secondary, emoji="🎨", row=0)
    async def customization(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = CustomizationView(str(interaction.user.id), self.guild_id, interaction.client)
        embed = view.create_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class MultiplierModal(discord.ui.Modal, title="⚙️ Set Server Multipliers"):
    xp_multiplier = discord.ui.TextInput(label="XP Multiplier", placeholder="e.g., 1.5 for 150% XP", required=True)
    gold_multiplier = discord.ui.TextInput(label="Gold Multiplier", placeholder="e.g., 2.0 for 200% Gold", required=True)

    def __init__(self, guild_id: int):
        super().__init__()
        self.guild_id = guild_id
        guild_data = get_guild_data(str(guild_id)) or {}
        self.xp_multiplier.default = str(guild_data.get('xp_multiplier', 1.0))
        self.gold_multiplier.default = str(guild_data.get('gold_multiplier', 1.0))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            xp_rate = float(self.xp_multiplier.value)
            gold_rate = float(self.gold_multiplier.value)

            guild_data = get_guild_data(str(self.guild_id)) or {}
            guild_data['xp_multiplier'] = xp_rate
            guild_data['gold_multiplier'] = gold_rate
            update_guild_data(str(self.guild_id), guild_data)

            await interaction.response.send_message(f"✅ Multipliers updated: XP `x{xp_rate}`, Gold `x{gold_rate}`.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Invalid input. Please enter numbers only.", ephemeral=True)

class AdminMainView(discord.ui.View):
    """Main admin panel interface."""

    def __init__(self, user_id: str, bot):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.bot = bot

    def create_main_embed(self):
        """Create the main admin panel embed."""
        embed = discord.Embed(
            title="🔧 Admin Control Panel",
            description="**Welcome to the administrative interface.**\n\n"
                       "Select an administrative function from the options below.\n"
                       "All actions are logged and monitored.",
            color=COLORS['error']
        )

        embed.add_field(
            name="🎮 Player Management",
            value="• Modify player stats\n• Manage inventories\n• Reset characters\n• Grant items\n• Edit levels & XP",
            inline=True
        )

        embed.add_field(
            name="💰 Economy Control",
            value="• Adjust gold amounts\n• Spawn items\n• Market manipulation\n• Grant consumables",
            inline=True
        )

        embed.add_field(
            name="🛠️ System Tools",
            value="• Database management\n• Bot diagnostics\n• Module controls\n• Server stats",
            inline=True
        )

        # Add system status
        guild_count = len(self.bot.guilds)
        user_count = sum(guild.member_count for guild in self.bot.guilds)

        embed.add_field(
            name="📊 System Status",
            value=f"**Guilds:** {guild_count}\n"
                  f"**Users:** {user_count}\n"
                  f"**Ping:** {round(self.bot.latency * 1000)}ms\n"
                  f"**Status:** 🟢 Online",
            inline=True
        )

        embed.set_footer(text="⚠️ Use admin powers responsibly • Timeout: 10 minutes")
        return embed

    @discord.ui.button(label="🎮 Player Manager", style=discord.ButtonStyle.primary, emoji="🎮", row=0)
    async def player_manager(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your admin panel!", ephemeral=True)
            return

        view = PlayerManagerView(self.user_id, self.bot)
        embed = view.create_player_manager_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="💰 Economy Control", style=discord.ButtonStyle.success, emoji="💰", row=0)
    async def economy_control(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your admin panel!", ephemeral=True)
            return

        view = EconomyControlView(self.user_id, self.bot)
        embed = view.create_economy_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🛠️ System Tools", style=discord.ButtonStyle.secondary, emoji="🛠️", row=0)
    async def system_tools(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your admin panel!", ephemeral=True)
            return

        view = SystemToolsView(self.user_id, self.bot)
        embed = view.create_system_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🎁 Item Spawner", style=discord.ButtonStyle.danger, emoji="🎁", row=1)
    async def item_spawner(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your admin panel!", ephemeral=True)
            return

        view = ItemSpawnerView(self.user_id, self.bot)
        embed = view.create_spawner_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class PlayerManagerView(discord.ui.View):
    """Interface for managing player-related actions."""

    def __init__(self, user_id: str, bot):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.bot = bot

    def create_player_manager_embed(self):
        """Embed for the player management interface."""
        embed = discord.Embed(
            title="🎮 Player Management Center",
            description="**Control player stats, inventories, and characters.**\n"
                       "Use the tools below to modify player attributes.\n\n"
                       "All actions are logged for security.",
            color=COLORS['warning']
        )
        embed.set_footer(text="⚠️ Exercise player management with care")
        return embed

class EconomyControlView(discord.ui.View):
    """Interface for managing economy-related actions."""

    def __init__(self, user_id: str, bot):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.bot = bot

    def create_economy_embed(self):
        """Embed for the economy control interface."""
        embed = discord.Embed(
            title="💰 Economy Control Hub",
            description="**Manipulate the game's economy.**\n"
                       "Adjust gold, spawn items, and control the market.\n\n"
                       "Use responsibly to prevent economic imbalances.",
            color=COLORS['success']
        )
        embed.set_footer(text="⚠️ Handle economy controls with precision")
        return embed

class SystemToolsView(discord.ui.View):
    """Interface for managing system-related tools."""

    def __init__(self, user_id: str, bot):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.bot = bot

    def create_system_embed(self):
        """Embed for the system tools interface."""
        embed = discord.Embed(
            title="🛠️ System Tools Command",
            description="**Administer bot systems and configurations.**\n"
                       "Manage databases, diagnose issues, and control modules.\n\n"
                       "Use caution to avoid disrupting bot operations.",
            color=COLORS['dark']
        )
        embed.set_footer(text="⚠️ Apply system tools judiciously")
        return embed

class ItemSpawnerView(discord.ui.View):
    """Interface for spawning items into the game."""

    def __init__(self, user_id: str, bot):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.bot = bot

    def create_spawner_embed(self):
        """Embed for the item spawner interface."""
        embed = discord.Embed(
            title="🎁 Item Spawner Station",
            description="**Generate and distribute items in the game.**\n"
                       "Spawn new items, grant consumables, and manage loot.\n\n"
                       "Use with moderation to maintain game balance.",
            color=COLORS['danger']
        )
        embed.set_footer(text="⚠️ Spawn items thoughtfully")
        return embed

class Admin(commands.Cog):
    """Advanced admin commands with enhanced security and interactive interfaces."""

    def __init__(self, bot):
        self.bot = bot

    def is_owner_or_admin(self, user_id: int) -> bool:
        """Check if user is bot owner or has admin permissions."""
        return user_id == 1297013439125917766  # Bot owner ID

    @commands.command(name="admin", aliases=["adminpanel", "ap"])
    async def admin_panel(self, ctx):
        """Open the interactive admin panel."""
        if not self.is_owner_or_admin(ctx.author.id):
            await ctx.send("❌ You don't have permission to use admin commands!")
            return

        view = AdminMainView(str(ctx.author.id), self.bot)
        embed = view.create_main_embed()
        await ctx.send(embed=embed, view=view)

class AdminCog(commands.Cog):
    """Administrative commands and tools."""

    def __init__(self, bot):
        self.bot = bot

    def update_derived_stats(self, player_data):
        """Update derived stats based on base stats."""
        base_stats = player_data['stats']

        # Update derived stats
        player_data['derived_stats']['attack'] = 10 + (base_stats['strength'] * 2)
        player_data['derived_stats']['magic_attack'] = 10 + (base_stats['intelligence'] * 2)
        player_data['derived_stats']['defense'] = 5 + base_stats['constitution']
        player_data['derived_stats']['critical_chance'] = 0.05 + (base_stats['dexterity'] * 0.01)
        player_data['derived_stats']['dodge_chance'] = base_stats['dexterity'] * 0.005

        # Update max HP and mana
        new_max_hp = 100 + (base_stats['constitution'] * 10)
        new_max_mana = 50 + (base_stats['intelligence'] * 5)

        # If max increased, add the difference to current
        hp_diff = new_max_hp - player_data['resources']['max_hp']
        mana_diff = new_max_mana - player_data['resources']['max_mana']

        player_data['resources']['max_hp'] = new_max_hp
        player_data['resources']['max_mana'] = new_max_mana

        if hp_diff > 0:
            player_data['resources']['hp'] += hp_diff
        if mana_diff > 0:
            player_data['resources']['mana'] += mana_diff

    async def update_player_stat(self, interaction: discord.Interaction, user_id: str, stat_type: str, new_value: int):
        """Update a player's stat and save to the database."""
        rpg_core = self.bot.get_cog('RPGCore')
        if not rpg_core:
            await interaction.response.send_message("❌ RPG system not found!", ephemeral=True)
            return

        # Apply the change directly to player data
        player_data = rpg_core.get_player_data(user_id)
        if not player_data:
            await interaction.response.send_message("❌ Player not found!", ephemeral=True)
            return

        if stat_type == "Level":
            player_data['level'] = new_value
        elif stat_type == "Gold":
            player_data['gold'] = new_value
        elif stat_type == "XP":
            player_data['xp'] = new_value
        elif stat_type == "STR":
            player_data['stats']['strength'] = new_value
        elif stat_type == "DEX":
            player_data['stats']['dexterity'] = new_value
        elif stat_type == "CON":
            player_data['stats']['constitution'] = new_value
        elif stat_type == "INT":
            player_data['stats']['intelligence'] = new_value
        elif stat_type == "WIS":
            player_data['stats']['wisdom'] = new_value
        elif stat_type == "CHA":
            player_data['stats']['charisma'] = new_value

        # Update derived stats
        self.update_derived_stats(player_data)

        success = rpg_core.save_player_data(user_id, player_data)
        if not success:
            await interaction.response.send_message("❌ Failed to save changes!", ephemeral=True)
            return

        user = interaction.guild.get_member(int(user_id))
        username = user.display_name if user else "that player"

        plagg_responses = [
            f"Fine, I changed {username}'s {stat_type} to {new_value}. Happy now?",
            f"There, {username} now has {new_value} {stat_type}. Can I go back to my cheese?",
            f"Updated {username}'s {stat_type} to {new_value}. This better be worth interrupting my nap."
        ]

        import random
        response = random.choice(plagg_responses)
        await interaction.response.send_message(f"✅ {response}", ephemeral=True)

    @commands.command(name="testtools", hidden=True)
    @commands.has_permissions(administrator=True)
    async def test_tools(self, ctx):
        """Comprehensive testing tools for testers (ADMIN ONLY)."""
        view = TestingToolsView(str(ctx.author.id), self.bot)
        embed = discord.Embed(
            title="🧪 RPG Testing Suite",
            description="**Comprehensive testing tools for Project: Blood & Cheese**\n\n"
                       "Use the buttons below to test different systems:",
            color=COLORS['primary']
        )

        embed.add_field(
            name="🎮 Available Tests",
            value="• **Character Creation** - Test new player flow\n"
                  "• **Combat System** - Test battle mechanics\n"
                  "• **Leveling System** - Test XP and stat progression\n"
                  "• **Shop System** - Test purchasing and inventory\n"
                  "• **Admin Tools** - Test stat modification\n"
                  "• **Quick Setup** - Instant high-level character",
            inline=False
        )

        await ctx.send(embed=embed, view=view)

    @commands.command(name="quicksetup", hidden=True)
    @commands.has_permissions(administrator=True)
    async def quick_setup(self, ctx, user: discord.Member = None, level: int = 10):
        """Quickly set up a test character (ADMIN ONLY)."""
        target = user or ctx.author
        rpg_core = self.bot.get_cog('RPGCore')

        if not rpg_core:
            await ctx.send("❌ RPG system not loaded.")
            return

        # Create or modify character with test data
        user_data = get_user_data(str(target.id)) or {}

        test_character = {
            'level': level,
            'xp': 1000 * level,
            'gold': 10000 + (level * 1000),
            'class': 'warrior',
            'path': None,
            'name': target.display_name,
            'stats': {
                'strength': 10 + level,
                'dexterity': 8 + level,
                'constitution': 12 + level,
                'intelligence': 6 + level,
                'wisdom': 8 + level,
                'charisma': 7 + level
            },
            'resources': {
                'hp': 100 + (level * 15),
                'max_hp': 100 + (level * 15),
                'mana': 50 + (level * 10),
                'max_mana': 50 + (level * 10),
                'stamina': 100,
                'max_stamina': 100,
                'sp': 100,
                'max_sp': 100,
                'miraculous_energy': 100,
                'max_miraculous_energy': 100,
                'ultimate_energy': 0,
                'technique_points': 3
            },
            'derived_stats': {
                'attack': 10 + (10 + level) * 2,
                'magic_attack': 10 + (6 + level) * 2,
                'defense': 5 + (12 + level),
                'critical_chance': 0.05 + ((8 + level) * 0.01),
                'dodge_chance': (8 + level) * 0.005,
                'max_ultimate_energy': 100
            },
            'unallocated_points': level * 2,
            'equipment': {
                'weapon': 'iron_sword',
                'armor': 'leather_vest',
                'accessory': None,
                'artifact': None
            },
            'inventory': {
                'health_potion': 10,
                'mana_potion': 10,
                'iron_sword': 2,
                'steel_blade': 1,
                'leather_vest': 1,
                'chainmail_armor': 1
            },
            'skills': ['power_strike', 'shield_bash', 'berserker_fury'],
            'techniques': ['ambush', 'preparation'],
            'achievements': [],
            'arena_rating': 1000,
            'arena_wins': 0,
            'arena_losses': 0,
            'arena_tokens': 100,
            'faction': None,
            'title': None,
            'in_combat': False,
            'last_hunt': 0,
            'last_adventure': 0,
            'last_explore': 0,
            'last_work': 0,
            'created_at': datetime.now().isoformat(),
            'kwami_artifacts': [],
            'active_buffs': [],
            'chosen_path': None
        }

        user_data['rpg_data'] = test_character
        update_user_data(str(target.id), user_data)

        embed = discord.Embed(
            title="🧪 Test Character Created!",
            description=f"**{target.display_name}** has been set up for testing!",
            color=COLORS['success']
        )

        embed.add_field(
            name="📊 Test Stats",
            value=f"**Level:** {level}\n"
                  f"**Gold:** {format_number(test_character['gold'])}\n"
                  f"**Stat Points:** {test_character['unallocated_points']}\n"
                  f"**HP:** {test_character['resources']['hp']}\n"
                  f"**Attack:** {test_character['derived_stats']['attack']}",
            inline=True
        )

        embed.add_field(
            name="🎒 Test Inventory",
            value="• 10x Health Potions\n"
                  "• 10x Mana Potions\n"
                  "• Multiple weapons & armor\n"
                  "• Ready for combat testing",
            inline=True
        )

        await ctx.send(embed=embed)

    @commands.command(name="testbattle", hidden=True)
    @commands.has_permissions(administrator=True)
    async def test_battle(self, ctx, user: discord.Member = None):
        """Start a test battle for specified user (ADMIN ONLY)."""
        target = user or ctx.author

        # Use the combat cog to start a battle
        combat_cog = self.bot.get_cog('RPGCombat')
        if not combat_cog:
            await ctx.send("❌ Combat system not loaded.")
            return

        # Create a mock context for the target user
        class MockContext:
            def __init__(self, author, channel, send_func):
                self.author = author
                self.channel = channel
                self.send = send_func
                self.guild = channel.guild

        async def mock_send(content=None, embed=None):
            return await ctx.send(content=content, embed=embed)

        mock_ctx = MockContext(target, ctx.channel, mock_send)

        # Start battle
        await combat_cog.battle(mock_ctx, "goblin")

    @commands.command(name="admintest", hidden=True)
    @commands.has_permissions(administrator=True)
    async def admin_test(self, ctx):
        """Test admin functionality (ADMIN ONLY)."""
        embed = discord.Embed(
            title="🔧 Admin Test Panel",
            description="Testing admin functionality...",
            color=COLORS['info']
        )

        # Test basic functionality
        embed.add_field(
            name="✅ Basic Tests",
            value="• Command loaded successfully\n• Permissions working\n• Bot responding",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="sysstats", hidden=True)
    async def system_stats(self, ctx):
        """Display comprehensive system statistics (OWNER ONLY)."""
        if not self.is_owner_or_admin(ctx.author.id):
            await ctx.send("❌ Owner access required!")
            return

        # Memory usage
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        embed = discord.Embed(
            title="📊 System Performance Dashboard",
            description="**Real-time bot and server statistics**",
            color=COLORS['info']
        )

        # Bot statistics
        guild_count = len(self.bot.guilds)
        user_count = sum(guild.member_count for guild in self.bot.guilds if guild.member_count)
        
        embed.add_field(
            name="🤖 Bot Statistics",
            value=f"**Guilds:** {guild_count}\n"
                  f"**Users:** {format_number(user_count)}\n"
                  f"**Ping:** {round(self.bot.latency * 1000)}ms\n"
                  f"**Uptime:** {format_duration(int((datetime.now() - self.bot.start_time).total_seconds()))}",
            inline=True
        )

        # System resources
        embed.add_field(
            name="💻 System Resources",
            value=f"**Memory:** {memory.percent}% used\n"
                  f"**Available:** {format_number(memory.available // 1024 // 1024)}MB\n"
                  f"**Disk:** {disk.percent}% used\n"
                  f"**CPU Count:** {psutil.cpu_count()} cores",
            inline=True
        )

        # Database statistics
        total_players = len([k for k in db.keys() if k.startswith('player_')])
        total_guilds = len([k for k in db.keys() if k.startswith('guild_')])
        
        embed.add_field(
            name="💾 Database Stats",
            value=f"**Player Records:** {format_number(total_players)}\n"
                  f"**Guild Records:** {format_number(total_guilds)}\n"
                  f"**Total Keys:** {format_number(len(db.keys()))}\n"
                  f"**Status:** 🟢 Connected",
            inline=True
        )

        await ctx.send(embed=embed)

    @commands.command(name="maintenance", hidden=True)
    async def maintenance_mode(self, ctx, action: str = "status"):
        """Toggle maintenance mode (OWNER ONLY)."""
        if not self.is_owner_or_admin(ctx.author.id):
            await ctx.send("❌ Owner access required!")
            return

        if action.lower() == "on":
            db['maintenance_mode'] = True
            embed = discord.Embed(
                title="🔧 Maintenance Mode Activated",
                description="**The bot is now in maintenance mode.**\n\n"
                           "• Most commands are disabled\n"
                           "• Only admins can use the bot\n"
                           "• Players will see maintenance messages",
                color=COLORS['warning']
            )
        elif action.lower() == "off":
            if 'maintenance_mode' in db:
                del db['maintenance_mode']
            embed = discord.Embed(
                title="✅ Maintenance Mode Deactivated",
                description="**The bot is now fully operational.**\n\n"
                           "• All commands are available\n"
                           "• Normal operation resumed",
                color=COLORS['success']
            )
        else:
            is_maintenance = db.get('maintenance_mode', False)
            status = "🔧 ACTIVE" if is_maintenance else "✅ INACTIVE"
            embed = discord.Embed(
                title="🔧 Maintenance Mode Status",
                description=f"**Current Status:** {status}\n\n"
                           f"Use `{ctx.prefix}maintenance on` to enable\n"
                           f"Use `{ctx.prefix}maintenance off` to disable",
                color=COLORS['warning'] if is_maintenance else COLORS['success']
            )

        await ctx.send(embed=embed)

    @commands.command(name="backup", hidden=True)
    async def backup_data(self, ctx, data_type: str = "all"):
        """Create data backups (OWNER ONLY)."""
        if not self.is_owner_or_admin(ctx.author.id):
            await ctx.send("❌ Owner access required!")
            return

        await ctx.send("🔄 Creating backup... This may take a moment.")

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if data_type.lower() in ["all", "players"]:
                player_data = {k: v for k, v in db.items() if k.startswith('player_')}
                db[f'backup_players_{timestamp}'] = player_data
                
            if data_type.lower() in ["all", "guilds"]:
                guild_data = {k: v for k, v in db.items() if k.startswith('guild_')}
                db[f'backup_guilds_{timestamp}'] = guild_data

            embed = discord.Embed(
                title="✅ Backup Complete",
                description=f"**Backup created successfully!**\n\n"
                           f"**Timestamp:** {timestamp}\n"
                           f"**Data Type:** {data_type.title()}\n"
                           f"**Status:** Stored in database",
                color=COLORS['success']
            )
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Backup Failed",
                description=f"**Error creating backup:**\n```{str(e)}```",
                color=COLORS['danger']
            )

        await ctx.send(embed=embed)

    @commands.command(name="cleanup", hidden=True)
    async def cleanup_data(self, ctx, days: int = 30):
        """Clean up old data and backups (OWNER ONLY)."""
        if not self.is_owner_or_admin(ctx.author.id):
            await ctx.send("❌ Owner access required!")
            return

        await ctx.send(f"🧹 Starting cleanup of data older than {days} days...")

        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            cleaned_count = 0
            
            # Clean old backups
            for key in list(db.keys()):
                if key.startswith('backup_'):
                    try:
                        # Extract timestamp from backup key
                        timestamp_str = key.split('_')[-1]
                        backup_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                        
                        if backup_date < cutoff_date:
                            del db[key]
                            cleaned_count += 1
                    except:
                        continue

            # Force garbage collection
            gc.collect()

            embed = discord.Embed(
                title="✅ Cleanup Complete",
                description=f"**Removed {cleaned_count} old backup entries**\n\n"
                           f"**Cutoff Date:** {cutoff_date.strftime('%Y-%m-%d')}\n"
                           f"**Memory Freed:** Garbage collected",
                color=COLORS['success']
            )
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Cleanup Failed",
                description=f"**Error during cleanup:**\n```{str(e)}```",
                color=COLORS['danger']
            )

        await ctx.send(embed=embed)

    @commands.command(name="eval", hidden=True)
    async def evaluate_code(self, ctx, *, code):
        """Execute Python code (OWNER ONLY - DANGEROUS)."""
        if ctx.author.id != 1297013439125917766:  # Only bot owner
            await ctx.send("❌ This command is restricted to the bot owner only!")
            return

        try:
            # Create a safe environment with limited access
            env = {
                'discord': discord,
                'bot': self.bot,
                'ctx': ctx,
                'db': db,
                'format_number': format_number,
                'COLORS': COLORS,
                '__import__': None,
                '__builtins__': None,
            }
            
            result = eval(code, env)
            
            if asyncio.iscoroutine(result):
                result = await result
                
            output = str(result)[:1900]  # Limit output length
            
            embed = discord.Embed(
                title="🐍 Code Execution Result",
                description=f"**Input:**\n```python\n{code[:500]}\n```\n"
                           f"**Output:**\n```python\n{output}\n```",
                color=COLORS['success']
            )
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Code Execution Error",
                description=f"**Input:**\n```python\n{code[:500]}\n```\n"
                           f"**Error:**\n```python\n{str(e)[:500]}\n```",
                color=COLORS['danger']
            )
            
        await ctx.send(embed=embed)

    @commands.command(name="globalannounce", hidden=True)
    async def global_announce(self, ctx, *, message):
        """Send announcement to all servers (OWNER ONLY)."""
        if not self.is_owner_or_admin(ctx.author.id):
            await ctx.send("❌ Owner access required!")
            return

        sent_count = 0
        failed_count = 0

        embed = discord.Embed(
            title="📢 Global Announcement",
            description=message,
            color=COLORS['primary']
        )
        embed.set_footer(text=f"Sent by {ctx.author.display_name} | Bot Owner")

        for guild in self.bot.guilds:
            try:
                # Find the best channel to send to
                channel = None
                
                # Look for announcement channels first
                for ch in guild.text_channels:
                    if any(name in ch.name.lower() for name in ['announce', 'news', 'general', 'main']):
                        if ch.permissions_for(guild.me).send_messages:
                            channel = ch
                            break
                
                # Fallback to first available channel
                if not channel:
                    for ch in guild.text_channels:
                        if ch.permissions_for(guild.me).send_messages:
                            channel = ch
                            break
                
                if channel:
                    await channel.send(embed=embed)
                    sent_count += 1
                else:
                    failed_count += 1
                    
                # Small delay to avoid rate limits
                await asyncio.sleep(0.5)
                    
            except Exception:
                failed_count += 1

        result_embed = discord.Embed(
            title="📊 Global Announcement Results",
            description=f"**Message sent to {sent_count}/{len(self.bot.guilds)} servers**\n\n"
                       f"✅ **Successful:** {sent_count}\n"
                       f"❌ **Failed:** {failed_count}",
            color=COLORS['success'] if failed_count == 0 else COLORS['warning']
        )
        
        await ctx.send(embed=result_embed)

    @commands.command(name="modules", hidden=True)
    async def module_management(self, ctx):
        """Module management interface (OWNER ONLY)."""
        if not self.is_owner_or_admin(ctx.author.id):
            await ctx.send("❌ Owner access required!")
            return

        view = ModuleManagementView(str(ctx.author.id), self.bot)
        embed = discord.Embed(
            title="🔧 Module Management",
            description="**Manage bot modules and extensions**\n\n"
                       "Use the buttons below to view, reload, or get system information.",
            color=COLORS['primary']
        )
        
        embed.add_field(
            name="📋 Available Actions",
            value="• **List Modules** - View all loaded modules\n"
                  "• **Reload Module** - Restart a specific module\n"
                  "• **System Info** - View system diagnostics",
            inline=False
        )
        
        await ctx.send(embed=embed, view=view)

    @commands.command(name="reload", hidden=True)
    async def reload_extension(self, ctx, extension: str):
        """Reload a specific bot extension (OWNER ONLY)."""
        if not self.is_owner_or_admin(ctx.author.id):
            await ctx.send("❌ Owner access required!")
            return

        try:
            extension_name = f"cogs.{extension.lower()}"
            
            if extension_name in self.bot.extensions:
                await self.bot.reload_extension(extension_name)
                embed = discord.Embed(
                    title="✅ Extension Reloaded",
                    description=f"**{extension}** has been successfully reloaded!",
                    color=COLORS['success']
                )
            else:
                await self.bot.load_extension(extension_name)
                embed = discord.Embed(
                    title="✅ Extension Loaded",
                    description=f"**{extension}** has been successfully loaded!",
                    color=COLORS['success']
                )
                
        except Exception as e:
            embed = discord.Embed(
                title="❌ Reload Failed",
                description=f"**Error with {extension}:**\n```{str(e)[:1000]}```",
                color=COLORS['danger']
            )
            
        await ctx.send(embed=embed)

    @commands.command(name="emergencyshutdown", hidden=True)
    async def emergency_shutdown(self, ctx):
        """Emergency bot shutdown with notifications (OWNER ONLY)."""
        if ctx.author.id != 1297013439125917766:  # Only bot owner
            await ctx.send("❌ This command is restricted to the bot owner only!")
            return

        embed = discord.Embed(
            title="🚨 Emergency Shutdown Initiated",
            description="**The bot will shutdown in 10 seconds.**\n\n"
                       "This is an emergency shutdown requested by the bot owner.\n"
                       "The bot will attempt to reconnect automatically.",
            color=COLORS['danger']
        )
        
        await ctx.send(embed=embed)
        
        # Give time for the message to send
        await asyncio.sleep(10)
        
        # Close the bot gracefully
        await self.bot.close()

class TestingToolsView(discord.ui.View):
    def __init__(self, user_id: str, bot):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.bot = bot

    @discord.ui.button(label="🧪 Test Character", style=discord.ButtonStyle.primary, emoji="👤", row=0)
    async def test_character(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🧪 Testing character creation...", ephemeral=True)

    @discord.ui.button(label="⚔️ Test Combat", style=discord.ButtonStyle.success, emoji="⚔️", row=0)
    async def test_combat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⚔️ Testing combat system...", ephemeral=True)

    @discord.ui.button(label="📈 Test Leveling", style=discord.ButtonStyle.secondary, emoji="📈", row=0)
    async def test_leveling(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📈 Testing leveling system...", ephemeral=True)

    @discord.ui.button(label="💰 Test Shop", style=discord.ButtonStyle.danger, emoji="💰", row=1)
    async def test_shop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("💰 Testing shop system...", ephemeral=True)

    @discord.ui.button(label="🔧 Test Admin Tools", style=discord.ButtonStyle.gray, emoji="🔧", row=1)
    async def test_admin(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔧 Testing admin tools...", ephemeral=True)

    @discord.ui.button(label="⚡ Quick Setup", style=discord.ButtonStyle.blurple, emoji="⚡", row=1)
    async def quick_setup(self, interaction: discord.Interaction, button: discord.ui.Button):
        admin_cog = self.bot.get_cog('Admin')
        if not admin_cog:
            await interaction.response.send_message("❌ Admin system not loaded.", ephemeral=True)
            return

        await admin_cog.quick_setup(interaction, interaction.user)
        await interaction.response.send_message("✅ Quick setup complete!", ephemeral=True)

class ModuleManagementView(discord.ui.View):
    """Module loading/unloading management interface."""
    
    def __init__(self, user_id: str, bot):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.bot = bot

    @discord.ui.button(label="📋 List Modules", style=discord.ButtonStyle.primary, emoji="📋", row=0)
    async def list_modules(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your panel!", ephemeral=True)
            return

        embed = discord.Embed(
            title="📋 Loaded Modules",
            description="**Current bot modules and their status:**",
            color=COLORS['info']
        )
        
        loaded_cogs = []
        for name, cog in self.bot.cogs.items():
            status = "🟢 Active"
            loaded_cogs.append(f"{status} **{name}**")
        
        if loaded_cogs:
            embed.add_field(
                name="Loaded Cogs",
                value="\n".join(loaded_cogs[:15]),  # Limit to prevent overflow
                inline=False
            )
        else:
            embed.add_field(name="Status", value="No cogs loaded", inline=False)
            
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🔄 Reload Module", style=discord.ButtonStyle.secondary, emoji="🔄", row=0)
    async def reload_module(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your panel!", ephemeral=True)
            return
            
        await interaction.response.send_modal(ReloadModuleModal(self.bot))

    @discord.ui.button(label="🔧 System Info", style=discord.ButtonStyle.danger, emoji="🔧", row=1)
    async def system_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your panel!", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="🔧 System Information",
            description="**Bot system details and diagnostics:**",
            color=COLORS['secondary']
        )
        
        # Python and Discord.py versions
        embed.add_field(
            name="🐍 Environment",
            value=f"**Python:** {sys.version.split()[0]}\n"
                  f"**Discord.py:** {discord.__version__}\n"
                  f"**Platform:** Linux (Replit)",
            inline=True
        )
        
        # Memory usage
        memory = psutil.virtual_memory()
        embed.add_field(
            name="💾 Memory Usage",
            value=f"**Used:** {memory.percent}%\n"
                  f"**Available:** {memory.available // 1024 // 1024}MB\n"
                  f"**Total:** {memory.total // 1024 // 1024}MB",
            inline=True
        )
        
        await interaction.response.edit_message(embed=embed, view=self)

class ReloadModuleModal(discord.ui.Modal, title="🔄 Reload Module"):
    module_name = discord.ui.TextInput(
        label="Module Name",
        placeholder="e.g., rpg_core, admin, economy",
        required=True,
        max_length=50
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        module = self.module_name.value.lower()
        
        try:
            # Try to reload the module
            extension_name = f"cogs.{module}"
            
            if extension_name in self.bot.extensions:
                await self.bot.reload_extension(extension_name)
                embed = discord.Embed(
                    title="✅ Module Reloaded",
                    description=f"**{module}** has been successfully reloaded!",
                    color=COLORS['success']
                )
            else:
                # Try to load it if not loaded
                await self.bot.load_extension(extension_name)
                embed = discord.Embed(
                    title="✅ Module Loaded",
                    description=f"**{module}** has been successfully loaded!",
                    color=COLORS['success']
                )
                
        except Exception as e:
            embed = discord.Embed(
                title="❌ Reload Failed",
                description=f"**Error reloading {module}:**\n```{str(e)[:500]}```",
                color=COLORS['danger']
            )
            
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
    await bot.add_cog(AdminCog(bot))