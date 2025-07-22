import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

from config import COLORS, EMOJIS, is_module_enabled
from utils.database import get_user_data, update_user_data, ensure_user_exists
from utils.helpers import create_embed, format_number
from rpg_data.game_data import CLASSES, PATHS, ITEMS, RARITY_COLORS
from utils.warning_system import warning_system

logger = logging.getLogger(__name__)

class StartRPGView(discord.ui.View):
    """Button to initiate the RPG start process."""

    def __init__(self):
        super().__init__(timeout=None)  # Persistent view

    @discord.ui.button(label="✨ Start Your Adventure", style=discord.ButtonStyle.success, custom_id="start_rpg_adventure")
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        rpg_core = self.get_rpg_core(interaction.client)
        if not rpg_core:
            await interaction.response.send_message("❌ RPG module not found.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=False)  # Acknowledge and defer

        user_id = str(interaction.user.id)
        ensure_user_exists(user_id)

        # Check if user already has a character
        player_data = rpg_core.get_player_data(user_id)
        if player_data:
            embed = discord.Embed(
                title="🎮 Adventure Already Started!",
                description=f"Welcome back, {interaction.user.mention}! Your adventure continues...\n\n"
                           f"**Current Character:**\n"
                           f"• **Class:** {CLASSES[player_data['class']]['name']}\n"
                           f"• **Level:** {player_data['level']}\n"
                           f"• **Gold:** {format_number(player_data['gold'])}\n"
                           f"• **HP:** {player_data['resources']['hp']}/{player_data['resources']['max_hp']}\n\n"
                           f"Use `$profile` to view your full character sheet!",
                color=COLORS['info']
            )
            await interaction.followup.send(embed=embed)
            return

        # Create character creation embed
        embed = discord.Embed(
            title="🎭 Begin Your RPG Adventure",
            description="**Welcome to Project: Blood & Cheese!**\n\n"
                       "Choose your character class to start your epic journey!",
            color=COLORS['primary']
        )

        view = ClassSelectionView(user_id, rpg_core)
        await interaction.followup.send(embed=embed, view=view)

    def get_rpg_core(self, bot):
        """Helper to get the RPGCore cog."""
        return bot.get_cog("RPGCore")

class ClassSelectionView(discord.ui.View):
    """Interactive class selection for new characters."""

    def __init__(self, user_id: str, rpg_core):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.rpg_core = rpg_core

    @discord.ui.select(
        placeholder="🎭 Choose your character class...",
        options=[
            discord.SelectOption(
                label="🛡️ Warrior",
                value="warrior",
                description="Tank • High defense and protective abilities",
                emoji="🛡️"
            ),
            discord.SelectOption(
                label="🔮 Mage", 
                value="mage",
                description="DPS • Magical damage with area effects",
                emoji="🔮"
            ),
            discord.SelectOption(
                label="🗡️ Rogue",
                value="rogue", 
                description="DPS • High critical hits and stealth",
                emoji="🗡️"
            ),
            discord.SelectOption(
                label="🏹 Archer",
                value="archer",
                description="DPS • Ranged precision striker",
                emoji="🏹"
            ),
            discord.SelectOption(
                label="❤️ Healer",
                value="healer",
                description="Support • Healing and team buffs",
                emoji="❤️"
            ),
            discord.SelectOption(
                label="⚔️ Battlemage",
                value="battlemage",
                description="Hybrid • Melee and magic fighter",
                emoji="⚔️"
            ),
            discord.SelectOption(
                label="⏰ Chrono Knight",
                value="chrono_knight",
                description="Hidden • Time manipulation specialist",
                emoji="⏰"
            )
        ]
    )
    async def class_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your character creation!", ephemeral=True)
            return

        selected_class = select.values[0]
        class_data = CLASSES[selected_class]

        # Create new character data
        new_character = {
            'level': 1,
            'xp': 0,
            'gold': 1000,
            'class': selected_class,
            'path': None,
            'name': interaction.user.display_name,
            'stats': {
                'strength': class_data['starting_stats']['strength'],
                'dexterity': class_data['starting_stats']['dexterity'],
                'constitution': class_data['starting_stats']['constitution'],
                'intelligence': class_data['starting_stats']['intelligence'],
                'wisdom': class_data['starting_stats']['wisdom'],
                'charisma': class_data['starting_stats']['charisma']
            },
            'resources': {
                'hp': class_data['base_hp'],
                'max_hp': class_data['base_hp'],
                'mana': class_data['base_mp'],
                'max_mana': class_data['base_mp'],
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
                'attack': 10 + class_data['starting_stats']['strength'] * 2,
                'magic_attack': 10 + class_data['starting_stats']['intelligence'] * 2,
                'defense': 5 + class_data['starting_stats']['constitution'],
                'critical_chance': 0.05 + (class_data['starting_stats']['dexterity'] * 0.01),
                'dodge_chance': class_data['starting_stats']['dexterity'] * 0.005,
                'max_ultimate_energy': 100
            },
            'unallocated_points': 0,
            'equipment': {
                'weapon': None,
                'armor': None,
                'accessory': None,
                'artifact': None
            },
            'inventory': {
                'health_potion': 5,
                'mana_potion': 3
            },
            'skills': class_data['starting_skills'].copy(),
            'techniques': ['ambush'],
            'achievements': [],
            'arena_rating': 1000,
            'arena_wins': 0,
            'arena_losses': 0,
            'arena_tokens': 0,
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

        # Save character data
        user_data = get_user_data(self.user_id) or {}
        user_data['rpg_data'] = new_character
        update_user_data(self.user_id, user_data)

        embed = discord.Embed(
            title="🎉 Character Created Successfully!",
            description=f"Welcome to your adventure as a **{class_data['name']}**!\n\n"
                       f"**{class_data['description']}**\n\n"
                       f"**Role:** {class_data['role']}\n"
                       f"**Starting Resources:**\n"
                       f"• Level 1 • 1,000 Gold\n"
                       f"• {class_data['base_hp']} HP • {class_data['base_mp']} MP\n"
                       f"• 5 Health Potions • 3 Mana Potions\n\n"
                       f"**Next Steps:**\n"
                       f"• Use `$profile` to view your character\n"
                       f"• Use `$battle` to start combat\n"
                       f"• Use `$help` for all commands",
            color=COLORS['success']
        )

        await interaction.response.edit_message(embed=embed, view=None)

class StatAllocationView(discord.ui.View):
    """Interactive stat allocation interface."""

    def __init__(self, user_id: str, rpg_core):
        super().__init__(timeout=180)
        self.user_id = str(user_id)
        self.rpg_core = rpg_core

    def create_allocation_embed(self, player_data):
        """Create the stat allocation embed."""
        embed = discord.Embed(
            title="📊 Stat Allocation",
            description=f"**Available Points:** {player_data.get('unallocated_points', 0)}\n\n"
                       "Use the buttons below to allocate your stat points:",
            color=COLORS['primary']
        )

        stats = player_data['stats']
        embed.add_field(
            name="Current Stats",
            value=f"**STR:** {stats['strength']}\n"
                  f"**DEX:** {stats['dexterity']}\n"
                  f"**CON:** {stats['constitution']}\n"
                  f"**INT:** {stats['intelligence']}\n"
                  f"**WIS:** {stats['wisdom']}\n"
                  f"**CHA:** {stats['charisma']}",
            inline=True
        )

        embed.add_field(
            name="Stat Benefits",
            value="**STR** - Physical damage\n"
                  "**DEX** - Critical hits, dodge\n"
                  "**CON** - Health points\n"
                  "**INT** - Magical damage\n"
                  "**WIS** - Mana points\n"
                  "**CHA** - Social interactions",
            inline=True
        )

        return embed

    @discord.ui.select(
        placeholder="Choose stat to allocate (+1 point)",
        options=[
            discord.SelectOption(label="💪 Strength", value="strength", description="Increases physical damage"),
            discord.SelectOption(label="🎯 Dexterity", value="dexterity", description="Increases critical hit chance"),
            discord.SelectOption(label="❤️ Constitution", value="constitution", description="Increases health points"),
            discord.SelectOption(label="🧠 Intelligence", value="intelligence", description="Increases magical damage"),
            discord.SelectOption(label="🔮 Wisdom", value="wisdom", description="Increases mana points"),
            discord.SelectOption(label="✨ Charisma", value="charisma", description="Increases social effectiveness")
        ]
    )
    async def stat_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your allocation!", ephemeral=True)
            return

        stat = select.values[0]
        player_data = self.rpg_core.get_player_data(interaction.user.id)

        if not player_data:
            await interaction.response.send_message("❌ Player data not found!", ephemeral=True)
            return

        if player_data.get('unallocated_points', 0) <= 0:
            await interaction.response.send_message("❌ No stat points available!", ephemeral=True)
            return

        # Allocate the point
        player_data['stats'][stat] += 1
        player_data['unallocated_points'] -= 1

        # Update derived stats
        self.update_derived_stats(player_data)
        self.rpg_core.save_player_data(interaction.user.id, player_data)

        embed = self.create_allocation_embed(player_data)
        embed.add_field(
            name="✅ Point Allocated",
            value=f"Added 1 point to **{stat.title()}**!",
            inline=False
        )

        await interaction.response.edit_message(embed=embed, view=self)

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

class CombatEscapeView(discord.ui.View):
    """View to handle combat escape options."""

    def __init__(self, user_id: str, rpg_core):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.rpg_core = rpg_core

    @discord.ui.button(label="🏃 Force Exit Combat", style=discord.ButtonStyle.danger)
    async def force_exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your combat!", ephemeral=True)
            return

        player_data = self.rpg_core.get_player_data(self.user_id)
        if player_data:
            player_data['in_combat'] = False
            player_data['resources']['ultimate_energy'] = 0
            # Small penalty for force exiting
            gold_lost = max(1, int(player_data.get('gold', 0) * 0.05))
            player_data['gold'] = max(0, player_data.get('gold', 0) - gold_lost)

            self.rpg_core.save_player_data(self.user_id, player_data)

            embed = discord.Embed(
                title="🏃 Forced Exit from Combat",
                description=f"You forcefully escaped from combat!\n\n"
                           f"**Penalty:** Lost {gold_lost} gold for fleeing.\n"
                           f"You can now use other RPG commands.",
                color=COLORS['warning']
            )
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.send_message("❌ Player data not found!", ephemeral=True)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_action(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your action!", ephemeral=True)
            return

        embed = discord.Embed(
            title="✅ Action Cancelled",
            description="Combat status unchanged. Finish your current battle to continue.",
            color=COLORS['secondary']
        )
        await interaction.response.edit_message(embed=embed, view=None)

class ProfileActionView(discord.ui.View):
    """Buttons for profile-related actions."""

    def __init__(self, target_id: str, requester_id: str):
        super().__init__(timeout=180)
        self.target_id = str(target_id)
        self.requester_id = str(requester_id)

    @discord.ui.button(label="📊 Allocate Stats", style=discord.ButtonStyle.primary, emoji="📊")
    async def allocate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.requester_id:
            await interaction.response.send_message("❌ This isn't your profile!", ephemeral=True)
            return

        # Get updated player data
        player_data = self.get_rpg_core(interaction.client).get_player_data(interaction.user.id)
        if not player_data:
            await interaction.response.send_message("❌ Player data not found!", ephemeral=True)
            return

        if player_data.get('unallocated_points', 0) <= 0:
            await interaction.response.send_message("❌ You don't have any stat points to allocate!", ephemeral=True)
            return

        view = StatAllocationView(str(interaction.user.id), self.get_rpg_core(interaction.client))
        embed = view.create_allocation_embed(player_data)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="🎒 View Inventory", style=discord.ButtonStyle.secondary, emoji="🎒")
    async def inventory_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.requester_id:
            await interaction.response.send_message("❌ This isn't your profile!", ephemeral=True)
            return

        # Get updated player data
        rpg_core = self.get_rpg_core(interaction.client)
        player_data = rpg_core.get_player_data(interaction.user.id)
        if not player_data:
            await interaction.response.send_message("❌ Player data not found!", ephemeral=True)
            return

        from cogs.rpg_items import InventoryView
        view = InventoryView(player_data, rpg_core, str(interaction.user.id))
        embed = view.create_inventory_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    def get_rpg_core(self, bot):
        """Helper to get the RPGCore cog."""
        return bot.get_cog("RPGCore")

class RPGCore(commands.Cog):
    """Core RPG functionality with proper data management."""

    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(StartRPGView())

    def get_player_data(self, user_id):
        """Get player RPG data safely."""
        user_data = get_user_data(str(user_id))
        if user_data and 'rpg_data' in user_data:
            player_data = user_data['rpg_data']

            # Safety check: ensure resources exist
            if 'resources' not in player_data:
                player_data['resources'] = {
                    'hp': 100,
                    'max_hp': 100,
                    'mana': 50,
                    'max_mana': 50,
                    'stamina': 100,
                    'max_stamina': 100,
                    'sp': 100,
                    'max_sp': 100,
                    'miraculous_energy': 100,
                    'max_miraculous_energy': 100,
                    'ultimate_energy': 0,
                    'technique_points': 3
                }
                self.save_player_data(user_id, player_data)

            # Ensure SP exists (for existing characters)
            if 'sp' not in player_data['resources']:
                player_data['resources']['sp'] = 100
                player_data['resources']['max_sp'] = 100
                self.save_player_data(user_id, player_data)

            return player_data
        return None

    def save_player_data(self, user_id, player_data):
        """Save player RPG data safely."""
        user_data = get_user_data(str(user_id)) or {}
        user_data['rpg_data'] = player_data
        update_user_data(str(user_id), user_data)

    def level_up_check(self, player_data):
        """Check and process level ups."""
        current_level = player_data['level']
        current_xp = player_data['xp']

        levels_gained = 0
        while current_xp >= self.calculate_level_xp_requirement(current_level + 1):
            current_level += 1
            levels_gained += 1

            # Give stat points (3 per level)
            player_data['unallocated_points'] = player_data.get('unallocated_points', 0) + 3

            # Update base stats slightly on level up
            stats = player_data['stats']
            stats['strength'] += 1
            stats['constitution'] += 1

            # Update derived stats
            self.update_derived_stats(player_data)

            # Heal on level up
            player_data['resources']['hp'] = player_data['resources']['max_hp']
            player_data['resources']['mana'] = player_data['resources']['max_mana']

        player_data['level'] = current_level
        return levels_gained
    
    def calculate_level_rewards(self, old_level, new_level):
        """Calculate rewards for leveling up."""
        level_diff = new_level - old_level

        rewards = {
            'stat_points': level_diff * 2,  # 2 points per level
            'gold': level_diff * 100,       # 100 gold per level
            'skill_points': 0
        }

        # Every 5 levels, get a skill point
        for level in range(old_level + 1, new_level + 1):
            if level % 5 == 0:
                rewards['skill_points'] += 1

        return rewards

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

    def calculate_level_xp_requirement(self, level):
        """Calculate XP needed for a level."""
        return int(100 * (level ** 1.5))

    def is_player_in_combat(self, user_id):
        """Check if player is currently in combat."""
        player_data = self.get_player_data(user_id)
        if not player_data:
            return False
        return player_data.get('in_combat', False)

    @commands.command(name="startrpg", aliases=["start", "begin", "create", "newchar"])
    async def start_rpg(self, ctx):
        """Start your RPG adventure with interactive class selection."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        user_id = str(ctx.author.id)
        ensure_user_exists(user_id)

        # Check if player is in combat first
        if self.is_player_in_combat(user_id):
            embed = discord.Embed(
                title="⚔️ Already Fighting!",
                description="You're currently in combat! Finish your current battle first.",
                color=COLORS['warning']
            )
            view = CombatEscapeView(user_id, self)
            await ctx.send(embed=embed, view=view)
            return

        # Check if user already has a character
        player_data = self.get_player_data(user_id)
        if player_data:
            embed = discord.Embed(
                title="🎮 Adventure Already Started!",
                description=f"Welcome back, {ctx.author.mention}! Your adventure continues...\n\n"
                           f"**Current Character:**\n"
                           f"• **Class:** {CLASSES[player_data['class']]['name']}\n"
                           f"• **Level:** {player_data['level']}\n"
                           f"• **Gold:** {format_number(player_data['gold'])}\n"
                           f"• **HP:** {player_data['resources']['hp']}/{player_data['resources']['max_hp']}\n\n"
                           f"Use `$profile` to view your full character sheet!",
                color=COLORS['info']
            )
            await ctx.send(embed=embed)
            return

        # Create character creation embed
        embed = discord.Embed(
            title="🎭 Begin Your RPG Adventure",
            description="**Welcome to Project: Blood & Cheese!**\n\n"
                       "Choose your character class to start your epic journey!",
            color=COLORS['primary']
        )

        view = ClassSelectionView(user_id, self)
        await ctx.send(embed=embed, view=view)

    @commands.command(name="profile", aliases=["prof", "me", "stats", "char", "character"])
    async def profile(self, ctx, member: discord.Member = None):
        """View character profile and stats."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        target = member or ctx.author
        player_data = self.get_player_data(target.id)

        if not player_data:
            if target == ctx.author:
                embed = discord.Embed(
                    title="🎮 No Character Found",
                    description="You need to create a character before you can view your profile!",
                    color=COLORS['info']
                )
                embed.add_field(
                    name="🌟 Getting Started",
                    value="Click the button below to create your character and begin your journey!",
                    inline=False
                )

                view = StartRPGView()
                await ctx.send(embed=embed, view=view)
            else:
                embed = create_embed("No Character", f"{target.display_name} hasn't started their RPG journey!", COLORS['error'])
                await ctx.send(embed=embed)
            return

        # Check for progression warnings
        progression_warning = warning_system.check_progression_warning(player_data, "level_check")

        # Create profile embed
        embed = discord.Embed(
            title=f"🎮 {target.display_name}'s Profile",
            color=COLORS['primary']
        )

        # Basic info
        embed.add_field(
            name="📊 Basic Info",
            value=f"**Class:** {CLASSES.get(player_data['class'], {}).get('name', player_data['class'].title())}\n"
                  f"**Level:** {player_data['level']}\n"
                  f"**XP:** {format_number(player_data['xp'])}\n"
                  f"**Gold:** {format_number(player_data['gold'])}",
            inline=True
        )

        # Resources
        resources = player_data['resources']
        embed.add_field(
            name="❤️ Resources",
            value=f"**HP:** {resources['hp']}/{resources['max_hp']}\n"
                  f"**MP:** {resources['mana']}/{resources['max_mana']}\n"
                  f"**SP:** {resources.get('sp', 100)}/{resources.get('max_sp', 100)}\n"
                  f"**Energy:** {resources['miraculous_energy']}/{resources['max_miraculous_energy']}",
            inline=True
        )

        # Stats
        stats = player_data['stats']
        embed.add_field(
            name="⚔️ Stats",
            value=f"**STR:** {stats['strength']}\n"
                  f"**DEX:** {stats['dexterity']}\n"
                  f"**CON:** {stats['constitution']}\n"
                  f"**INT:** {stats['intelligence']}\n"
                  f"**WIS:** {stats['wisdom']}\n"
                  f"**CHA:** {stats['charisma']}",
            inline=True
        )

        # Combat stats
        derived = player_data['derived_stats']
        embed.add_field(
            name="⚔️ Combat Stats",
            value=f"**Attack:** {derived['attack']}\n"
                  f"**Magic Attack:** {derived['magic_attack']}\n"
                  f"**Defense:** {derived['defense']}\n"
                  f"**Crit Chance:** {int(derived['critical_chance']*100)}%",
            inline=True
        )

        # PvP info
        embed.add_field(
            name="🏆 PvP Record",
            value=f"**Rating:** {player_data['arena_rating']}\n"
                  f"**Wins:** {player_data['arena_wins']}\n"
                  f"**Losses:** {player_data['arena_losses']}\n"
                  f"**Tokens:** {player_data['arena_tokens']}",
            inline=True
        )

        # Path info if available
        if player_data.get('chosen_path'):
            path_data = PATHS.get(player_data['chosen_path'], {})
            embed.add_field(
                name="🌟 Miraculous Path",
                value=f"**{path_data.get('name', 'Unknown')}**\n"
                      f"{path_data.get('description', 'No description')}",
                inline=False
            )

        embed.set_thumbnail(url=target.display_avatar.url)

        # Calculate last active time
        last_active_times = [player_data.get('last_hunt', 0),
                             player_data.get('last_adventure', 0),
                             player_data.get('last_explore', 0),
                             player_data.get('last_work', 0)]
        last_active = max(last_active_times) if last_active_times else 0
        if isinstance(last_active, (int, float)):
            last_active = datetime.now() - timedelta(seconds=last_active)
            last_active = last_active.strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_active = "N/A"

        embed.set_footer(text=f"⏰ Last Active: {last_active}")

        # Add progression warning if exists
        if progression_warning and target == ctx.author:
            embed.add_field(
                name="💡 Helpful Suggestion",
                value=progression_warning['warnings'][0]['message'],
                inline=False
            )

        view = ProfileActionView(target.id, ctx.author.id) if target == ctx.author else None
        await ctx.send(embed=embed, view=view)

    @commands.command(name="inventory", aliases=["inv"])
    async def inventory(self, ctx, category: str = None):
        """View your inventory with interactive interface."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        player_data = self.get_player_data(ctx.author.id)
        if not player_data:
            # Auto-start tutorial for new players
            embed = discord.Embed(
                title="🎮 Welcome to Project: Blood & Cheese!",
                description="You need to create a character first! Let's start with the interactive tutorial to get you started.",
                color=COLORS['info']
            )

            from cogs.help import TutorialView
            view = TutorialView(self.bot, "$")
            await ctx.send(embed=embed, view=view)
            return

        # Use the new interactive inventory system
        from cogs.rpg_inventory import InventoryView
        view = InventoryView(ctx.author.id, self)
        if not view.player_data:
            await ctx.send("❌ Error loading player data.")
            return

        embed = view.create_main_inventory_embed()
        await ctx.send(embed=embed, view=view)

    @commands.command(name="combatstatus", aliases=["cs"])
    async def combat_status(self, ctx):
        """Check your current combat status."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        player_data = self.get_player_data(ctx.author.id)
        if not player_data:
            embed = create_embed("No Character", "Use `$startrpg` first!", COLORS['error'])
            await ctx.send(embed=embed)
            return

        in_combat = player_data.get('in_combat', False)

        if in_combat:
            embed = discord.Embed(
                title="⚔️ Combat Status",
                description="You are currently **IN COMBAT**.",
                color=COLORS['error']
            )
            embed.add_field(
                name="Options",
                value="• Wait for combat to end naturally\n• Use the Force Exit button if needed",
                inline=False
            )
            view = CombatEscapeView(str(ctx.author.id), self)
            await ctx.send(embed=embed, view=view)
        else:
            embed = discord.Embed(
                title="✅ Combat Status",
                description="You are **NOT IN COMBAT**.\nFree to use all RPG commands!",
                color=COLORS['success']
            )
            await ctx.send(embed=embed)

    @commands.command(name="allocate", aliases=["alloc"])
    async def allocate_stats(self, ctx, stat: str, points: int = 1):
        """Allocate stat points to improve your character."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        player_data = self.get_player_data(ctx.author.id)
        if not player_data:
            embed = discord.Embed(
                title="🎮 No Character Found",
                description="You need to create a character before you can allocate stats!",
                color=COLORS['info']
            )
            embed.add_field(
                name="🌟 Getting Started",
                value="Click the button below to create your character and begin your journey!",
                inline=False
            )

            view = StartRPGView()
            await ctx.send(embed=embed, view=view)
            return

        # Validate stat name
        valid_stats = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
        if stat.lower() not in valid_stats:
            embed = create_embed("Invalid Stat", f"Valid stats: {', '.join(valid_stats)}", COLORS['error'])
            await ctx.send(embed=embed)
            return

        # Check for stat allocation warnings
        warning_result = warning_system.check_stat_allocation_warning(player_data, stat.lower(), points)
        if warning_result and warning_result['severity'] in ['error']:
            # Block if it's an error-level warning
            await ctx.send(embed=warning_result['embed'])
            return
        elif warning_result:
            # Show warning but allow continuation
            warning_embed = warning_result['embed']
            warning_embed.add_field(
                name="⚡ Continue Anyway?",
                value="React with ✅ to proceed or ❌ to cancel.",
                inline=False
            )

            warning_msg = await ctx.send(embed=warning_embed)
            await warning_msg.add_reaction("✅")
            await warning_msg.add_reaction("❌")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message == warning_msg

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                if str(reaction.emoji) == "❌":
                    await warning_msg.edit(embed=create_embed("Cancelled", "Stat allocation cancelled.", COLORS['secondary']))
                    return
                await warning_msg.delete()
            except asyncio.TimeoutError:
                await warning_msg.edit(embed=create_embed("Timeout", "Stat allocation cancelled due to timeout.", COLORS['secondary']))
                return

        # Check available points
        if player_data['unallocated_points'] < points:
            embed = create_embed("Not Enough Points", f"You only have {player_data['unallocated_points']} unallocated points.", COLORS['error'])
            await ctx.send(embed=embed)
            return

        # Allocate stat points
        player_data['stats'][stat.lower()] += points
        player_data['unallocated_points'] -= points

        # Update derived stats
        self.update_derived_stats(player_data)

        self.save_player_data(ctx.author.id, player_data)

        embed = create_embed("Stats Allocated", f"Successfully allocated {points} points to {stat.title()}.", COLORS['success'])
        await ctx.send(embed=embed)

    @commands.command(name="forceexit", aliases=["forcexit", "emergencyexit"])
    async def force_exit_combat(self, ctx):
        """Force exit combat with heavy penalties (emergency use only)."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        player_data = self.get_player_data(str(ctx.author.id))
        if not player_data:
            await ctx.send("❌ You don't have a character!")
            return

        if not player_data.get('in_combat', False):
            await ctx.send("❌ You're not in combat!")
            return

        # Show warning confirmation
        embed = discord.Embed(
            title="⚠️ EMERGENCY COMBAT EXIT",
            description="*\"You want to break out of combat? This is going to hurt... your wallet and your pride.\"*\n\n"
                       "**⚠️ WARNING: This will apply HEAVY penalties:**\n"
                       "• Lose 30% of your gold\n"
                       "• Reduce HP to 1\n"
                       "• Reset ultimate energy to 0\n"
                       "• Mark as combat deserter\n\n"
                       "**Use only if:**\n"
                       "• Combat is genuinely stuck/broken\n"
                       "• Buttons aren't responding\n"
                       "• Emergency situation\n\n"
                       "**This is NOT for normal fleeing!** Use the flee button in combat instead.",
            color=COLORS['error']
        )

        view = ForceExitConfirmView(str(ctx.author.id), self)
        await ctx.send(embed=embed, view=view)

class ForceExitConfirmView(discord.ui.View):
    """Confirmation view for force exit with warnings."""

    def __init__(self, user_id, rpg_core):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.rpg_core = rpg_core

    @discord.ui.button(label="💀 CONFIRM FORCE EXIT", style=discord.ButtonStyle.danger, emoji="💀")
    async def confirm_exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != int(self.user_id):
            await interaction.response.send_message("Not your choice!", ephemeral=True)
            return

        # Apply heavy penalties
        player_data = self.rpg_core.get_player_data(self.user_id)
        if not player_data:
            await interaction.response.send_message("❌ Player data not found!", ephemeral=True)
            return

        # Calculate penalties
        gold_lost = max(10, int(player_data.get('gold', 0) * 0.30))
        player_data['gold'] = max(0, player_data.get('gold', 0) - gold_lost)
        player_data['resources']['hp'] = 1
        player_data['resources']['ultimate_energy'] = 0
        player_data['in_combat'] = False

        # Track force exits for potential abuse
        stats = player_data.get('stats', {})
        stats['force_exits'] = stats.get('force_exits', 0) + 1
        player_data['stats'] = stats

        # Save changes
        self.rpg_core.save_player_data(self.user_id, player_data)

        # Clear combat tracking
        from cogs.rpg_combat import active_combats
        for channel_id, user_id in list(active_combats.items()):
            if user_id == int(self.user_id):
                del active_combats[channel_id]
                break

        embed = discord.Embed(
            title="💀 Force Exit Applied",
            description=f"*\"There, I broke you out. Hope it was worth it because it cost you {format_number(gold_lost)} gold, "
                       f"all your health, and your ultimate energy. Try not to get stuck next time!\"*\n\n"
                       f"**Penalties Applied:**\n"
                       f"• Lost {format_number(gold_lost)} gold\n"
                       f"• HP reduced to 1/{player_data['resources']['max_hp']}\n"
                       f"• Ultimate energy reset to 0\n"
                       f"• Force exits: {stats['force_exits']}\n\n"
                       f"*Use `$heal` or rest to recover.*",
            color=COLORS['error']
        )

        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌")
    async def cancel_exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != int(self.user_id):
            await interaction.response.send_message("Not your choice!", ephemeral=True)
            return

        embed = discord.Embed(
            title="✅ Force Exit Cancelled",
            description="*\"Smart choice. Now go back to your battle and try to win properly this time.\"*\n\n"
                       "**Alternative options:**\n"
                       "• Use the 🏃 **Flee** button in combat for normal escape\n"
                       "• Try refreshing Discord if buttons aren't working\n"
                       "• Ask for help in support if combat is genuinely broken",
            color=COLORS['success']
        )

        await interaction.response.edit_message(embed=embed, view=None)

    @commands.command(name="superitems", aliases=["legendary_items", "op_items"])
    async def super_items(self, ctx):
        """View the 10 super OP items and their requirements."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        player_data = self.get_player_data(ctx.author.id)
        if not player_data:
            embed = discord.Embed(
                title="🎮 No Character Found",
                description="You need to create a character first!",
                color=COLORS['info']
            )
            view = StartRPGView()
            await ctx.send(embed=embed, view=view)
            return

        from rpg_data.game_data import SUPER_OP_ITEMS, ACHIEVEMENT_REQUIREMENTS

        embed = discord.Embed(
            title="⭐ The 10 Legendary Super Items",
            description="**These are the most powerful items in existence!**\n\n"
                       "*Each item requires completing an extremely difficult achievement.*\n"
                       "*Only the most dedicated warriors can obtain these legendary artifacts.*",
            color=COLORS['legendary']
        )

        unlocked_count = 0

        for item_key, item_data in SUPER_OP_ITEMS.items():
            achievement_req = item_data.get('achievement_req')

            # Check if player has the required achievement
            player_achievements = player_data.get('achievements', [])
            has_achievement = achievement_req in player_achievements
            unlocked_count += 1 if has_achievement else 0

            # Get achievement info
            achievement_info = ACHIEVEMENT_REQUIREMENTS.get(achievement_req, {})
            achievement_name = achievement_info.get('name', achievement_req)
            achievement_desc = achievement_info.get('description', 'No description available')

            # Create item display
            status_emoji = "✅" if has_achievement else "🔒"
            rarity_emoji = "🌟"  # All super items are cosmic

            item_display = f"{status_emoji} {rarity_emoji} **{item_data['name']}**\n"

            if has_achievement:
                # Show full stats if unlocked
                stats = []
                if item_data.get('attack'):
                    stats.append(f"⚔️{item_data['attack']:,}")
                if item_data.get('defense'):
                    stats.append(f"🛡️{item_data['defense']:,}")
                if item_data.get('hp'):
                    stats.append(f"❤️{item_data['hp']:,}")
                if item_data.get('mana'):
                    stats.append(f"💙{item_data['mana']:,}")

                item_display += f"*{' | '.join(stats)}*\n"
                item_display += f"📖 {item_data['description']}\n"
            else:
                item_display += f"*Hidden until unlocked*\n"

            item_display += f"🏆 **Requires:** {achievement_name}\n"
            item_display += f"📋 *{achievement_desc}*"

            embed.add_field(
                name=f"{item_data['name']}" + (" - UNLOCKED!" if has_achievement else " - Locked"),
                value=item_display,
                inline=False
            )

        embed.add_field(
            name="📊 Your Progress",
            value=f"**Unlocked:** {unlocked_count}/10 items\n"
                  f"**Progress:** {int((unlocked_count/10)*100)}% complete\n\n"
                  f"💡 **Tip:** Use `$achievements` to track your progress!",
            inline=False
        )

        if unlocked_count == 0:
            embed.set_footer(text="🔥 Challenge yourself to unlock these legendary items!")
        elif unlocked_count < 5:
            embed.set_footer(text="⚡ You're making progress! Keep pushing your limits!")
        elif unlocked_count < 10:
            embed.set_footer(text="🌟 So close to completing the legendary collection!")
        else:
            embed.set_footer(text="👑 CONGRATULATIONS! You've unlocked all legendary items!")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RPGCore(bot))