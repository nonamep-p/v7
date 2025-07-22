import discord
from discord.ext import commands
from replit import db
import random
import asyncio
from datetime import datetime
from rpg_data.game_data import TACTICAL_MONSTERS, ITEMS
from utils.helpers import create_embed, format_number
from config import COLORS, is_module_enabled
import logging

logger = logging.getLogger(__name__)

# Enhanced Dungeon definitions with comprehensive scenarios
DUNGEONS = {
    'akuma_catacombs': {
        'name': 'The Crumbling Akuma Catacombs',
        'emoji': '🏴‍☠️',
        'min_level': 1,
        'max_level': 8,
        'floors': 3,
        'description': 'Dusty, dark stone corridors filled with cobwebs, leftover magical energy, and disappointingly cheese-free air.',
        'monsters': ['shadow_grub', 'akuma_sentinel', 'cursed_spirit'],
        'boss': 'Giant Akumatized Spider',
        'theme': 'dark_catacombs',
        'plagg_intro': "Ugh, finally. You've stumbled into the Akuma Catacombs. It smells like old socks and regret, with just a HINT of aged cheese. Disappointing, really.",
        'rewards': {
            'xp_multiplier': 1.5,
            'gold_multiplier': 1.3,
            'rare_materials': ['shadow_essence', 'akuma_fragment', 'old_cheese_rind']
        }
    },
    'foxen_forest': {
        'name': 'The Whispering Foxen Forest',
        'emoji': '🌲',
        'min_level': 8,
        'max_level': 15,
        'floors': 5,
        'description': 'An enchanted forest of perpetual twilight with glowing runes and trickster magic.',
        'monsters': ['forest_sprite', 'illusion_fox', 'trickster_spirit'],
        'boss': 'Council of Kitsune Illusionists',
        'theme': 'mystical_forest',
        'plagg_intro': "Great, a magical forest. It's all sparkly and mystical and has exactly ZERO cheese. The foxes better have some good snacks hidden somewhere.",
        'rewards': {
            'xp_multiplier': 2.0,
            'gold_multiplier': 1.8,
            'rare_materials': ['fox_fur', 'illusion_crystal', 'forest_essence']
        }
    },
    'shadow_fortress': {
        'name': 'Shadow Fortress',
        'emoji': '🏰',
        'min_level': 15,
        'max_level': 25,
        'floors': 7,
        'description': 'An ancient fortress consumed by darkness and shadowy beings.',
        'monsters': ['shadow_assassin', 'shadow_wraith', 'void_sentinel'],
        'boss': 'Shadow Lord',
        'theme': 'dark_fortress',
        'plagg_intro': "Oh wonderful, a spooky shadow fortress. Because what I really needed was MORE darkness and LESS cheese visibility.",
        'rewards': {
            'xp_multiplier': 2.5,
            'gold_multiplier': 2.2,
            'rare_materials': ['shadow_essence', 'dark_crystal', 'void_fragment']
        }
    },
    'dragons_lair': {
        'name': "Dragon's Lair",
        'emoji': '🐉',
        'min_level': 25,
        'max_level': 35,
        'floors': 10,
        'description': 'The lair of an ancient dragon, filled with legendary treasures.',
        'monsters': ['fire_drake', 'dragon_cultist', 'flame_elemental'],
        'boss': 'Ancient Red Dragon',
        'theme': 'dragon_hoard',
        'plagg_intro': "A dragon's lair! Finally, someone with good taste in hoarding. Though I bet they don't collect cheese. Typical.",
        'rewards': {
            'xp_multiplier': 3.0,
            'gold_multiplier': 2.8,
            'rare_materials': ['dragon_scale', 'dragon_heart', 'legendary_gem']
        }
    },
    'cosmic_void': {
        'name': 'The Cosmic Void of the Peacock',
        'emoji': '🌌',
        'min_level': 35,
        'max_level': 50,
        'floors': 15,
        'description': 'A mind-bending reality of floating islands and crystallized emotions.',
        'monsters': ['void_walker', 'emotion_wraith', 'cosmic_horror'],
        'boss': 'Manifestation of Cosmic Indifference',
        'theme': 'cosmic_nightmare',
        'plagg_intro': "Well, THIS is new. We're in some kind of emotional void space thing. It's all floaty and weird and I GUARANTEE there's no cheese. This is the worst.",
        'rewards': {
            'xp_multiplier': 4.0,
            'gold_multiplier': 3.5,
            'rare_materials': ['void_essence', 'cosmic_dust', 'reality_fragment']
        }
    }
}

class DungeonSelectionView(discord.ui.View):
    """Interactive dungeon selection interface."""

    def __init__(self, user_id, rpg_core):
        super().__init__(timeout=300)
        self.user_id = str(user_id)
        self.rpg_core = rpg_core
        self.add_dungeon_select()

    def add_dungeon_select(self):
        """Add dungeon selection dropdown."""
        player_data = self.rpg_core.get_player_data(self.user_id)
        if not player_data:
            return

        player_level = player_data.get('level', 1)

        options = []
        for dungeon_key, dungeon_data in DUNGEONS.items():
            min_level = dungeon_data['min_level']
            max_level = dungeon_data['max_level']

            if player_level >= min_level:
                difficulty = "Easy" if player_level > max_level else "Challenging" if player_level >= max_level - 5 else "Hard"

                options.append(discord.SelectOption(
                    label=f"{dungeon_data['name']} (Lv. {min_level}-{max_level})",
                    value=dungeon_key,
                    description=f"{difficulty} • {dungeon_data['floors']} floors",
                    emoji=dungeon_data['emoji']
                ))

        if options:
            select = DungeonSelect(options, self.user_id, self.rpg_core)
            self.add_item(select)

class DungeonSelect(discord.ui.Select):
    """Dropdown for selecting dungeons."""

    def __init__(self, options, user_id, rpg_core):
        super().__init__(
            placeholder="🏰 Choose your dungeon adventure...",
            options=options,
            max_values=1
        )
        self.user_id = user_id
        self.rpg_core = rpg_core

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ This isn't your dungeon selection!", ephemeral=True)
            return

        dungeon_key = self.values[0]

        # Start the dungeon exploration
        view = DungeonExplorationView(self.user_id, dungeon_key, self.rpg_core)
        embed = view.create_dungeon_intro_embed()

        await interaction.response.edit_message(embed=embed, view=view)

class DungeonExplorationView(discord.ui.View):
    """Comprehensive dungeon exploration system."""

    def __init__(self, user_id, dungeon_key, rpg_core):
        super().__init__(timeout=900)  # 15 minute timeout
        self.user_id = str(user_id)
        self.dungeon_key = dungeon_key
        self.rpg_core = rpg_core
        self.dungeon_data = DUNGEONS[dungeon_key]

        # Exploration state
        self.current_floor = 1
        self.current_room = 1
        self.rooms_per_floor = 5
        self.total_rooms_explored = 0
        self.total_rooms = self.dungeon_data['floors'] * self.rooms_per_floor

        # Session tracking
        self.total_xp_gained = 0
        self.total_gold_gained = 0
        self.items_found = []
        self.monsters_defeated = 0
        self.floors_completed = 0

        # Current scenario
        self.current_scenario = None
        self.awaiting_choice = False

        # Load player data
        self.player_data = self.rpg_core.get_player_data(user_id)
        if not self.player_data:
            return

    def create_dungeon_intro_embed(self):
        """Create the dungeon introduction embed."""
        embed = discord.Embed(
            title=f"{self.dungeon_data['emoji']} Welcome to {self.dungeon_data['name']}",
            description=f"*\"{self.dungeon_data['plagg_intro']}\"*\n\n"
                       f"**{self.dungeon_data['description']}**\n\n"
                       f"**Dungeon Info:**\n"
                       f"• **Floors:** {self.dungeon_data['floors']}\n"
                       f"• **Recommended Level:** {self.dungeon_data['min_level']}-{self.dungeon_data['max_level']}\n"
                       f"• **Boss:** {self.dungeon_data['boss']}\n\n"
                       f"**Your Level:** {self.player_data['level']}",
            color=COLORS['primary']
        )

        # Add rewards info
        rewards = self.dungeon_data['rewards']
        embed.add_field(
            name="💰 Potential Rewards",
            value=f"• **XP Bonus:** +{int((rewards['xp_multiplier'] - 1) * 100)}%\n"
                  f"• **Gold Bonus:** +{int((rewards['gold_multiplier'] - 1) * 100)}%\n"
                  f"• **Rare Materials:** {len(rewards['rare_materials'])} types",
            inline=True
        )

        embed.set_footer(text="💡 Click 'Enter Dungeon' to begin your adventure!")

        # Add enter button
        self.clear_items()
        self.add_item(EnterDungeonButton())
        self.add_item(ExitDungeonButton())

        return embed

    def create_exploration_embed(self):
        """Create the main exploration interface embed."""
        embed = discord.Embed(
            title=f"🗺️ Floor {self.current_floor} - Room {self.current_room}",
            description=f"*\"Keep moving, cheese-seeker. This floor isn't going to explore itself.\"*\n\n"
                       f"You stand in a dimly lit chamber of {self.dungeon_data['name']}. "
                       f"The air is thick with {self.get_atmosphere_description()}.",
            color=COLORS['primary']
        )

        # Progress tracking
        floor_progress = f"{self.current_room}/{self.rooms_per_floor}"
        total_progress = f"{self.total_rooms_explored}/{self.total_rooms}"
        progress_percentage = (self.total_rooms_explored / self.total_rooms) * 100

        embed.add_field(
            name="📊 Progress",
            value=f"**Floor:** {self.current_floor}/{self.dungeon_data['floors']}\n"
                  f"**Room:** {floor_progress}\n"
                  f"**Total:** {total_progress} ({progress_percentage:.1f}%)",
            inline=True
        )

        # Session stats
        embed.add_field(
            name="⚡ Session Stats",
            value=f"**XP Gained:** {format_number(self.total_xp_gained)}\n"
                  f"**Gold Gained:** {format_number(self.total_gold_gained)}\n"
                  f"**Monsters:** {self.monsters_defeated}",
            inline=True
        )

        # Player status
        hp = self.player_data['resources']['hp']
        max_hp = self.player_data['resources']['max_hp']
        hp_bar = self.create_health_bar(hp, max_hp)

        embed.add_field(
            name="🛡️ Status",
            value=f"**HP:** {hp_bar} {hp}/{max_hp}\n"
                  f"**Level:** {self.player_data['level']}\n"
                  f"**Gold:** {format_number(self.player_data['gold'])}",
            inline=True
        )

        return embed

    def get_atmosphere_description(self):
        """Get atmospheric description based on dungeon theme."""
        atmospheres = {
            'dark_catacombs': "ancient magic and sadly, no cheese whatsoever",
            'mystical_forest': "enchantment and trickery, but disappointingly cheese-free",
            'dark_fortress': "shadows and malevolent energy (and zero cheese)",
            'dragon_hoard': "sulfur and treasure (though probably not cheese treasure)",
            'cosmic_nightmare': "otherworldly energies and cosmic cheese-lessness"
        }
        return atmospheres.get(self.dungeon_data['theme'], "mystery and adventure")

    def create_health_bar(self, current, maximum):
        """Create a visual health bar."""
        if maximum == 0:
            return "▱▱▱▱▱"

        percentage = current / maximum
        filled_blocks = int(percentage * 5)
        empty_blocks = 5 - filled_blocks

        return "▰" * filled_blocks + "▱" * empty_blocks

    async def update_exploration_view(self):
        """Update the exploration interface."""
        self.clear_items()

        if self.current_room > self.rooms_per_floor:
            # Floor completed
            if self.current_floor >= self.dungeon_data['floors']:
                # Final boss
                self.add_item(FinalBossButton())
            else:
                # Next floor
                self.add_item(NextFloorButton())
                self.add_item(RestButton())
        else:
            # Continue exploration
            self.add_item(ExploreRoomButton())
            self.add_item(RestButton())

        self.add_item(ExitDungeonButton())

class EnterDungeonButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Enter Dungeon", style=discord.ButtonStyle.success, emoji="🚪")

    async def callback(self, interaction: discord.Interaction):
        view = self.view

        # Start exploration
        embed = view.create_exploration_embed()
        await view.update_exploration_view()

        await interaction.response.edit_message(embed=embed, view=view)

class ExploreRoomButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Explore Room", style=discord.ButtonStyle.primary, emoji="🔍")

    async def callback(self, interaction: discord.Interaction):
        view = self.view

        # Generate random encounter
        encounter_type = random.choices(
            ['monster', 'treasure', 'trap', 'empty'],
            weights=[40, 30, 20, 10]
        )[0]

        result = view.process_room_encounter(encounter_type)

        # Update progress
        view.current_room += 1
        view.total_rooms_explored += 1

        # Create result embed
        embed = view.create_encounter_result_embed(encounter_type, result)
        await view.update_exploration_view()

        await interaction.response.edit_message(embed=embed, view=view)

class NextFloorButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Descend to Next Floor", style=discord.ButtonStyle.success, emoji="⬇️")

    async def callback(self, interaction: discord.Interaction):
        view = self.view

        view.current_floor += 1
        view.current_room = 1
        view.floors_completed += 1

        embed = discord.Embed(
            title=f"🏁 Floor {view.current_floor - 1} Complete!",
            description=f"*\"Congratulations, you survived another floor. Only {view.dungeon_data['floors'] - view.current_floor + 1} more to go. "
                       f"Don't get cocky.\"*\n\n"
                       f"You descend deeper into the {view.dungeon_data['name']}...",
            color=COLORS['success']
        )

        await view.update_exploration_view()
        await interaction.response.edit_message(embed=embed, view=view)

class RestButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Rest", style=discord.ButtonStyle.secondary, emoji="💤")

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        player_data = view.player_data

        # Restore some HP
        resources = player_data['resources']
        heal_amount = int(resources['max_hp'] * 0.25)  # 25% heal
        old_hp = resources['hp']
        resources['hp'] = min(resources['max_hp'], resources['hp'] + heal_amount)
        actual_heal = resources['hp'] - old_hp

        view.rpg_core.save_player_data(view.user_id, player_data)

        embed = discord.Embed(
            title="💤 Rest Complete",
            description=f"*\"Fine, take a little nap. I'll keep watch for cheese... I mean, danger.\"*\n\n"
                       f"You rest for a moment and recover {actual_heal} HP.",
            color=COLORS['info']
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

class FinalBossButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Face the Final Boss", style=discord.ButtonStyle.danger, emoji="🐉")

    async def callback(self, interaction: discord.Interaction):
        view = self.view

        # Boss encounter logic
        boss_result = view.process_boss_encounter()

        embed = discord.Embed(
            title=f"🐉 FINAL BOSS: {view.dungeon_data['boss']}",
            description=boss_result,
            color=COLORS['error'] if 'defeated' in boss_result.lower() else COLORS['success']
        )

        if 'victory' in boss_result.lower():
            # Dungeon completed
            completion_rewards = view.calculate_completion_rewards()
            embed.add_field(
                name="🏆 Completion Rewards",
                value=completion_rewards,
                inline=False
            )

        view.clear_items()
        view.add_item(ExitDungeonButton())

        await interaction.response.edit_message(embed=embed, view=view)

class ExitDungeonButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Exit Dungeon", style=discord.ButtonStyle.danger, emoji="🚪")

    async def callback(self, interaction: discord.Interaction):
        view = self.view

        # Final session summary
        embed = discord.Embed(
            title="📋 Dungeon Session Complete",
            description=f"*\"Well, that was... something. At least we didn't find any cheese to get my hopes up.\"*\n\n"
                       f"**Final Results:**\n"
                       f"• **Floors Explored:** {view.floors_completed}/{view.dungeon_data['floors']}\n"
                       f"• **Rooms Explored:** {view.total_rooms_explored}\n"
                       f"• **Monsters Defeated:** {view.monsters_defeated}\n"
                       f"• **XP Gained:** {format_number(view.total_xp_gained)}\n"
                       f"• **Gold Gained:** {format_number(view.total_gold_gained)}",
            color=COLORS['info']
        )

        if view.items_found:
            items_text = ", ".join(view.items_found[:5])
            if len(view.items_found) > 5:
                items_text += f" (+{len(view.items_found) - 5} more)"
            embed.add_field(name="🎒 Items Found", value=items_text, inline=False)

        await interaction.response.edit_message(embed=embed, view=None)

# Add these methods to DungeonExplorationView class
    def process_room_encounter(self, encounter_type):
        """Process different types of room encounters."""
        if encounter_type == 'monster':
            return self.handle_monster_encounter()
        elif encounter_type == 'treasure':
            return self.handle_treasure_encounter()
        elif encounter_type == 'trap':
            return self.handle_trap_encounter()
        else:
            return "The room appears empty. *\"Great, more nothing. Like a cheese-less refrigerator.\"*"

    def handle_monster_encounter(self):
        """Handle monster encounter."""
        monster = random.choice(self.dungeon_data['monsters'])

        # Simple combat resolution
        player_level = self.player_data['level']
        monster_strength = random.randint(1, 10)

        if player_level + random.randint(1, 6) > monster_strength:
            # Victory
            xp_gain = random.randint(20, 50) * self.dungeon_data['rewards']['xp_multiplier']
            gold_gain = random.randint(10, 30) * self.dungeon_data['rewards']['gold_multiplier']

            self.total_xp_gained += int(xp_gain)
            self.total_gold_gained += int(gold_gain)
            self.monsters_defeated += 1

            # Update player data
            self.player_data['xp'] += int(xp_gain)
            self.player_data['gold'] += int(gold_gain)

            return f"Victory! You defeated the {monster.replace('_', ' ').title()}! Gained {int(xp_gain)} XP and {int(gold_gain)} gold."
        else:
            # Defeat
            damage = random.randint(5, 15)
            self.player_data['resources']['hp'] = max(1, self.player_data['resources']['hp'] - damage)
            return f"The {monster.replace('_', ' ').title()} proves too strong! You take {damage} damage."

    def handle_treasure_encounter(self):
        """Handle treasure encounter."""
        treasure_type = random.choice(['gold', 'item', 'materials'])

        if treasure_type == 'gold':
            gold_amount = random.randint(50, 150) * self.dungeon_data['rewards']['gold_multiplier']
            self.total_gold_gained += int(gold_amount)
            self.player_data['gold'] += int(gold_amount)
            return f"Treasure chest! You found {int(gold_amount)} gold!"

        elif treasure_type == 'item':
            item_key = 'health_potion'  # Simplified for now
            inventory = self.player_data.get('inventory', {})
            inventory[item_key] = inventory.get(item_key, 0) + 1
            self.player_data['inventory'] = inventory
            self.items_found.append(item_key.replace('_', ' ').title())
            return f"You found a {item_key.replace('_', ' ').title()}!"

        else:
            material = random.choice(self.dungeon_data['rewards']['rare_materials'])
            inventory = self.player_data.get('inventory', {})
            inventory[material] = inventory.get(material, 0) + 1
            self.player_data['inventory'] = inventory
            self.items_found.append(material.replace('_', ' ').title())
            return f"Rare materials! You found {material.replace('_', ' ').title()}!"

    def handle_trap_encounter(self):
        """Handle trap encounter."""
        trap_types = [
            ("Pressure Plate", "You step on a pressure plate and spikes shoot up!"),
            ("Poison Dart", "A dart flies out of the wall!"),
            ("Pit Trap", "The floor gives way beneath you!")
        ]

        trap_name, description = random.choice(trap_types)

        # Simple trap resolution
        if random.randint(1, 10) > 6:  # 40% chance to avoid
            return f"{description} But you dodge it skillfully!"
        else:
            damage = random.randint(8, 20)
            self.player_data['resources']['hp'] = max(1, self.player_data['resources']['hp'] - damage)
            return f"{description} You take {damage} damage!"

    def process_boss_encounter(self):
        """Process the final boss encounter."""
        boss_name = self.dungeon_data['boss']
        player_level = self.player_data['level']

        # Simple boss fight resolution
        boss_difficulty = self.dungeon_data['max_level']

        if player_level + random.randint(1, 10) > boss_difficulty - 5:
            # Victory
            xp_reward = 200 * self.dungeon_data['rewards']['xp_multiplier']
            gold_reward = 500 * self.dungeon_data['rewards']['gold_multiplier']

            self.total_xp_gained += int(xp_reward)
            self.total_gold_gained += int(gold_reward)

            self.player_data['xp'] += int(xp_reward)
            self.player_data['gold'] += int(gold_reward)

            return f"VICTORY! You have defeated the {boss_name}! The dungeon trembles as your foe falls!"
        else:
            # Defeat
            damage = random.randint(20, 40)
            self.player_data['resources']['hp'] = max(1, self.player_data['resources']['hp'] - damage)
            return f"The {boss_name} proves too powerful! You are defeated and must retreat, taking {damage} damage."

    def calculate_completion_rewards(self):
        """Calculate final completion rewards."""
        bonus_xp = 100 * self.floors_completed
        bonus_gold = 200 * self.floors_completed

        self.player_data['xp'] += bonus_xp
        self.player_data['gold'] += bonus_gold

        return f"**Completion Bonus:** +{bonus_xp} XP, +{bonus_gold} Gold"

    def create_encounter_result_embed(self, encounter_type, result):
        """Create embed for encounter results."""
        embed = discord.Embed(
            title=f"🎲 {encounter_type.title()} Encounter",
            description=result,
            color=COLORS['primary']
        )

        # Update player status in embed
        hp = self.player_data['resources']['hp']
        max_hp = self.player_data['resources']['max_hp']

        embed.add_field(
            name="🛡️ Status",
            value=f"**HP:** {hp}/{max_hp}\n"
                  f"**Session XP:** {format_number(self.total_xp_gained)}\n"
                  f"**Session Gold:** {format_number(self.total_gold_gained)}",
            inline=True
        )

        return embed

class RPGDungeons(commands.Cog):
    """Comprehensive dungeon exploration system."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dungeons", aliases=["dung", "explore_dungeon"])
    async def dungeon_explore(self, ctx, dungeon_name: str = None):
        """Enter and explore dangerous dungeons for rewards."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        rpg_core = self.bot.get_cog('RPGCore')
        if not rpg_core:
            await ctx.send("❌ RPG system not loaded.")
            return

        player_data = rpg_core.get_player_data(ctx.author.id)
        if not player_data:
            embed = create_embed("No Character", "Use `$startrpg` first!", COLORS['error'])
            await ctx.send(embed=embed)
            return

        # Check if player is in combat
        if rpg_core.is_player_in_combat(ctx.author.id):
            embed = discord.Embed(
                title="⚔️ Currently in Combat",
                description="You're currently in combat! Finish your battle first.",
                color=COLORS['warning']
            )
            await ctx.send(embed=embed)
            return

        if not dungeon_name:
            # Show dungeon selection
            embed = self.create_dungeon_list_embed(player_data)
            view = DungeonSelectionView(str(ctx.author.id), rpg_core)
            await ctx.send(embed=embed, view=view)
        else:
            # Try to enter specific dungeon
            dungeon_key = dungeon_name.lower().replace(' ', '_')
            if dungeon_key not in DUNGEONS:
                await ctx.send(f"❌ Unknown dungeon: {dungeon_name}")
                return

            dungeon_data = DUNGEONS[dungeon_key]
            if player_data['level'] < dungeon_data['min_level']:
                await ctx.send(f"❌ You need to be level {dungeon_data['min_level']} to enter {dungeon_data['name']}!")
                return

            # Start dungeon directly
            view = DungeonExplorationView(str(ctx.author.id), dungeon_key, rpg_core)
            embed = view.create_dungeon_intro_embed()
            await ctx.send(embed=embed, view=view)

    def create_dungeon_list_embed(self, player_data):
        """Create the dungeon selection embed."""
        embed = discord.Embed(
            title="🏰 Available Dungeons",
            description="*\"Ah, looking for adventure? These places are dangerous, uncomfortable, and definitely cheese-free. Perfect for you.\"*",
            color=COLORS['primary']
        )

        player_level = player_data['level']

        for dungeon_key, dungeon_data in DUNGEONS.items():
            min_level = dungeon_data['min_level']
            max_level = dungeon_data['max_level']

            # Determine difficulty and accessibility
            if player_level < min_level:
                status = f"🔒 Requires Level {min_level}"
                difficulty = "Locked"
            elif player_level > max_level:
                status = "✅ Easy"
                difficulty = "Easy"
            elif player_level >= max_level - 5:
                status = "⚠️ Challenging"
                difficulty = "Challenging"
            else:
                status = "💀 Hard"
                difficulty = "Hard"

            embed.add_field(
                name=f"{dungeon_data['emoji']} {dungeon_data['name']}",
                value=f"**Level Range:** {min_level}-{max_level}\n"
                      f"**Floors:** {dungeon_data['floors']}\n"
                      f"**Status:** {status}\n"
                      f"**Boss:** {dungeon_data['boss']}",
                inline=True
            )

        embed.add_field(
            name="🎯 Your Level",
            value=f"**Current Level:** {player_level}\n"
                  f"**HP:** {player_data['resources']['hp']}/{player_data['resources']['max_hp']}\n"
                  f"**Gold:** {format_number(player_data['gold'])}",
            inline=False
        )

        embed.set_footer(text="💡 Select a dungeon from the dropdown below to begin your adventure!")
        return embed

async def setup(bot):
    await bot.add_cog(RPGDungeons(bot))