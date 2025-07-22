import discord
from discord.ext import commands
from config import COLORS, is_module_enabled, get_server_config
import asyncio

class MainMenuView(discord.ui.View):
    """Main interactive menu for the RPG bot."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    @discord.ui.select(
        placeholder="🎮 Choose a category to explore...",
        options=[
            discord.SelectOption(
                label="⚔️ Character & Combat",
                value="character",
                description="Character creation, classes, combat, and progression",
                emoji="⚔️"
            ),
            discord.SelectOption(
                label="🏰 Adventures & Dungeons",
                value="adventures",
                description="Hunting, dungeons, exploration, and PvE content",
                emoji="🏰"
            ),
            discord.SelectOption(
                label="🛒 Economy & Trading",
                value="economy",
                description="Shop, inventory, crafting, and item management",
                emoji="🛒"
            ),
            discord.SelectOption(
                label="🏆 PvP & Arena",
                value="pvp",
                description="Arena battles, rankings, and competitive play",
                emoji="🏆"
            ),
            discord.SelectOption(
                label="✨ Advanced Features",
                value="advanced",
                description="Artifacts, achievements, paths, and hidden content",
                emoji="✨"
            ),
            discord.SelectOption(
                label="🔧 Admin & Management",
                value="admin",
                description="Server settings and administrative commands",
                emoji="🔧"
            )
        ]
    )
    async def category_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        category = select.values[0]

        if category == "character":
            view = CharacterMenuView(self.bot, self.prefix)
        elif category == "adventures":
            view = AdventureMenuView(self.bot, self.prefix)
        elif category == "economy":
            view = EconomyMenuView(self.bot, self.prefix)
        elif category == "pvp":
            view = PvPMenuView(self.bot, self.prefix)
        elif category == "advanced":
            view = AdvancedMenuView(self.bot, self.prefix)
        elif category == "admin":
            view = AdminMenuView(self.bot, self.prefix)
        else:
            view = self

        embed = view.create_embed() if hasattr(view, 'create_embed') else self.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🏠 Main Menu", style=discord.ButtonStyle.secondary, row=1)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="📖 Tutorial", style=discord.ButtonStyle.success, row=1)
    async def tutorial_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = TutorialView(self.bot, self.prefix)
        embed = discord.Embed(
            title="📖 Interactive Tutorial System",
            description="**Welcome to the comprehensive tutorial!**\n\n"
                       "This step-by-step guide will teach you everything you need "
                       "to know about playing Project: Blood & Cheese.\n\n"
                       "**What you'll learn:**\n"
                       "- Character creation and classes\n"
                       "- Combat mechanics and strategy\n"
                       "- Character progression and stats\n"
                       "- Economy and equipment\n"
                       "- Adventures and exploration\n"
                       "- Advanced tips and warnings\n\n"
                       "Click **Start Tutorial** to begin!",
            color=COLORS['primary']
        )
        embed.set_footer(text="Tutorial • Interactive Learning Experience")
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="📚 Info Database", style=discord.ButtonStyle.primary, row=1)
    async def info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = InfoPanelView(self.bot, self.prefix)
        embed = discord.Embed(
            title="📚 Game Information Database",
            description="**Comprehensive game mechanics reference!**\n\n"
                       "This information system provides detailed breakdowns of all "
                       "game mechanics, formulas, and systems for players who want "
                       "to understand the game at a deeper level.\n\n"
                       "**Available Topics:**\n"
                       "- Combat mechanics and formulas\n"
                       "- Character statistics and effects\n"
                       "- Item rarity and quality systems\n"
                       "- Classes and Miraculous Paths\n"
                       "- Kwami Artifacts and set bonuses\n"
                       "- Achievement system and rewards\n"
                       "- Economic systems and trading\n"
                       "- Mathematical formulas and calculations\n\n"
                       "**Perfect for:** Min-maxers, theorycrafters, and curious players!",
            color=COLORS['info']
        )
        embed.set_footer(text="Information Database • For the Nerds 🤓")
        await interaction.response.edit_message(embed=embed, view=view)

    def create_main_embed(self):
        embed = discord.Embed(
            title="🧀 Project: Blood & Cheese - Combat RPG",
            description="**Welcome to the ultimate combat-focused RPG experience!**\n\n"
                       "🎯 **Core Philosophy:** Combat is King! Every feature serves to make you a more powerful warrior.\n\n"
                       "🌟 **Your Journey Awaits:**\n"
                       "- Create your character and choose a combat class\n"
                       "- Master the tactical combat system\n"
                       "- Hunt monsters and explore dangerous dungeons\n"
                       "- Craft legendary equipment and artifacts\n"
                       "- Dominate in PvP Arena battles\n"
                       "- Join factions for large-scale warfare\n\n"
                       "**Select a category below to begin your adventure!**\n\n"
                       f"**Quick Start:** Use `{self.prefix}startrpg` to create your character!",
            color=COLORS['primary']
        )
        embed.set_footer(text="Use the dropdown menu to navigate • Made by NoNameP_P")
        return embed

class CharacterMenuView(discord.ui.View):
    """Character and combat focused menu."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    @discord.ui.select(
        placeholder="⚔️ Character & Combat Commands",
        options=[
            discord.SelectOption(
                label="🎭 Create Character",
                value="startrpg",
                description="$start, $begin, $create - Begin your journey",
                emoji="🎭"
            ),
            discord.SelectOption(
                label="📊 View Profile",
                value="profile",
                description="$prof, $me, $stats - View your character",
                emoji="📊"
            ),
            discord.SelectOption(
                label="⚔️ Enter Combat",  
                value="battle",
                description="$fight, $battle, $combat - Engage monsters",
                emoji="⚔️"
            ),
            discord.SelectOption(
                label="📈 Allocate Stats",
                value="allocate",
                description="allocate - Distribute stat points to grow stronger",
                emoji="📈"
            ),
            discord.SelectOption(
                label="🌟 Choose Path",
                value="path",
                description="path - Select your Miraculous Path (Level 20+)",
                emoji="🌟"
            ),
            discord.SelectOption(
                label="🎓 View Classes",
                value="classes",
                description="classes - See all available character classes",
                emoji="🎓"
            ),
            discord.SelectOption(
                label="⚡ View Skills",
                value="skills",
                description="skills - See your combat abilities and techniques",
                emoji="⚡"
            )
        ]
    )
    async def command_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        command = select.values[0]
        embed = self.create_command_embed(command)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🏠 Main Menu", style=discord.ButtonStyle.secondary, row=1)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🎮 Quick Actions", style=discord.ButtonStyle.primary, row=1)
    async def quick_actions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = CharacterQuickActionsView(self.bot, self.prefix)
        embed = discord.Embed(
            title="🎮 Character Quick Actions",
            description="**Use these buttons to quickly access character commands:**\n\n"
                       "Click the buttons below to instantly run commands without typing!",
            color=COLORS['success']
        )
        await interaction.response.edit_message(embed=embed, view=view)

    def create_embed(self):
        embed = discord.Embed(
            title="⚔️ Character & Combat System",
            description="**Master the art of combat and forge your legend!**\n\n"
                       "The character system is the foundation of your power. Choose your class wisely, "
                       "allocate stats strategically, and master the tactical combat engine.\n\n"
                       "**Key Features:**\n"
                       "- 7 Unique Character Classes with distinct roles\n"
                       "- Tactical Turn-Based Combat System\n"
                       "- Skill Point & Ultimate Energy Mechanics\n"
                       "- Weakness Break & Follow-up Attacks\n"
                       "- Miraculous Paths for end-game specialization\n\n"
                       "Select a command from the dropdown to learn more!",
            color=COLORS['error']
        )
        return embed

    def create_command_embed(self, command):
        embeds = {
            "startrpg": discord.Embed(
                title="🎭 Create Your Character",
                description=f"**Command:** `{self.prefix}startrpg`\n\n"
                           "Begin your legendary journey as a combatant in Project: Blood & Cheese!\n\n"
                           "**What happens:**\n"
                           "- Interactive class selection with detailed descriptions\n"
                           "- Starting equipment and resources\n"
                           "- Level 1 character with balanced base stats\n"
                           "- Welcome package with potions and gold\n\n"
                           "**Available Classes:**\n"
                           "🛡️ **Warrior** - Tank with high defense\n"
                           "🔮 **Mage** - Magical DPS with area attacks\n"
                           "🗡️ **Rogue** - High crit assassin\n"
                           "🏹 **Archer** - Ranged precision striker\n"
                           "❤️ **Healer** - Support with healing abilities\n"
                           "⚔️ **Battlemage** - Hybrid melee/magic fighter\n"
                           "⏰ **Chrono Knight** - Time manipulation specialist",
                color=COLORS['success']
            ),
            "profile": discord.Embed(
                title="📊 Character Profile",
                description=f"**Command:** `{self.prefix}profile [@user]`\n\n"
                           "View detailed character information and combat statistics.\n\n"
                           "**Profile Information:**\n"
                           "- Character level and XP progress\n"
                           "- Base stats and combat derived stats\n"
                           "- Current HP, Mana, and resources\n"
                           "- Arena rating and win/loss record\n"
                           "- Chosen Miraculous Path and faction\n"
                           "- Equipment and active effects\n\n"
                           "**Special Features:**\n"
                           "- View other players' profiles\n"
                           "- Special display for bot owner\n"
                           "- Combat status indicator",
                color=COLORS['primary']
            ),
            "battle": discord.Embed(
                title="⚔️ Tactical Combat",
                description=f"**Command:** `{self.prefix}battle [monster]`\n\n"
                           "Engage in strategic turn-based combat with monsters!\n\n"
                           "**Combat Mechanics:**\n"
                           "- **Skill Points (SP):** Generate with basic attacks, spend on abilities\n"
                           "- **Ultimate Energy:** Build up to unleash devastating ultimates\n"
                           "- **Weakness Break:** Hit enemy weaknesses to stun them\n"
                           "- **Follow-up Attacks:** Chain attacks for bonus damage\n"
                           "- **Technique Points:** Pre-combat preparation abilities\n\n"
                           "**Rewards:**\n"
                           "- Experience points for leveling up\n"
                           "- Gold and valuable loot\n"
                           "- Rare equipment and artifacts\n"
                           "- Arena rating improvements",
                color=COLORS['error']
            ),
            "allocate": discord.Embed(
                title="📈 Stat Allocation",
                description=f"**Command:** `{self.prefix}allocate <stat> <points>`\n\n"
                           "Distribute stat points to customize your character's strengths.\n\n"
                           "**Available Stats:**\n"
                           "- **STR (Strength):** Physical damage and carrying capacity\n"
                           "- **DEX (Dexterity):** Critical chance, dodge, and initiative\n"
                           "- **CON (Constitution):** Maximum HP and damage reduction\n"
                           "- **INT (Intelligence):** Magical damage and maximum mana\n"
                           "- **WIS (Wisdom):** Healing power and mana regeneration\n"
                           "- **CHA (Charisma):** Shop prices and social interactions\n\n"
                           "**Examples:**\n"
                           f"`{self.prefix}allocate strength 5` - Add 5 points to Strength\n"
                           f"`{self.prefix}allocate dex 1` - Add 1 point to Dexterity",
                color=COLORS['warning']
            ),
            "path": discord.Embed(
                title="🌟 Miraculous Paths",
                description=f"**Command:** `{self.prefix}path`\n\n"
                           "Choose your permanent specialization at Level 20!\n\n"
                           "**Available Paths:**\n"
                           "💥 **Destruction** - Pure offensive power\n"
                           "   - +20% Critical Damage\n"
                           "   - Follow-up attack chances\n"
                           "   - Execution bonuses\n\n"
                           "🛡️ **Preservation** - Defensive mastery\n"
                           "   - +15% Damage Reduction\n"
                           "   - Shield generation abilities\n"
                           "   - Protective buffs\n\n"
                           "❤️‍🩹 **Abundance** - Support excellence\n"
                           "   - +25% Healing Power\n"
                           "   - Enhanced buff effects\n"
                           "   - Team synergy bonuses\n\n"
                           "🎯 **The Hunt** - Precision strikes\n"
                           "   - Execute low HP enemies\n"
                           "   - Enhanced accuracy\n"
                           "   - Single-target mastery",
                color=COLORS['legendary']
            ),
            "classes": discord.Embed(
                title="🎓 Character Classes",
                description=f"**Command:** `{self.prefix}classes`\n\n"
                           "View all available character classes and their specializations.\n\n"
                           "Each class has unique:\n"
                           "- **Role:** Tank, DPS, Support, or Hybrid\n"
                           "- **Passive Ability:** Always-active bonus\n"
                           "- **Ultimate Ability:** Powerful combat finisher\n"
                           "- **Starting Skills:** Class-specific abilities\n"
                           "- **Stat Focus:** Optimized attribute distribution\n\n"
                           "Choose based on your preferred playstyle:\n"
                           "- Aggressive damage dealing\n"
                           "- Defensive tanking\n"
                           "- Support and healing\n"
                           "- Balanced hybrid approach",
                color=COLORS['info']
            ),


}
        return embeds.get(command, self.create_embed())

class CharacterQuickActionsView(discord.ui.View):
    """Quick action buttons for character commands."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    @discord.ui.button(label="👤 Profile", style=discord.ButtonStyle.secondary, emoji="👤")
    async def profile_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        # Create a fake message for context
        fake_message = interaction.message
        fake_message.content = f"{self.prefix}profile"
        fake_message.author = interaction.user

        ctx = await self.bot.get_context(fake_message)
        command = self.bot.get_command('profile')

        if command:
            try:
                await command(ctx)
            except Exception as e:
                await interaction.followup.send(f"❌ Error running profile command: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send("❌ Profile command not found!", ephemeral=True)

    @discord.ui.button(label="🎒 Inventory", style=discord.ButtonStyle.secondary, emoji="🎒") 
    async def inventory_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        # Create a fake message for context
        fake_message = interaction.message
        fake_message.content = f"{self.prefix}inventory"
        fake_message.author = interaction.user

        ctx = await self.bot.get_context(fake_message)
        command = self.bot.get_command('inventory')

        if command:
            try:
                await command(ctx)
            except Exception as e:
                await interaction.followup.send(f"❌ Error running inventory command: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send("❌ Inventory command not found!", ephemeral=True)

    @discord.ui.button(label="⚔️ Battle", style=discord.ButtonStyle.danger, emoji="⚔️")
    async def battle_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        # Create a fake message for context
        fake_message = interaction.message
        fake_message.content = f"{self.prefix}battle"
        fake_message.author = interaction.user

        ctx = await self.bot.get_context(fake_message)
        command = self.bot.get_command('battle')

        if command:
            try:
                await command(ctx)
            except Exception as e:
                await interaction.followup.send(f"❌ Error running battle command: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send("❌ Battle command not found!", ephemeral=True)

    @discord.ui.button(label="🛒 Shop", style=discord.ButtonStyle.success, emoji="🛒")
    async def shop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        # Create a fake message for context
        fake_message = interaction.message
        fake_message.content = f"{self.prefix}shop"
        fake_message.author = interaction.user

        ctx = await self.bot.get_context(fake_message)
        command = self.bot.get_command('shop')

        if command:
            try:
                await command(ctx)
            except Exception as e:
                await interaction.followup.send(f"❌ Error running shop command: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send("❌ Shop command not found!", ephemeral=True)

    @discord.ui.button(label="🏠 Back to Help", style=discord.ButtonStyle.primary, row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    def create_command_embed(self, command):
        embeds = {
            "skills": discord.Embed(
                title="⚡ Combat Skills",
                description=f"**Command:** `{self.prefix}skills`\n\n"
                           "View your learned combat abilities and techniques.\n\n"
                           "**Skill Types:**\n"
                           "- **Class Skills:** Unique to your chosen class\n"
                           "- **Universal Skills:** Available to all classes\n"
                           "- **Passive Ability:** Your class's permanent bonus\n"
                           "- **Ultimate Ability:** Your most powerful attack\n\n"
                           "**Technique Points:**\n"
                           "Pre-combat preparation abilities that provide:\n"
                           "- Stat bonuses for the fight\n"
                           "- Special combat effects\n"
                           "- Strategic advantages\n\n"
                           "Skills unlock as you level up and progress!",
                color=COLORS['secondary']
            )
        }
        return embeds.get(command, self.create_embed())

class AdventureMenuView(discord.ui.View):
    """Adventure and exploration menu."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    @discord.ui.select(
        placeholder="🏰 Adventures & Exploration",
        options=[
            discord.SelectOption(
                label="🦌 Hunt Monsters",
                value="hunt",
                description="hunt - Search for creatures to battle",
                emoji="🦌"
            ),
            discord.SelectOption(
                label="🏰 Interactive Dungeons",
                value="dungeon",
                description="dungeons - Multi-floor adventures with scenarios",
                emoji="🏰"
            ),
            discord.SelectOption(
                label="✨ Miraculous Box",
                value="miraculous",
                description="miraculous - Enter artifact farming dimension",
                emoji="✨"
            ),
            discord.SelectOption(
                label="🗺️ Explore Areas", 
                value="explore",
                description="explore - Discover new locations and dungeons",
                emoji="🗺️"
            )
        ]
    )
    async def command_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        command = select.values[0]
        embed = self.create_command_embed(command)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🏠 Main Menu", style=discord.ButtonStyle.secondary, row=1)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🎮 Quick Actions", style=discord.ButtonStyle.primary, row=1)
    async def quick_actions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = AdventureQuickActionsView(self.bot, self.prefix)
        embed = discord.Embed(
            title="🎮 Adventure Quick Actions",
            description="**Use these buttons to quickly access adventure commands:**\n\n"
                       "Click the buttons below to instantly run commands without typing!",
            color=COLORS['success']
        )
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="📝 Try Commands", style=discord.ButtonStyle.primary, row=1)
    async def try_commands_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📝 Adventure Commands Channel",
            description=f"**Try these adventure commands in this channel:**\n\n"
                       f"• `{self.prefix}hunt` - Hunt for monsters\n"
                       f"• `{self.prefix}explore_dungeon <name>` - Enter dungeons\n"
                       f"• `{self.prefix}miraculous` - Farm artifacts\n"
                       f"• `{self.prefix}explore` - Discover locations\n\n"
                       "**Click any command to try it right here!**",
            color=COLORS['success']
        )
        embed.set_footer(text="Adventure Commands • Ready for exploration!")
        await interaction.response.edit_message(embed=embed, view=self)

    def create_embed(self):
        embed = discord.Embed(
            title="🏰 Adventures & Exploration",
            description="**Venture forth and claim your destiny!**\n\n"
                       "The world is filled with dangerous creatures, hidden treasures, and "
                       "mysterious dungeons waiting to be explored.\n\n"
                       "**Adventure Features:**\n"
                       "- Monster hunting with level-appropriate challenges\n"
                       "- Multi-floor dungeons with progressive difficulty\n"
                       "- Special artifact farming in the Miraculous Box\n"
                       "- World exploration with random encounters\n"
                       "- Epic boss battles with unique mechanics\n\n"
                       "Each adventure offers experience, gold, and rare loot!",
            color=COLORS['warning']
        )
        return embed

    def create_command_embed(self, command):
        """Create embed for specific command - Adventure category."""
        embeds = {
            "hunt": discord.Embed(
                title="🦌 Monster Hunting",
                description=f"**Command:** `{self.prefix}hunt`\n\n"
                           "Search the wilderness for creatures to battle!\n\n"
                           "**How it works:**\n"
                           "- System finds monsters near your level\n"
                           "- Automatically initiates tactical combat\n"
                           "- Rewards scale with monster difficulty\n"
                           "- 30-minute cooldown between hunts\n\n"
                           "**Rewards:**\n"
                           "- Experience points for leveling\n"
                           "- Gold and consumable items\n"
                           "- Equipment drops\n"
                           "- Rare crafting materials",
                color=COLORS['success']
            ),
            "dungeon": discord.Embed(
                title="🏰 Epic Interactive Dungeons",
                description=f"**Command:** `{self.prefix}dungeons` or `{self.prefix}dungeons <name>`\n\n"
                           "Experience revolutionary multi-floor dungeon adventures!\n\n"
                           "**Available Dungeons:**\n"
                           "- **🕳️ Goblin Caves** (Levels 1-5, 3 floors)\n"
                           "- **🏰 Shadow Fortress** (Levels 8-15, 5 floors)\n"
                           "- **🐉 Dragon's Lair** (Levels 20-30, 7 floors)\n"
                           "- **🌌 Cosmic Void** (Levels 35-50, 10 floors)\n\n"
                           "**Interactive Features:**\n"
                           "- **Floor-by-Floor Exploration**: Navigate room by room\n"
                           "- **Dynamic Encounters**: Monsters, treasures, traps, scenarios\n"
                           "- **Special Scenarios**: Puzzles, lava bridges, mirror halls\n"
                           "- **Epic Boss Battles**: Legendary final encounters\n"
                           "- **Session Tracking**: Complete performance statistics\n"
                           "- **Strategic Choices**: Rest, search, or rush forward\n\n"
                           "**Requirements:** 75% HP to enter, appropriate level",
                color=COLORS['info']
            ),
            "miraculous": discord.Embed(
                title="✨ Miraculous Box",
                description=f"**Command:** `{self.prefix}miraculous` or `{self.prefix}box`\n\n"
                           "Enter the mystical Miraculous Box for artifact farming!\n\n"
                           "**Requirements:**\n"
                           "- 40 Miraculous Energy per entry\n"
                           "- Not currently in combat\n"
                           "- Level 15+ recommended\n\n"
                           "**Rewards:**\n"
                           "- Kwami Artifacts with set bonuses\n"
                           "- Rare crafting materials\n"
                           "- Special enhancement stones\n\n"
                           "Energy regenerates 1 point every 5 minutes!",
                color=COLORS['legendary']
            ),
            "explore": discord.Embed(
                title="🗺️ World Exploration",
                description=f"**Command:** `{self.prefix}explore`\n\n"
                           "Discover new locations and hidden secrets!\n\n"
                           "**Possible Discoveries:**\n"
                           "- Ancient ruins with powerful artifacts\n"
                           "- Merchant camps with rare items\n"
                           "- Resource nodes for crafting\n"
                           "- Portal gates to special areas\n\n"
                           "**Cooldown:** 45 minutes between explorations\n"
                           "**Luck Factor:** Charisma affects discovery chances",
                color=COLORS['secondary']
            )
        }
        return embeds.get(command, self.create_embed())

class AdventureQuickActionsView(discord.ui.View):
    """Quick action buttons for adventure commands."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    # Implement button actions for hunt, dungeon, etc.
    # Example:
    # @discord.ui.button(label="Hunt", style=discord.ButtonStyle.secondary, emoji="🦌")
    # async def hunt_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     ...

    @discord.ui.button(label="🏠 Back to Help", style=discord.ButtonStyle.primary, row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class EconomyMenuView(discord.ui.View):
    """Economy and trading menu."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    @discord.ui.select(
        placeholder="🛒 Economy & Trading",
        options=[
            discord.SelectOption(
                label="🛒 Browse Shop",
                value="shop",
                description="shop - Buy weapons, armor, and items",
                emoji="🛒"
            ),
            discord.SelectOption(
                label="🎒 Interactive Inventory",
                value="inventory",
                description="inventory - Advanced item management with categories",
                emoji="🎒"
            ),
            discord.SelectOption(
                label="🔨 Crafting System",
                value="craft",
                description="craft - Create powerful equipment",
                emoji="🔨"
            ),
            discord.SelectOption(
                label="💰 Sell Items",
                value="sell",
                description="sell - Convert items to gold",
                emoji="💰"
            ),
            discord.SelectOption(
                label="🏛️ Auction House",
                value="auction",
                description="auction, market - Player trading system",
                emoji="🏛️"
            )
        ]
    )
    async def command_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        command = select.values[0]
        embed = self.create_command_embed(command)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🏠 Main Menu", style=discord.ButtonStyle.secondary, row=1)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🎮 Quick Actions", style=discord.ButtonStyle.primary, row=1)
    async def quick_actions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = EconomyQuickActionsView(self.bot, self.prefix)
        embed = discord.Embed(
            title="🎮 Economy Quick Actions",
            description="**Use these buttons to quickly access economy commands:**\n\n"
                       "Click the buttons below to instantly run commands without typing!",
            color=COLORS['success']
        )
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="📝 Try Commands", style=discord.ButtonStyle.primary, row=1)
    async def try_commands_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📝 Economy Commands Channel",
            description=f"**Try these economy commands in this channel:**\n\n"
                       f"• `{self.prefix}shop` - Browse the shop\n"
                       f"• `{self.prefix}inventory` - View your items\n"
                       f"• `{self.prefix}craft` - Create equipment\n"
                       f"• `{self.prefix}sell <item>` - Sell items for gold\n\n"
                       "**Click any command to try it right here!**",
            color=COLORS['success']
        )
        embed.set_footer(text="Economy Commands • Start trading!")
        await interaction.response.edit_message(embed=embed, view=self)

    def create_embed(self):
        embed = discord.Embed(
            title="🛒 Economy & Trading System",
            description="**Master the art of commerce and crafting!**\n\n"
                       "Build your wealth through smart trading, strategic purchases, "
                       "and masterful crafting.\n\n"
                       "**Economic Features:**\n"
                       "- Comprehensive shop with 8 rarity tiers\n"
                       "- Advanced crafting system with recipes\n"```python
                       "- Player-to-player trading market\n"
                       "- Dynamic pricing based on demand\n"
                       "- Investment opportunities and gambling\n"
                       "- Resource management and storage\n\n"
                       "Wealth is power - use it wisely!",
            color=COLORS['success']
        )
        return embed

    def create_command_embed(self, command):
        """Create embed for specific command - Economy category."""
        embeds = {
            "shop": discord.Embed(
                title="🛒 Item Shop",
                description=f"**Command:** `{self.prefix}shop [category]`\n\n"
                           "Browse and purchase equipment, items, and materials!\n\n"
                           "**Rarity System:**\n"
                           "⚪ Common → 🟢 Uncommon → 🔵 Rare → 🟣 Epic\n"
                           "🟠 Legendary → 🔴 Mythical → ⭐ Divine → 🌟 Cosmic\n\n"
                           "**Special Features:**\n"
                           "- Charisma affects shop prices\n"
                           "- Daily featured items with discounts\n"
                           "- Bulk purchase options",
                color=COLORS['primary']
            ),
            "inventory": discord.Embed(
                title="🎒 Interactive Inventory System",
                description=f"**Command:** `{self.prefix}inventory` or `{self.prefix}inv`\n\n"
                           "Revolutionary interactive inventory management with Plagg's commentary!\n\n"
                           "**Features:**\n"
                           "- **Category Filtering**: Weapons, Armor, Consumables, Kwami Artifacts, Materials\n"
                           "- **Rarity Organization**: Items grouped by rarity with visual indicators\n"
                           "- **Interactive Pagination**: Navigate large inventories with ease\n"
                           "- **Detailed Item Inspection**: Complete stats, effects, and Plagg's sarcastic commentary\n"
                           "- **One-Click Actions**: Use, equip, compare, and sellwith interactive buttons\n"
                           "- **EquipmentComparison**: Side-by-side stat comparisons before equipping\n"
                           "- **Smart Item Management**: Automatically handles equipment swapping\n\n"
                           "**Related Commands:**\n"
                           f"• `{self.prefix}use <item>` - Quick use consumables from command line\n"
                           f"• `{self.prefix}equip <item>` - Quick equip weapons/armor from command line\n"
                           f"• `{self.prefix}equipment` - View currently equipped gear overview",
                color=COLORS['secondary']
            ),
            "craft": discord.Embed(
                title="🔨 Crafting System",
                description=f"**Command:** `{self.prefix}craft <recipe>` or `{self.prefix}forge`\n\n"
                           "Create powerful equipment and enhance your gear!\n\n"
                           "**Related Commands:**\n"
                           f"`{self.prefix}recipes` - View known recipes\n"
                           f"`{self.prefix}materials` - Check crafting materials\n"
                           f"`{self.prefix}enhance <item>` - Upgrade equipment",
                color=COLORS['warning']
            ),
            "sell": discord.Embed(
                title="💰 Item Selling",
                description=f"**Command:** `{self.prefix}sell <item> [quantity]`\n\n"
                           "Convert unwanted items into gold!\n\n"
                           "**Examples:**\n"
                           f"`{self.prefix}sell iron_sword` - Sell one iron sword\n"
                           f"`{self.prefix}sell health_potion 5` - Sell 5 health potions\n\n"
                           "**Warning:** Selling is permanent!",
                color=COLORS['info']
            ),
            "auction": discord.Embed(
                title="🏛️ Auction House System",
                description=f"**Commands:** `{self.prefix}auction`, `{self.prefix}market`\n\n"
                           "Player-driven trading system with bidding!\n\n"
                           "**Main Commands:**\n"
                           f"`{self.prefix}auction` - Browse active auctions\n"
                           f"`{self.prefix}sell <item> <qty> <bid> <hours>` - List items\n"
                           f"`{self.prefix}bid <auction_id> <amount>` - Place bid\n\n"
                           "**Features:**\n"
                           "- Interactive browsing with filters\n"
                           "- Automatic bidding system\n"
                           "- 5% auction house fee\n"
                           "- 24-168 hour duration options",
                color=COLORS['gold']
            )
        }
        return embeds.get(command, self.create_embed())

class EconomyQuickActionsView(discord.ui.View):
    """Quick action buttons for economy commands."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    # Implement button actions for shop, inventory, etc.
    # Example:
    # @discord.ui.button(label="Shop", style=discord.ButtonStyle.secondary, emoji="🛒")
    # async def shop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     ...

    @discord.ui.button(label="🏠 Back to Help", style=discord.ButtonStyle.primary, row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class PvPMenuView(discord.ui.View):
    """PvP and competitive menu."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    @discord.ui.select(
        placeholder="🏆 PvP & Arena Combat",
        options=[
            discord.SelectOption(
                label="⚔️ Arena Queue",
                value="arena",
                description="arena - Enter ranked PvP battles",
                emoji="⚔️"
            ),
            discord.SelectOption(
                label="🤺 Challenge Duel",
                value="duel",
                description="duel - Challenge another player",
                emoji="🤺"
            ),
            discord.SelectOption(
                label="🏆 Leaderboards",
                value="ranking",
                description="ranking - View arena rankings",
                emoji="🏆"
            )
        ]
    )
    async def command_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        command = select.values[0]
        embed = self.create_command_embed(command)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🏠 Main Menu", style=discord.ButtonStyle.secondary, row=1)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🎮 Quick Actions", style=discord.ButtonStyle.primary, row=1)
    async def quick_actions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = PvPQuickActionsView(self.bot, self.prefix)
        embed = discord.Embed(
            title="🎮 PvP Quick Actions",
            description="**Use these buttons to quickly access PvP commands:**\n\n"
                       "Click the buttons below to instantly run commands without typing!",
            color=COLORS['success']
        )
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="📝 Try Commands", style=discord.ButtonStyle.primary, row=1)
    async def try_commands_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📝 PvP Commands Channel",
            description=f"**Try these PvP commands in this channel:**\n\n"
                       f"• `{self.prefix}arena` - Enter ranked arena\n"
                       f"• `{self.prefix}duel @user` - Challenge a player\n"
                       f"• `{self.prefix}ranking` - View leaderboards\n\n"
                       "**Click any command to try it right here!**",
            color=COLORS['success']
        )
        embed.set_footer(text="PvP Commands • Battle other players!")
        await interaction.response.edit_message(embed=embed, view=self)

    def create_embed(self):
        embed = discord.Embed(
            title="🏆 PvP & Competitive Combat",
            description="**Prove your worth against other warriors!**\n\n"
                       "Test your combat skills against other players in various competitive modes.\n\n"
                       "**PvP Features:**\n"
                       "- Ranked Arena with ELO rating system\n"
                       "- Direct player dueling challenges\n"
                       "- Faction-based large-scale warfare\n"
                       "- Seasonal tournaments and events\n"
                       "- Exclusive PvP rewards and titles\n\n"
                       "Only the strongest will claim the throne!",
            color=COLORS['error']
        )
        return embed

    def create_command_embed(self, command):
        """Create embed for specific command - PvP category."""
        embeds = {
            "arena": discord.Embed(
                title="⚔️ Arena Combat",
                description=f"**Command:** `{self.prefix}arena`\n\n"
                           "Enter the ranked arena for competitive PvP battles!\n\n"
                           "**Ranking Tiers:**\n"
                           "🥉 **Bronze** (800-1199): Starting tier\n"
                           "🥈 **Silver** (1200-1599): Skilled fighters\n"
                           "🥇 **Gold** (1600-1999): Elite combatants\n"
                           "💎 **Platinum** (2000-2399): Master warriors\n"
                           "🌟 **Diamond** (2400+): Legendary champions\n\n"
                           "**Rewards per Win:**\n"
                           "- 2-5 Gladiator Tokens\n"
                           "- Arena rating increase\n"
                           "- Experience and gold",
                color=COLORS['primary']
            ),
            "duel": discord.Embed(
                title="🤺 Player Dueling",
                description=f"**Command:** `{self.prefix}duel @user`\n\n"
                           "Challenge another player to a direct combat duel!\n\n"
                           "**Duel Types:**\n"
                           "- **Friendly:** No stakes, practice only\n"
                           "- **Ranked:** Affects arena rating\n"
                           "- **Wagered:** Gold or items at stake\n"
                           "- **Tournament:** Organized brackets\n\n"
                           "**Duel Rules:**\n"
                           "- Both players must accept\n"
                           "- Full tactical combat mechanics\n"
                           "- Cooldown after each duel",
                color=COLORS['warning']
            ),
            "ranking": discord.Embed(
                title="🏆 Arena Leaderboards",
                description=f"**Command:** `{self.prefix}ranking [type]`\n\n"
                           "View the greatest warriors in various categories!\n\n"
                           "**Leaderboard Types:**\n"
                           "- **Arena:** Highest rated PvP players\n"
                           "- **Level:** Highest level characters\n"
                           "- **Wealth:** Richest players by gold\n"
                           "- **Power:** Highest combat power\n"
                           "- **Wins:** Most arena victories\n\n"
                           "**Rewards:**\n"
                           "Top players receive exclusive titles and bonuses!",
                color=COLORS['info']
            )
        }
        return embeds.get(command, self.create_embed())

class PvPQuickActionsView(discord.ui.View):
    """Quick action buttons for PvP commands."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    # Implement button actions for arena, duel, etc.
    # Example:
    # @discord.ui.button(label="Arena", style=discord.ButtonStyle.secondary, emoji="⚔️")
    # async def arena_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     ...

    @discord.ui.button(label="🏠 Back to Help", style=discord.ButtonStyle.primary, row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class AdvancedMenuView(discord.ui.View):
    """Advanced features menu."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    @discord.ui.select(
        placeholder="✨ Advanced Features",
        options=[
            discord.SelectOption(
                label="🏆 Achievements",
                value="achievements",
                description="achievements - Track your accomplishments",
                emoji="🏆"
            ),
            discord.SelectOption(
                label="✨ Kwami Artifacts",
                value="artifacts",
                description="artifacts - Manage artifact sets",
                emoji="✨"
            ),
            discord.SelectOption(
                label="👑 Titles & Prestige",
                value="titles",
                description="titles - Display your accomplishments",
                emoji="👑"
            )
        ]
    )
    async def command_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        command = select.values[0]
        embed = self.create_command_embed(command)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🏠 Main Menu", style=discord.ButtonStyle.secondary, row=1)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🎮 Quick Actions", style=discord.ButtonStyle.primary, row=1)
    async def quick_actions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = AdvancedQuickActionsView(self.bot, self.prefix)
        embed = discord.Embed(
            title="🎮 Advanced Quick Actions",
            description="**Use these buttons to quickly access advanced features:**\n\n"
                       "Click the buttons below to instantly run commands without typing!",
            color=COLORS['success']
        )
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="📝 Try Commands", style=discord.ButtonStyle.primary, row=1)
    async def try_commands_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📝 Advanced Commands Channel",
            description=f"**Try these advanced commands in this channel:**\n\n"
                       f"• `{self.prefix}achievements` - View your progress\n"
                       f"• `{self.prefix}artifacts` - Manage artifact sets\n"
                       f"• `{self.prefix}titles` - Display accomplishments\n\n"
                       "**Click any command to try it right here!**",
            color=COLORS['success']
        )
        embed.set_footer(text="Advanced Commands • Master the endgame!")
        await interaction.response.edit_message(embed=embed, view=self)

    def create_embed(self):
        embed = discord.Embed(
            title="✨ Advanced Features",
            description="**Master the deeper mysteries of power!**\n\n"
                       "Unlock the true potential of your character through advanced systems.\n\n"
                       "**Advanced Systems:**\n"
                       "- Achievement tracking with tier-based rewards\n"
                       "- Kwami Artifacts with powerful set bonuses\n"
                       "- Prestige titles and cosmetic displays\n"
                       "- Equipment enhancement and upgrading\n\n"
                       "These features separate masters from novices!",
            color=COLORS['legendary']
        )
        return embed

    def create_command_embed(self, command):
        """Create embed for specific command - Advanced category."""
        embeds = {
            "achievements": discord.Embed(
                title="🏆 Achievement System",
                description=f"**Command:** `{self.prefix}achievements`\n\n"
                           "Track your accomplishments and unlock exclusive rewards!\n\n"
                           "**Achievement Tiers:**\n"
                           "🥉 **Bronze:** Basic milestones (XP, Gold bonuses)\n"
                           "🥈 **Silver:** Moderate challenges (Item rewards)\n"
                           "🥇 **Gold:** Significant accomplishments (Equipment)\n"
                           "💎 **Platinum:** Major feats (Titles, Skills)\n"
                           "🌟 **Legendary:** Epic achievements (Class unlocks)\n"
                           "✨ **Mythic:** Ultimate mastery (Unique abilities)\n\n"
                           "**Progress Tracking:** Real-time updates with percentages",
                color=COLORS['primary']
            ),
            "artifacts": discord.Embed(
                title="✨ Kwami Artifact System",
                description=f"**Command:** `{self.prefix}artifacts`\n\n"
                           "Harness the power of ancient Kwami artifacts!\n\n"
                           "**Set Bonuses:**\n"
                           "- **2 pieces:** Minor stat improvements\n"
                           "- **4 pieces:** Significant combat bonuses\n"
                           "- **6 pieces:** Powerful passive abilities\n"
                           "- **Full Set:** Transformation ultimate skills\n\n"
                           "**Artifact Sources:**\n"
                           "- Miraculous Box expeditions\n"
                           "- High-level dungeon completions",
                color=COLORS['info']
            ),
            "titles": discord.Embed(
                title="👑 Titles & Prestige",
                description=f"**Command:** `{self.prefix}titles`\n\n"
                           "Display your greatest accomplishments for all to see!\n\n"
                           "**Title Examples:**\n"
                           "• 'The Destroyer' - 1000 PvP victories\n"
                           "• 'Dragonslayer' - Defeat the Ancient Dragon\n"
                           "• 'Master Merchant' - Earn 1,000,000 gold\n\n"
                           "**Active Title:** Appears next to your name\n"
                           "• Prestige Bonuses: Some titles provide stat boosts",
                color=COLORS['secondary']
            )
        }
        return embeds.get(command, self.create_embed())

class AdvancedQuickActionsView(discord.ui.View):
    """Quick action buttons for advanced commands."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    # Implement button actions for achievements, artifacts, etc.
    # Example:
    # @discord.ui.button(label="Achievements", style=discord.ButtonStyle.secondary, emoji="🏆")
    # async def achievements_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     ...

    @discord.ui.button(label="🏠 Back to Help", style=discord.ButtonStyle.primary, row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class AdminMenuView(discord.ui.View):
    """Admin and management menu."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    @discord.ui.select(
        placeholder="🔧 Admin & Management",
        options=[
            discord.SelectOption(
                label="⚙️ Server Settings",
                value="settings",
                description="Configure bot settings for your server",
                emoji="⚙️"
            ),
            discord.SelectOption(
                label="📊 Player Management",
                value="management",
                description="Manage player data and characters",
                emoji="📊"
            ),
            discord.SelectOption(
                label="🛡️ Moderation Tools",
                value="moderation",
                description="Moderation and anti-abuse systems",
                emoji="🛡️"
            )
        ]
    )
    async def category_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        category = select.values[0]
        embed = self.create_command_embed(category)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🏠 Main Menu", style=discord.ButtonStyle.secondary, row=1)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="🎮 Quick Actions", style=discord.ButtonStyle.primary, row=1)
    async def quick_actions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = AdminQuickActionsView(self.bot, self.prefix)
        embed = discord.Embed(
            title="🎮 Admin Quick Actions",
            description="**Use these buttons to quickly access admin commands:**\n\n"
                       "Click the buttons below to instantly run commands without typing!",
            color=COLORS['success']
        )
        await interaction.response.edit_message(embed=embed, view=view)

    def create_command_embed(self, category):
        embeds = {
            "settings": discord.Embed(
                title="⚙️ Server Settings",
                description="Configure bot settings for your server.",
                color=COLORS['primary']
            ),
            "management": discord.Embed(
                title="📊 Player Management",
                description="Manage player data and characters.",
                color=COLORS['info']
            ),
            "moderation": discord.Embed(
                title="🛡️ Moderation Tools",
                description="Moderation and anti-abuse systems.",
                color=COLORS['error']
            )
        }
        return embeds.get(category, discord.Embed(title="Error", description="Invalid category.", color=COLORS['error']))

class AdminQuickActionsView(discord.ui.View):
    """Quick action buttons for admin commands."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=300)
        self.bot = bot
        self.prefix = prefix

    @discord.ui.button(label="⚙️ Settings", style=discord.ButtonStyle.secondary, emoji="⚙️")
    async def settings_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        # Create a fake message for context
        fake_message = interaction.message
        fake_message.content = f"{self.prefix}settings"
        fake_message.author = interaction.user

        ctx = await self.bot.get_context(fake_message)
        # Assuming you have a 'settings' command
        command = self.bot.get_command('settings')

        if command:
            try:
                await command(ctx)
            except Exception as e:
                await interaction.followup.send(f"❌ Error running settings command: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send("❌ Settings command not found!", ephemeral=True)

    @discord.ui.button(label="📊 Management", style=discord.ButtonStyle.secondary, emoji="📊")
    async def management_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        # Create a fake message for context
        fake_message = interaction.message
        fake_message.content = f"{self.prefix}management"
        fake_message.author = interaction.user

        ctx = await self.bot.get_context(fake_message)
        # Assuming you have a 'management' command
        command = self.bot.get_command('management')

        if command:
            try:
                await command(ctx)
            except Exception as e:
                await interaction.followup.send(f"❌ Error running management command: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send("❌ Management command not found!", ephemeral=True)

    @discord.ui.button(label="🛡️ Moderation", style=discord.ButtonStyle.danger, emoji="🛡️")
    async def moderation_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        # Create a fake message for context
        fake_message = interaction.message
        fake_message.content = f"{self.prefix}moderation"
        fake_message.author = interaction.user

        ctx = await self.bot.get_context(fake_message)
        # Assuming you have a 'moderation' command
        command = self.bot.get_command('moderation')

        if command:
            try:
                await command(ctx)
            except Exception as e:
                await interaction.followup.send(f"❌ Error running moderation command: {str(e)}", ephemeral=True)
        else:
            await interaction.followup.send("❌ Moderation command not found!", ephemeral=True)

    @discord.ui.button(label="🏠 Back to Help", style=discord.ButtonStyle.primary, row=1)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

class TutorialView(discord.ui.View):
    """Interactive tutorial system for new players."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=600)
        self.bot = bot
        self.prefix = prefix
        self.current_step = 0
        self.total_steps = 6

    @discord.ui.button(label="📖 Start Tutorial", style=discord.ButtonStyle.success, row=0)
    async def start_tutorial(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_step = 1
        embed = self.create_tutorial_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="⬅️ Previous", style=discord.ButtonStyle.secondary, row=1)
    async def previous_step(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_step > 1:
            self.current_step -= 1
            embed = self.create_tutorial_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("❌ You're already at the first step!", ephemeral=True)

    @discord.ui.button(label="➡️ Next", style=discord.ButtonStyle.primary, row=1)
    async def next_step(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_step < self.total_steps:
            self.current_step += 1
            embed = self.create_tutorial_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            embed = discord.Embed(
                title="🎉 Tutorial Complete!",
                description="Congratulations! You've completed the tutorial.\n\n"
                           "You're now ready to begin your epic adventure!\n\n"
                           "**Quick Start:**\n"
                           f"• `{self.prefix}startrpg` - Create your character\n"
                           f"• `{self.prefix}battle` - Start your first combat\n"
                           f"• `{self.prefix}help` - Return to this menu anytime",
                color=COLORS['success']
            )
            await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="🏠 Main Menu", style=discord.ButtonStyle.secondary, row=1)
    async def back_to_menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    def create_tutorial_embed(self):
        steps = {
            1: {
                "title": "📖 Step 1: Creating Your Character",
                "description": f"**Welcome to Project: Blood & Cheese!**\n\n"
                              f"Your journey begins with creating a character. Use the command:\n"
                              f"`{self.prefix}startrpg`\n\n"
                              "**What happens:**\n"
                              "- Interactive class selection menu appears\n"
                              "- Choose from 7 unique classes\n"
                              "- Each class has different roles and abilities\n"
                              "- Your choice affects your entire adventure\n\n"
                              "**Tip:** Read each class description carefully!"
            },
            2: {
                "title": "⚔️ Step 2: Understanding Combat",
                "description": f"**Combat is the heart of this game!**\n\n"
                              f"Use `{self.prefix}battle` to enter tactical combat:\n\n"
                              "**Combat Mechanics:**\n"
                              "- **Skill Points (SP):** Generate with basic attacks\n"
                              "- **Ultimate Energy:** Build up for powerful abilities\n"
                              "- **Weakness Break:** Hit enemy weaknesses to stun them\n"
                              "- **Follow-up Attacks:** Chain attacks for bonus damage\n\n"
                              "**Strategy:** Balance basic attacks to generate SP with skills to deal damage!"
            },
            3: {
                "title": "📈 Step 3: Character Progression",
                "description": f"**Grow stronger through experience and smart choices!**\n\n"
                              "**Leveling System:**\n"
                              "- Gain XP from combat victories\n"
                              "- Level up to increase stats automatically\n"
                              "- Earn stat points to allocate manually\n\n"
                              "**Stat Allocation:**\n"
                              f"Use `{self.prefix}allocate` to distribute points:\n"
                              "- **Strength:** Physical damage\n"
                              "- **Dexterity:** Critical hits and dodge\n"
                              "- **Constitution:** Max HP and defense\n"
                              "- **Intelligence:** Magic damage and MP\n"
                              "- **Wisdom:** Healing and MP regen\n"
                              "- **Charisma:** Social bonuses and prices"
            },
            4: {
                "title": "🛒 Step 4: Economy & Equipment",
                "description": f"**Manage your resources and gear wisely!**\n\n"
                              "**Key Commands:**\n"
                              f"• `{self.prefix}shop` - Browse and buy equipment\n"
                              f"• `{self.prefix}inventory` - Manage your items\n"
                              f"• `{self.prefix}equip <item>` - Equip weapons and armor\n"
                              f"• `{self.prefix}sell <item>` - Convert items to gold\n\n"
                              "**Rarity System:**\n"
                              "⚪ Common → 🟢 Uncommon → 🔵 Rare → 🟣 Epic\n"
                              "🟠 Legendary → 🔴 Mythical → ⭐ Divine → 🌟 Cosmic\n\n"
                              "**Tip:** Higher rarity items have better stats!"
            },
            5: {
                "title": "🏰 Step 5: Adventures & Exploration",
                "description": f"**Explore the world and discover treasures!**\n\n"
                              "**Adventure Types:**\n"
                              f"• `{self.prefix}hunt` - Search for monsters (30min cooldown)\n"
                              f"• `{self.prefix}dungeon <name>` - Explore multi-floor dungeons\n"
                              f"• `{self.prefix}miraculous` - Farm Kwami Artifacts\n"
                              f"• `{self.prefix}arena` - Challenge other players\n\n"
                              "**Special Features:**\n"
                              "• Miraculous Paths: Choose at Level 20\n"
                              "• Hidden Classes: Unlock through achievements\n"
                              "• Artifacts: Powerful set equipment\n"
                              "• Achievements: Track your accomplishments"
            },
            6: {
                "title": "🎯 Step 6: Advanced Tips",
                "description": "**Master these concepts to excel!**\n\n"
                              "**Strategic Tips:**\n"
                              "- Balance offense and defense in stat allocation\n"
                              "- Save gold for higher-tier equipment\n"
                              "- Complete daily hunts for consistent progress\n"
                              "- Experiment with different combat strategies\n\n"
                              "**Warning System:**\n"
                              "⚠️ **The bot warns you about risky actions but won't stop you**\n"
                              "- Selling valuable items\n"
                              "- Making permanent choices\n"
                              "- Resource-intensive actions\n\n"
                              "**Remember:** Your choices shape your adventure!"
            }
        }

        step_data = steps[self.current_step]
        embed = discord.Embed(
            title=step_data["title"],
            description=step_data["description"],
            color=COLORS['primary']
        )

        embed.set_footer(text=f"Tutorial Step {self.current_step} of {self.total_steps}")
        return embed

class InfoPanelView(discord.ui.View):
    """Comprehensive information panels for game mechanics."""

    def __init__(self, bot, prefix="$"):
        super().__init__(timeout=600)
        ```python
        self.bot = bot
        self.prefix = prefix

    @discord.ui.select(
        placeholder="📚 Choose information topic...",
        options=[
            discord.SelectOption(
                label="⚔️ Combat Mechanics",
                value="combat",
                description="Detailed combat system explanation",
                emoji="⚔️"
            ),
            discord.SelectOption(
                label="📊 Character Stats",
                value="stats",
                description="Complete stat system breakdown",
                emoji="📊"
            ),
            discord.SelectOption(
                label="🎯 Rarity System",
                value="rarity",
                description="Item rarity and quality explained",
                emoji="🎯"
            ),
            discord.SelectOption(
                label="🌟 Paths & Classes",
                value="paths",
                description="Classes and Miraculous Paths guide",
                emoji="🌟"
            )
        ]
    )
    async def info_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        topic = select.values[0]
        embed = self.create_info_embed(topic)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🏠 Main Menu", style=discord.ButtonStyle.secondary, row=1)
    async def back_to_menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MainMenuView(self.bot, self.prefix)
        embed = view.create_main_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    def create_info_embed(self, topic):
        info_data = {
            "combat": {
                "title": "⚔️ Complete Combat Mechanics Guide",
                "description": "**Tactical Turn-Based Combat System**\n\n"
                              "**Core Resources:**\n"
                              "• **Skill Points (SP):** Start with 3, max 5. Generate 1 with basic attacks, spend 1 on skills\n"
                              "• **Ultimate Energy:** Builds from 0-100. Use ultimate abilities when full\n"
                              "• **Technique Points:** 3 per battle for pre-combat preparation\n\n"
                              "**Combat Flow:**\n"
                              "1. **Preparation Phase:** Use technique points for buffs\n"
                              "2. **Main Combat:** Alternate basic attacks and skills\n"
                              "3. **Strategic Decisions:** Manage SP for optimal damage\n"
                              "4. **Ultimate Timing:** Use ultimates at crucial moments\n\n"
                              "**Advanced Mechanics:**\n"
                              "• **Weakness Break:** Hit enemy weaknesses to stun and deal bonus damage\n"
                              "• **Follow-up Attacks:** Some abilities trigger additional attacks\n"
                              "• **Critical Hits:** Based on Dexterity, deals 1.5x damage\n"
                              "• **Dodge Chance:** Avoid damage entirely based on Dexterity"
            },
            "stats": {
                "title": "📊 Character Statistics Deep Dive",
                "description": "**Base Stats (Manually Allocated):**\n\n"
                              "**💪 Strength**\n"
                              "• +2 Attack per point\n"
                              "• Affects carrying capacity\n"
                              "• Required for heavy weapons\n\n"
                              "**🎯 Dexterity**\n"
                              "• +1% Crit Chance per point\n"
                              "• +0.5% Dodge Chance per point\n"
                              "• Affects turn order in combat\n\n"
                              "**❤️ Constitution**\n"
                              "• +10 Max HP per point\n"
                              "• +1% Damage Reduction per 2 points\n"
                              "• Affects status resist chance\n\n"
                              "**🧠 Intelligence**\n"
                              "• +2 Magic Attack per point\n"
                              "• +5 Max MP per point\n"
                              "• Required for advanced spells\n\n"
                              "**🔮 Wisdom**\n"
                              "• +1.5 Healing Power per point\n"
                              "• +1 MP Regeneration per 2 points\n"
                              "• Affects magical defense\n\n"
                              "**✨ Charisma**\n"
                              "• -1% Shop Prices per point (max 25%)\n"
                              "• +2% Hunt Success per point\n"
                              "• Affects social interactions"
            },
            "rarity": {
                "title": "🎯 Item Rarity & Quality System",
                "description": "**8-Tier Rarity System:**\n\n"
                              "⚪ **Common (1.0x)** - Basic items, easy to find\n"
                              "• Drop Rate: 40% • Stat Multiplier: 1.0x\n\n"
                              "🟢 **Uncommon (1.2x)** - Slightly better stats\n"
                              "• Drop Rate: 25% • Stat Multiplier: 1.2x\n\n"
                              "🔵 **Rare (1.5x)** - Noticeable improvements\n"
                              "• Drop Rate: 15% • Stat Multiplier: 1.5x\n\n"
                              "🟣 **Epic (2.0x)** - Significant power boost\n"
                              "• Drop Rate: 10% • Stat Multiplier: 2.0x\n\n"
                              "🟠 **Legendary (3.0x)** - Exceptional equipment\n"
                              "• Drop Rate: 5% • Stat Multiplier: 3.0x\n\n"
                              "🔴 **Mythical (4.5x)** - Nearly godlike power\n"
                              "• Drop Rate: 2% • Stat Multiplier: 4.5x\n\n"
                              "⭐ **Divine (7.0x)** - Divine artifacts\n"
                              "• Drop Rate: 0.5% • Stat Multiplier: 7.0x\n\n"
                              "🌟 **Cosmic (10.0x)** - Reality-breaking items\n"
                              "• Drop Rate: 0.1% • Stat Multiplier: 10.0x"
            },
            "paths": {
                "title": "🌟 Classes & Miraculous Paths",
                "description": "**Character Classes (Level 1):**\n\n"
                              "🛡️ **Warrior** - Tank specialist with high defense\n"
                              "🔮 **Mage** - Magic DPS with area attacks\n"
                              "🗡️ **Rogue** - Critical strike assassin\n"
                              "🏹 **Archer** - Ranged precision striker\n"
                              "❤️ **Healer** - Support with healing abilities\n"
                              "⚔️ **Battlemage** - Hybrid melee/magic fighter\n"
                              "⏰ **Chrono Knight** - Time manipulation (Hidden)\n\n"
                              "**Miraculous Paths (Level 20+):**\n\n"
                              "💥 **Path of Destruction**\n"
                              "• +20% Critical Damage\n"
                              "• Enhanced follow-up attacks\n"
                              "• Execution bonuses vs low HP enemies\n\n"
                              "🛡️ **Path of Preservation**\n"
                              "• +15% Damage Reduction\n"
                              "• Shield generation abilities\n"
                              "• Enhanced defensive buffs\n\n"
                              "❤️‍🩹 **Path of Abundance**\n"
                              "• +25% Healing Power\n"
                              "• Enhanced buff effects\n"
                              "• Team support synergies\n\n"
                              "🎯 **Path of The Hunt**\n"
                              "• Execute enemies below 25% HP\n"
                              "• +15% Accuracy\n"
                              "• Single-target damage mastery"
            }
        }

        data = info_data.get(topic, info_data["combat"])
        embed = discord.Embed(
            title=data["title"],
            description=data["description"],
            color=COLORS['info']
        )

        embed.set_footer(text="💡 Use this information to master the game!")
        return embed

def get_item_source_guide(item_key):
    """Get the item source guide for an item."""
    # Mock Data - Replace with actual database logic later
    SOURCES = {
        "iron_sword": "Obtained from the shop or by defeating goblins in the Goblin Caves.",
        "health_potion": "Bought from the shop or found in treasure chests during exploration.",
        "dragon_scale_mail": "Dropped by the Ancient Dragon in the Dragon's Lair.",
        "goblin_club": "Dropped by goblins",
        "rusty_dagger": "Commonly found during exploration"
    }

    return SOURCES.get(item_key, "Source information not available for this item.")

def get_source_locations():
    """Return description of item sources."""
    SOURCES = {
        "shop": "Buy weapons, armor, and potions from the shop.",
        "dungeon": "Explore dungeons and find rare artifacts.",
        "hunt": "Hunt monsters for equipment drops.",
        "crafting": "Craft powerful equipment",
        "exploration": "Discover new locations",
        "arena": "Win arena battles"
    }
    return SOURCES

def search_items_by_source(source):
    """Search items based on the source."""
    from rpg_data.game_data import ITEMS

    items_found = {}
    for item_key, item_data in ITEMS.items():
        sources = item_data.get('sources', [])
        if source in sources:
            items_found[item_key] = item_data
    return items_found

class HelpCog(commands.Cog):
    """Interactive help system with comprehensive UI."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h", "commands", "menu"])
    async def help_command(self, ctx):
        """Display the interactive help menu with full navigation."""
        if not is_module_enabled("rpg", ctx.guild.id):
            return

        # Get server configuration for prefix
        config = get_server_config(ctx.guild.id)
        prefix = config.get('prefix', '$')

        view = MainMenuView(self.bot, prefix)
        embed = view.create_main_embed()

        await ctx.send(embed=embed, view=view)

    @commands.command(name="tutorial", aliases=["guide", "walkthrough"])
    async def tutorial_command(self, ctx):
        """Start the interactive tutorial for new players."""
        # Get server configuration for prefix
        config = get_server_config(ctx.guild.id)
        prefix = config.get('prefix', '$')

        embed = discord.Embed(
            title="📖 Interactive Tutorial System",
            description="**Welcome to the comprehensive tutorial!**\n\n"
                       "This step-by-step guide will teach you everything you need "
                       "to know about playing Project: Blood & Cheese.\n\n"
                       "**What you'll learn:**\n"
                       "- Character creation and classes\n"
                       "- Combat mechanics and strategy\n"
                       "- Character progression and stats\n"
                       "- Economy and equipment\n"
                       "- Adventures and exploration\n"
                       "- Advanced tips and warnings\n\n"
                       "Click **Start Tutorial** to begin!",
            color=COLORS['primary']
        )

        embed.set_footer(text="Tutorial • Interactive Learning Experience")

        view = TutorialView(self.bot, prefix)
        await ctx.send(embed=embed, view=view)

    @commands.command(name="info", aliases=["gameinfo", "mechanics", "nerd"])
    async def info_command(self, ctx):
        """Display detailed game information panels for advanced players."""
        # Get server configuration for prefix
        config = get_server_config(ctx.guild.id)
        prefix = config.get('prefix', '$')

        embed = discord.Embed(
            title="📚 Game Information Database",
            description="**Comprehensive game mechanics reference!**\n\n"
                       "This information system provides detailed breakdowns of all "
                       "game mechanics, formulas, and systems for players who want "
                       "to understand the game at a deeper level.\n\n"
                       "**Available Topics:**\n"
                       "- Combat mechanics and formulas\n"
                       "- Character statistics and effects\n"
                       "- Item rarity and quality systems\n"
                       "- Classes and Miraculous Paths\n\n"
                       "**Perfect for:** Min-maxers, theorycrafters, and curious players!",
            color=COLORS['info']
        )

        embed.set_footer(text="Information Database • For the Nerds 🤓")

        view = InfoPanelView(self.bot, prefix)
        await ctx.send(embed=embed, view=view)

    @commands.command(name="quickhelp", aliases=["qh"])
    async def quick_help(self, ctx):
        """Display a quick reference for essential commands."""
        # Get server configuration for prefix
        config = get_server_config(ctx.guild.id)
        prefix = config.get('prefix', '$')

        embed = discord.Embed(
            title="⚡ Quick Command Reference",
            description="**Essential commands to get started:**",
            color=COLORS['primary']
        )

        embed.add_field(
            name="🎭 Character Basics",
            value=f"`{prefix}start` - Create character\n"
                  f"`{prefix}me` - View stats\n"
                  f"`{prefix}fight` - Fight monsters\n"
                  f"`{prefix}allocate` - Upgrade stats",
            inline=True
        )

        embed.add_field(
            name="🛒 Economy",
            value=f"`{prefix}store` - Browse items\n"
                  f"`{prefix}inv` - View items\n"
                  f"`{prefix}auction` - Player market\n"
                  f"`{prefix}sell <item>` - Quick sell",
            inline=True
        )

        embed.add_field(
            name="🏰 Adventures",
            value=f"`{prefix}hunt` - Find monsters\n"
                  f"`{prefix}dungeon <name>` - Enter dungeons\n"
                  f"`{prefix}miraculous` - Artifact farming\n"
                  f"`{prefix}arena` - PvP battles",
            inline=True
        )

        embed.add_field(
            name="📚 Learning",
            value=f"`{prefix}tutorial` - Interactive tutorial\n"
                  f"`{prefix}info` - Game mechanics database\n"
                  f"`{prefix}help` - Full interactive menu\n"
                  "@Plagg - Chat with AI Plagg!",
            inline=True
        )

        embed.set_footer(text=f"Use {prefix}help for the full interactive menu!")
        await ctx.send(embed=embed)

    @commands.command(name="itemsource", aliases=["source", "howtoget"])
    async def item_source(self, ctx, *, item_name: str = None):
        """Get detailed information on how to obtain any item."""
        if not item_name:
            embed = discord.Embed(
                title="🔍 Item Source Lookup",
                description="**Find out how to get any item!**\n\n"
                           f"**Usage:** `{ctx.prefix}itemsource <item name>`\n"
                           f"**Example:** `{ctx.prefix}itemsource dragon scale mail`\n\n"
                           f"**You can also search by source:**\n"
                           f"`{ctx.prefix}itemsource shop` - All shop items\n"
                           f"`{ctx.prefix}itemsource boss` - All boss drops\n"
                           f"`{ctx.prefix}itemsource arena` - All arena rewards",
                color=COLORS['info']
            )

            source_list = ""
            sources = get_source_locations()
            for source, desc in list(sources.items())[:10]:  # First 10 sources
                source_list += f"• **{source}** - {desc}\n"

            embed.add_field(name="Available Sources", value=source_list, inline=False)
            await ctx.send(embed=embed)
            return

        # Check if it's a source type search
        sources = get_source_locations()
        if item_name.lower() in sources:
            source_items = search_items_by_source(item_name.lower())

            embed = discord.Embed(
                title=f"📦 Items from: {item_name.title()}",
                description=f"**{sources[item_name.lower()]}**\n\n"
                           f"**Found {len(source_items)} items:**",
                color=COLORS['primary']
            )

            items_text = ""
            for item_key, item_data in list(source_items.items())[:15]:  # Limit to 15 items
                rarity_emoji = {'common': '⚪', 'uncommon': '🟢', 'rare': '🔵', 'epic': '🟣', 'legendary': '🟠'}.get(item_data.get('rarity', 'common'), '⚪')
                items_text += f"{rarity_emoji} {item_data['name']}\n"

            if len(source_items) > 15:
                items_text += f"... and {len(source_items) - 15} more items"

            embed.add_field(name="Available Items", value=items_text or "No items found", inline=False)
            await ctx.send(embed=embed)
            return

        # Search for specific item
        from rpg_data.game_data import ITEMS

        # Find item by name
        item_key = None
        item_name_lower = item_name.lower()

        for key, data in ITEMS.items():
            if (item_name_lower in data.get('name', '').lower() or 
                item_name_lower in key.lower()):
                item_key = key
                break

        if not item_key:
            embed = discord.Embed(
                title="❌ Item Not Found",
                description=f"Could not find an item matching '{item_name}'.\n\n"
                           f"**Try:**\n"
                           f"• Using the exact item name\n"
                           f"• Checking spelling\n"
                           f"• Using partial names (e.g., 'dragon' for dragon items)",
                color=COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        # Get source guide
        guide = get_item_source_guide(item_key)

        embed = discord.Embed(
            title="🔍 Item Source Guide",
            description=guide,
            color=COLORS['info']
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))