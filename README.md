# 🧀 Plagg (Kwami of Destruction) Bot

A comprehensive Discord RPG bot featuring tactical combat, economy systems, and interactive gameplay.

## 📁 Project Structure

```
├── cogs/                   # Bot command modules
│   ├── admin.py           # Administrative commands
│   ├── ai_chatbot.py      # AI chat integration
│   ├── auction_house.py   # Player trading system
│   ├── economy.py         # Economy and jobs
│   ├── help.py            # Interactive help system
│   ├── moderation.py      # Moderation tools
│   ├── rpg_core.py        # Core RPG functionality
│   ├── rpg_combat.py      # Tactical combat system
│   ├── rpg_dungeons.py    # Dungeon exploration
│   ├── rpg_games.py       # Mini-games and activities
│   ├── rpg_inventory.py   # Inventory management
│   ├── rpg_items.py       # Item system
│   ├── rpg_pvp.py         # Player vs Player
│   └── rpg_shop.py        # Shop and trading
├── rpg_data/              # Game data and configuration
│   └── game_data.py       # Items, classes, monsters
├── utils/                 # Utility functions
│   ├── achievements.py    # Achievement tracking
│   ├── database.py        # Database management
│   ├── helpers.py         # Helper functions
│   ├── item_sources.py    # Item acquisition guide
│   └── warning_system.py  # Player guidance system
├── attached_assets/       # Screenshots and documentation
├── main.py               # Bot entry point
├── config.py             # Configuration settings
└── web_server.py         # Keep-alive server
```

## 🚀 Features

### RPG System
- **Character Classes**: 7 unique classes with distinct abilities
- **Tactical Combat**: Turn-based combat with SP and ultimate abilities
- **Interactive Dungeons**: Multi-floor adventures with dynamic encounters
- **Equipment System**: 8-tier rarity system with set bonuses
- **Achievement Tracking**: Progress tracking with tier-based rewards

### Economy
- **Shop System**: Buy and sell items with dynamic pricing
- **Auction House**: Player-to-player trading
- **Interactive Inventory**: Advanced item management with categories
- **Crafting System**: Create and enhance equipment

### Social Features
- **AI Chatbot**: Chat with Plagg using advanced AI
- **Help System**: Comprehensive interactive help menus
- **Admin Tools**: Server management and moderation

## 🛠️ Setup

1. Set your Discord bot token in environment variables
2. Configure database settings in `config.py`
3. Run `python main.py` to start the bot

## 📝 Usage

- `$help` - Interactive help system
- `$startrpg` - Create your character
- `$battle` - Engage in tactical combat
- `$shop` - Browse the item shop
- `$inventory` - Manage your items

## 🐛 Troubleshooting

Check the console output for any module loading errors. The bot includes self-healing mechanisms and detailed error logging.

## 📄 License

See LICENSE file for details.
```├── cogs/                   # Bot command modules
│   ├── admin.py           # Administrative commands
│   ├── ai_chatbot.py      # AI chat integration
│   ├── auction_house.py   # Player trading system
│   ├── economy.py         # Economy and jobs
│   ├── help.py            # Interactive help system
│   ├── moderation.py      # Moderation tools
│   ├── rpg_core.py        # Core RPG functionality
│   ├── rpg_combat.py      # Tactical combat system
│   ├── rpg_dungeons.py    # Dungeon exploration
│   ├── rpg_games.py       # Mini-games and activities
│   ├── rpg_inventory.py   # Inventory management
│   ├── rpg_items.py       # Item system
│   ├── rpg_pvp.py         # Player vs Player
│   └── rpg_shop.py        # Shop and trading
├── rpg_data/              # Game data and configuration
│   └── game_data.py       # Items, classes, monsters
├── utils/                 # Utility functions
│   ├── achievements.py    # Achievement tracking
│   ├── database.py        # Database management
│   ├── helpers.py         # Helper functions
│   ├── item_sources.py    # Item acquisition guide
│   └── warning_system.py  # Player guidance system
├── attached_assets/       # Screenshots and documentation
├── main.py               # Bot entry point
├── config.py             # Configuration settings
└── web_server.py         # Keep-alive server