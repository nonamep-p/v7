"""
Comprehensive game data for Project: Blood & Cheese RPG system.
Contains all classes, paths, items, monsters, and game mechanics.
"""

import discord
from typing import Dict, Any, List, Optional
from datetime import datetime

# Character Classes
CLASSES = {
    'warrior': {
        'name': 'Warrior',
        'emoji': '🛡️',
        'description': 'A mighty tank with high defense and protective abilities',
        'role': 'Tank',
        'base_hp': 120,
        'base_mp': 40,
        'starting_stats': {
            'strength': 15,
            'dexterity': 8,
            'constitution': 18,
            'intelligence': 6,
            'wisdom': 8,
            'charisma': 10
        },
        'starting_skills': ['power_strike', 'shield_bash'],
        'passive_name': 'Fortress',
        'passive_description': '+20% damage reduction, immune to critical hits'
    },
    'mage': {
        'name': 'Mage',
        'emoji': '🔮',
        'description': 'A powerful spellcaster with devastating magical attacks',
        'role': 'DPS',
        'base_hp': 80,
        'base_mp': 100,
        'starting_stats': {
            'strength': 6,
            'dexterity': 10,
            'constitution': 8,
            'intelligence': 18,
            'wisdom': 15,
            'charisma': 8
        },
        'starting_skills': ['fireball', 'ice_lance'],
        'passive_name': 'Arcane Mastery',
        'passive_description': '+30% magical damage, spells cost 20% less mana'
    },
    'rogue': {
        'name': 'Rogue',
        'emoji': '🗡️',
        'description': 'A swift assassin with high critical hit chance',
        'role': 'DPS',
        'base_hp': 100,
        'base_mp': 60,
        'starting_stats': {
            'strength': 12,
            'dexterity': 18,
            'constitution': 10,
            'intelligence': 8,
            'wisdom': 6,
            'charisma': 12
        },
        'starting_skills': ['backstab', 'poison_strike'],
        'passive_name': 'Shadow Strike',
        'passive_description': '+25% critical chance, +50% critical damage'
    },
    'archer': {
        'name': 'Archer',
        'emoji': '🏹',
        'description': 'A precise ranged fighter with deadly accuracy',
        'role': 'DPS',
        'base_hp': 90,
        'base_mp': 70,
        'starting_stats': {
            'strength': 10,
            'dexterity': 16,
            'constitution': 12,
            'intelligence': 10,
            'wisdom': 12,
            'charisma': 10
        },
        'starting_skills': ['piercing_shot', 'multi_shot'],
        'passive_name': 'Eagle Eye',
        'passive_description': '+30% accuracy, immune to dodge'
    },
    'healer': {
        'name': 'Healer',
        'emoji': '❤️',
        'description': 'A supportive ally with powerful healing abilities',
        'role': 'Support',
        'base_hp': 95,
        'base_mp': 90,
        'starting_stats': {
            'strength': 8,
            'dexterity': 10,
            'constitution': 12,
            'intelligence': 12,
            'wisdom': 18,
            'charisma': 15
        },
        'starting_skills': ['heal', 'blessing'],
        'passive_name': 'Divine Grace',
        'passive_description': '+40% healing power, regenerate 5 MP per turn'
    },
    'battlemage': {
        'name': 'Battlemage',
        'emoji': '⚔️',
        'description': 'A hybrid fighter combining magic and melee combat',
        'role': 'Hybrid',
        'base_hp': 105,
        'base_mp': 80,
        'starting_stats': {
            'strength': 13,
            'dexterity': 10,
            'constitution': 13,
            'intelligence': 15,
            'wisdom': 10,
            'charisma': 9
        },
        'starting_skills': ['flame_slash', 'magic_weapon'],
        'passive_name': 'Spellsword',
        'passive_description': 'Weapons deal magical damage, +15% spell power'
    },
    'chrono_knight': {
        'name': 'Chrono Knight',
        'emoji': '⏰',
        'description': 'A mysterious warrior who manipulates time itself',
        'role': 'Hidden',
        'base_hp': 110,
        'base_mp': 85,
        'starting_stats': {
            'strength': 14,
            'dexterity': 14,
            'constitution': 14,
            'intelligence': 14,
            'wisdom': 14,
            'charisma': 14
        },
        'starting_skills': ['time_warp', 'temporal_strike'],
        'passive_name': 'Temporal Mastery',
        'passive_description': '20% chance to act twice per turn'
    }
}

# Miraculous Paths
PATHS = {
    'destruction': {
        'name': 'Path of Destruction',
        'emoji': '💥',
        'description': 'Pure offensive power that devastates enemies',
        'bonus_1': '+20% Critical Damage',
        'bonus_2': '30% chance for follow-up attacks on weakness break',
        'bonus_3': 'Execute enemies below 20% HP'
    },
    'preservation': {
        'name': 'Path of Preservation', 
        'emoji': '🛡️',
        'description': 'Defensive mastery that protects allies',
        'bonus_1': '+15% Damage Reduction',
        'bonus_2': 'Generate shields when taking damage',
        'bonus_3': 'Team gets +10% damage reduction'
    },
    'abundance': {
        'name': 'Path of Abundance',
        'emoji': '❤️‍🩹',
        'description': 'Support excellence that empowers the team',
        'bonus_1': '+25% Healing Power',
        'bonus_2': 'Buffs last 50% longer',
        'bonus_3': 'Healing grants temporary HP bonus'
    },
    'hunt': {
        'name': 'Path of The Hunt',
        'emoji': '🎯',
        'description': 'Precision strikes that hunt down prey',
        'bonus_1': 'Execute enemies below 25% HP',
        'bonus_2': '+15% Accuracy and cannot miss',
        'bonus_3': '+20% damage to wounded enemies'
    }
}

# Damage Types
DAMAGE_TYPES = {
    'physical': '⚔️',
    'fire': '🔥',
    'ice': '🧊',
    'lightning': '⚡',
    'quantum': '🌌',
    'imaginary': '👻'
}

# Techniques
TECHNIQUES = {
    'ambush': {
        'name': 'Ambush',
        'cost': 1,
        'description': 'Start combat with +2 Skill Points',
        'effect': {
            'type': 'skill_points',
            'amount': 2
        }
    },
    'preparation': {
        'name': 'Preparation',
        'cost': 2,
        'description': 'Start with 25 Ultimate Energy',
        'effect': {
            'type': 'ultimate_energy',
            'amount': 25
        }
    },
    'shield_wall': {
        'name': 'Shield Wall',
        'cost': 2,
        'description': 'Start with 50 shield points',
        'effect': {
            'type': 'shield',
            'amount': 50
        }
    }
}

# Synergy States
SYNERGY_STATES = {
    'riposte': {
        'name': 'Riposte',
        'emoji': '⚔️',
        'effect': 'riposte_damage',
        'description': 'Next basic attack deals bonus damage based on shield'
    },
    'opportunity': {
        'name': 'Opportunity',
        'emoji': '🎯',
        'effect': 'guaranteed_crit',
        'description': 'Next skill is guaranteed to critical hit'
    }
}

# Rarity Colors
RARITY_COLORS = {
    'common': 0x95a5a6,
    'uncommon': 0x2ecc71,
    'rare': 0x3498db,
    'epic': 0x9b59b6,
    'legendary': 0xff6b35,
    'mythical': 0xe74c3c,
    'divine': 0xf1c40f,
    'cosmic': 0xe91e63
}

# Items
ITEMS = {
    'health_potion': {
        'name': 'Health Potion',
        'type': 'consumable',
        'rarity': 'common',
        'heal': 60,
        'price': 25,
        'description': 'Restores 60 HP instantly'
    },
    'mana_potion': {
        'name': 'Mana Potion', 
        'type': 'consumable',
        'rarity': 'common',
        'restore_mp': 40,
        'price': 20,
        'description': 'Restores 40 MP instantly'
    },
    'iron_sword': {
        'name': 'Iron Sword',
        'type': 'weapon',
        'rarity': 'common',
        'attack': 15,
        'price': 100,
        'description': 'A sturdy iron blade'
    },
    'steel_armor': {
        'name': 'Steel Armor',
        'type': 'armor',
        'rarity': 'uncommon',
        'defense': 12,
        'price': 200,
        'description': 'Reliable steel protection'
    }
}

# Character Classes
CLASSES = {
    "warrior": {
        "name": "Warrior",
        "emoji": "🛡️",
        "role": "Tank",
        "description": "A stalwart defender with unbreakable resolve and protective instincts.",
        "base_hp": 120,
        "base_mp": 60,
        "starting_stats": {
            "strength": 8,
            "dexterity": 4,
            "constitution": 10,
            "intelligence": 3,
            "wisdom": 5,
            "charisma": 4
        },
        "starting_skills": ["Shield Bash", "Taunt", "Defensive Stance"],
        "passive_name": "Guardian's Resolve",
        "passive_description": "Reduces incoming damage by 15% and generates threat to protect allies.",
        "ultimate_name": "Fortress Wall",
        "ultimate_description": "Become immovable for 3 turns, reflecting 50% of damage back to attackers."
    },
    "mage": {
        "name": "Mage",
        "emoji": "🔮",
        "role": "Magic DPS",
        "description": "A master of arcane arts who bends reality to their will through powerful spells.",
        "base_hp": 80,
        "base_mp": 140,
        "starting_stats": {
            "strength": 3,
            "dexterity": 5,
            "constitution": 4,
            "intelligence": 10,
            "wisdom": 8,
            "charisma": 4
        },
        "starting_skills": ["Fireball", "Magic Missile", "Mana Shield"],
        "passive_name": "Arcane Mastery",
        "passive_description": "Spells have a 20% chance to not consume mana and deal bonus damage.",
        "ultimate_name": "Meteor Storm",
        "ultimate_description": "Rain magical destruction on all enemies for massive area damage."
    },
    "rogue": {
        "name": "Rogue",
        "emoji": "🗡️",
        "role": "Physical DPS",
        "description": "A shadowy assassin who strikes from darkness with lethal precision.",
        "base_hp": 90,
        "base_mp": 80,
        "starting_stats": {
            "strength": 6,
            "dexterity": 10,
            "constitution": 5,
            "intelligence": 4,
            "wisdom": 3,
            "charisma": 6
        },
        "starting_skills": ["Sneak Attack", "Poison Blade", "Shadow Step"],
        "passive_name": "Critical Mastery",
        "passive_description": "Critical hits deal 200% damage instead of 150% and have follow-up chance.",
        "ultimate_name": "Assassination",
        "ultimate_description": "Instantly kill enemies below 30% HP or deal 500% damage to stronger foes."
    },
    "archer": {
        "name": "Archer",
        "emoji": "🏹",
        "role": "Ranged DPS",
        "description": "A precise marksman who never misses their target with deadly accuracy.",
        "base_hp": 85,
        "base_mp": 90,
        "starting_stats": {
            "strength": 5,
            "dexterity": 9,
            "constitution": 6,
            "intelligence": 4,
            "wisdom": 6,
            "charisma": 4
        },
        "starting_skills": ["Power Shot", "Multi-Shot", "Hunter's Mark"],
        "passive_name": "Eagle Eye",
        "passive_description": "Cannot miss attacks and critical hits have 25% chance to not consume turn.",
        "ultimate_name": "Rain of Arrows",
        "ultimate_description": "Fire a volley that hits all enemies and pierces through armor."
    },
    "healer": {
        "name": "Healer",
        "emoji": "❤️",
        "role": "Support",
        "description": "A divine practitioner who mends wounds and shields allies from harm.",
        "base_hp": 95,
        "base_mp": 120,
        "starting_stats": {
            "strength": 3,
            "dexterity": 4,
            "constitution": 6,
            "intelligence": 6,
            "wisdom": 10,
            "charisma": 5
        },
        "starting_skills": ["Heal", "Blessing", "Purify"],
        "passive_name": "Divine Grace",
        "passive_description": "All healing effects are 50% more powerful and affect nearby allies.",
        "ultimate_name": "Miracle",
        "ultimate_description": "Instantly restore all HP and MP to self and all allies, remove debuffs."
    },
    "battlemage": {
        "name": "Battlemage",
        "emoji": "⚔️",
        "role": "Hybrid",
        "description": "A warrior-scholar who combines martial prowess with magical might.",
        "base_hp": 105,
        "base_mp": 105,
        "starting_stats": {
            "strength": 6,
            "dexterity": 5,
            "constitution": 6,
            "intelligence": 7,
            "wisdom": 5,
            "charisma": 5
        },
        "starting_skills": ["Flame Weapon", "Spell Strike", "Mage Armor"],
        "passive_name": "Spellsword",
        "passive_description": "Physical attacks have chance to trigger spell effects without mana cost.",
        "ultimate_name": "Elemental Fury",
        "ultimate_description": "Next 5 attacks deal random elemental damage and trigger magical explosions."
    },
    "chrono_knight": {
        "name": "Chrono Knight",
        "emoji": "⏰",
        "role": "Hidden Class",
        "description": "A time-wielding warrior who manipulates the flow of battle itself.",
        "base_hp": 110,
        "base_mp": 110,
        "starting_stats": {
            "strength": 7,
            "dexterity": 7,
            "constitution": 7,
            "intelligence": 7,
            "wisdom": 7,
            "charisma": 7
        },
        "starting_skills": ["Time Slash", "Temporal Shield", "Haste"],
        "passive_name": "Chronolock",
        "passive_description": "Can act twice per turn and has immunity to time-based effects.",
        "ultimate_name": "Time Stop",
        "ultimate_description": "Stop time for all enemies for 3 turns while you act freely."
    }
}

# Miraculous Paths (Level 20+ specializations)
PATHS = {
    "destruction": {
        "name": "Path of Destruction",
        "emoji": "💥",
        "description": "Embrace pure offensive power and devastating critical strikes.",
        "bonus_1": "+20% Critical Hit Damage",
        "bonus_2": "15% chance for follow-up attacks",
        "bonus_3": "Execute enemies below 15% HP",
        "stat_bonuses": {
            "strength": 5,
            "dexterity": 3
        }
    },
    "preservation": {
        "name": "Path of Preservation",
        "emoji": "🛡️",
        "description": "Master the arts of defense and ally protection.",
        "bonus_1": "+15% Damage Reduction",
        "bonus_2": "Generate shields equal to 20% of damage taken",
        "bonus_3": "Taunt enemies when allies are low on HP",
        "stat_bonuses": {
            "constitution": 5,
            "wisdom": 3
        }
    },
    "abundance": {
        "name": "Path of Abundance",
        "emoji": "❤️‍🩹",
        "description": "Channel life force to heal and empower your allies.",
        "bonus_1": "+25% Healing Power",
        "bonus_2": "Buffs last 50% longer",
        "bonus_3": "Healing effects have chance to spread to nearby allies",
        "stat_bonuses": {
            "wisdom": 5,
            "charisma": 3
        }
    },
    "hunt": {
        "name": "Path of The Hunt",
        "emoji": "🎯",
        "description": "Perfect your aim to deliver precise and lethal strikes.",
        "bonus_1": "Execute enemies below 25% HP",
        "bonus_2": "+15% Accuracy (cannot miss)",
        "bonus_3": "Single-target attacks deal 30% more damage",
        "stat_bonuses": {
            "dexterity": 5,
            "intelligence": 3
        }
    }
}

# Item Rarity System
RARITY_COLORS = {
    "common": "⚪",
    "uncommon": "🟢", 
    "rare": "🔵",
    "epic": "🟣",
    "legendary": "🟠",
    "mythical": "🔴",
    "divine": "⭐",
    "cosmic": "🌟"
}

RARITY_MULTIPLIERS = {
    "common": 1.0,
    "uncommon": 1.2,
    "rare": 1.5,
    "epic": 2.0,
    "legendary": 3.0,
    "mythical": 4.5,
    "divine": 7.0,
    "cosmic": 10.0
}

# Items Database
ITEMS = {
    # WEAPONS (20 total)
    "rusty_dagger": {
        "name": "Rusty Dagger",
        "type": "weapon",
        "rarity": "common",
        "attack": 8,
        "description": "A worn dagger that's seen better days.",
        "price": 50,
        "sell_price": 30
    },
    "wooden_sword": {
        "name": "Wooden Sword",
        "type": "weapon",
        "rarity": "common",
        "attack": 12,
        "description": "Basic training sword made of sturdy oak.",
        "price": 100,
        "sell_price": 60
    },
    "iron_sword": {
        "name": "Iron Sword",
        "type": "weapon",
        "rarity": "uncommon",
        "attack": 25,
        "description": "A reliable iron blade forged by skilled smiths.",
        "price": 500,
        "sell_price": 300
    },
    "steel_blade": {
        "name": "Steel Blade",
        "type": "weapon",
        "rarity": "rare",
        "attack": 45,
        "critical_chance": 5,
        "description": "Superior steel crafted with precision.",
        "price": 2000,
        "sell_price": 1200,
        "effects": ["5% chance to ignore armor"]
    },
    "flame_sword": {
        "name": "Flame Sword",
        "type": "weapon",
        "rarity": "rare",
        "attack": 50,
        "description": "A blade wreathed in eternal flames.",
        "price": 3000,
        "sell_price": 1800,
        "effects": ["Fire damage", "Burns enemies"]
    },
    "ice_blade": {
        "name": "Ice Blade",
        "type": "weapon",
        "rarity": "rare",
        "attack": 48,
        "description": "Frozen steel that never melts.",
        "price": 2800,
        "sell_price": 1680,
        "effects": ["Ice damage", "Slows enemies"]
    },
    "mithril_sword": {
        "name": "Mithril Sword",
        "type": "weapon",
        "rarity": "epic",
        "attack": 75,
        "critical_chance": 10,
        "critical_damage": 150,
        "description": "Legendary mithril blade, light as a feather, sharp as death.",
        "price": 10000,
        "sell_price": 6000,
        "effects": ["Ignores 25% of enemy defense", "10% chance for double strike"]
    },
    "dragon_fang": {
        "name": "Dragon Fang",
        "type": "weapon",
        "rarity": "epic",
        "attack": 80,
        "description": "Carved from an ancient dragon's tooth.",
        "price": 12000,
        "sell_price": 7200,
        "effects": ["Dragon slayer", "+50% damage to dragons"]
    },
    "shadow_blade": {
        "name": "Shadow Blade",
        "type": "weapon",
        "rarity": "epic",
        "attack": 70,
        "critical_chance": 15,
        "description": "A blade forged from pure darkness.",
        "price": 9000,
        "sell_price": 5400,
        "effects": ["Shadow damage", "Bypasses light armor"]
    },
    "excalibur": {
        "name": "Excalibur",
        "type": "weapon",
        "rarity": "legendary",
        "attack": 120,
        "critical_chance": 20,
        "description": "The legendary sword of kings.",
        "price": 50000,
        "sell_price": 30000,
        "effects": ["Holy damage", "Blessed by light", "Cannot break"]
    },
    "plagg_claw": {
        "name": "Plagg's Claw",
        "type": "weapon",
        "rarity": "legendary",
        "attack": 150,
        "critical_chance": 25,
        "critical_damage": 200,
        "description": "Forged from Plagg's own essence, radiates chaotic power.",
        "price": 100000,
        "sell_price": 60000,
        "effects": ["Cataclysm: 15% chance to destroy enemy equipment", "Chaos Strike: Damage varies wildly"]
    },
    "cosmic_reaper": {
        "name": "Cosmic Reaper",
        "type": "weapon",
        "rarity": "mythical",
        "attack": 200,
        "critical_chance": 30,
        "description": "A scythe that cuts through space and time.",
        "price": 250000,
        "sell_price": 150000,
        "effects": ["Void damage", "Ignores all resistances"]
    },
    "time_slicer": {
        "name": "Time Slicer",
        "type": "weapon",
        "rarity": "divine",
        "attack": 300,
        "description": "Cuts through the fabric of time itself.",
        "price": 500000,
        "sell_price": 300000,
        "effects": ["Temporal damage", "Rewinds enemy turns"]
    },
    "reality_render": {
        "name": "Reality Render",
        "type": "weapon",
        "rarity": "cosmic",
        "attack": 500,
        "critical_chance": 50,
        "critical_damage": 500,
        "description": "A blade that cuts through reality itself.",
        "price": 1000000,
        "sell_price": 600000,
        "effects": ["Dimensional slash", "25% chance to delete enemy"],
        "owner_only": True
    },
    "thunder_spear": {
        "name": "Thunder Spear",
        "type": "weapon",
        "rarity": "rare",
        "attack": 42,
        "description": "Crackling with electrical energy.",
        "price": 2500,
        "sell_price": 1500,
        "effects": ["Lightning damage", "Chain lightning"]
    },
    "bone_crusher": {
        "name": "Bone Crusher",
        "type": "weapon",
        "rarity": "uncommon",
        "attack": 35,
        "description": "A massive two-handed mace.",
        "price": 800,
        "sell_price": 480,
        "effects": ["Armor crushing", "Stuns enemies"]
    },
    "phantom_dagger": {
        "name": "Phantom Dagger",
        "type": "weapon",
        "rarity": "rare",
        "attack": 40,
        "critical_chance": 12,
        "description": "Appears and disappears at will.",
        "price": 2200,
        "sell_price": 1320,
        "effects": ["Phase through armor", "Invisible strikes"]
    },
    "holy_mace": {
        "name": "Holy Mace",
        "type": "weapon",
        "rarity": "epic",
        "attack": 65,
        "description": "Blessed by divine light.",
        "price": 8500,
        "sell_price": 5100,
        "effects": ["Holy damage", "Heals wielder"]
    },
    "void_axe": {
        "name": "Void Axe",
        "type": "weapon",
        "rarity": "epic",
        "attack": 85,
        "description": "Cleaves through dimensions.",
        "price": 11000,
        "sell_price": 6600,
        "effects": ["Void damage", "Dimension cut"]
    },
    "chaos_blade": {
        "name": "Chaos Blade",
        "type": "weapon",
        "rarity": "legendary",
        "attack": 130,
        "description": "Embodies pure chaos and destruction.",
        "price": 75000,
        "sell_price": 45000,
        "effects": ["Random damage type", "Unpredictable effects"],
        "sources": ["shop", "boss", "elite"]
    },
    
    # Additional weapons (5 more to reach 25)
    "soul_reaver": {
        "name": "Soul Reaver",
        "type": "weapon", 
        "rarity": "epic",
        "attack": 90,
        "description": "Harvests the souls of the fallen.",
        "price": 13000,
        "sell_price": 7800,
        "effects": ["Soul steal", "Life drain"],
        "sources": ["dungeon", "boss"]
    },
    "tempest_blade": {
        "name": "Tempest Blade",
        "type": "weapon",
        "rarity": "rare",
        "attack": 55,
        "description": "Crackling with storm energy.",
        "price": 3500,
        "sell_price": 2100,
        "effects": ["Storm damage", "Wind slash"],
        "sources": ["shop", "battle"]
    },
    "crystal_sword": {
        "name": "Crystal Sword",
        "type": "weapon",
        "rarity": "uncommon",
        "attack": 30,
        "description": "Made from pure crystal formations.",
        "price": 900,
        "sell_price": 540,
        "effects": ["Crystal resonance"],
        "sources": ["shop", "explore"]
    },
    "blood_drinker": {
        "name": "Blood Drinker",
        "type": "weapon",
        "rarity": "epic",
        "attack": 88,
        "description": "Thirsts for the blood of enemies.",
        "price": 14000,
        "sell_price": 8400,
        "effects": ["Vampiric", "Blood frenzy"],
        "sources": ["dungeon", "elite"]
    },
    "nightmare_edge": {
        "name": "Nightmare Edge",
        "type": "weapon",
        "rarity": "legendary",
        "attack": 125,
        "description": "Forged from crystallized nightmares.",
        "price": 65000,
        "sell_price": 39000,
        "effects": ["Fear inducing", "Nightmare realm"],
        "sources": ["boss", "legendary_monster"]
    },

    # ARMOR (20 total)
    "cloth_robe": {
        "name": "Cloth Robe",
        "type": "armor",
        "rarity": "common",
        "defense": 5,
        "mana": 20,
        "description": "Simple cloth garment for mages.",
        "price": 100,
        "sell_price": 60
    },
    "leather_vest": {
        "name": "Leather Vest",
        "type": "armor",
        "rarity": "common",
        "defense": 10,
        "hp": 25,
        "description": "Basic leather protection.",
        "price": 300,
        "sell_price": 180
    },
    "studded_leather": {
        "name": "Studded Leather",
        "type": "armor",
        "rarity": "uncommon",
        "defense": 18,
        "hp": 40,
        "description": "Leather reinforced with metal studs.",
        "price": 600,
        "sell_price": 360
    },
    "chain_mail": {
        "name": "Chain Mail",
        "type": "armor",
        "rarity": "uncommon",
        "defense": 25,
        "hp": 60,
        "description": "Interlocked metal rings.",
        "price": 1000,
        "sell_price": 600
    },
    "scale_armor": {
        "name": "Scale Armor",
        "type": "armor",
        "rarity": "rare",
        "defense": 35,
        "hp": 80,
        "description": "Overlapping metal scales.",
        "price": 2000,
        "sell_price": 1200
    },
    "plate_armor": {
        "name": "Plate Armor",
        "type": "armor",
        "rarity": "rare",
        "defense": 50,
        "hp": 120,
        "description": "Heavy metal plates.",
        "price": 4000,
        "sell_price": 2400,
        "effects": ["Damage reduction: -5 from all attacks"]
    },
    "mithril_mail": {
        "name": "Mithril Mail",
        "type": "armor",
        "rarity": "epic",
        "defense": 70,
        "hp": 150,
        "mana": 50,
        "description": "Lightweight yet incredibly strong.",
        "price": 8000,
        "sell_price": 4800,
        "effects": ["Magic resistance: 25%"]
    },
    "dragon_scale_mail": {
        "name": "Dragon Scale Mail",
        "type": "armor",
        "rarity": "epic",
        "defense": 85,
        "hp": 200,
        "description": "Crafted from genuine dragon scales.",
        "price": 15000,
        "sell_price": 9000,
        "effects": ["Fire immunity", "25% magic resistance"]
    },
    "celestial_robes": {
        "name": "Celestial Robes",
        "type": "armor",
        "rarity": "legendary",
        "defense": 60,
        "hp": 150,
        "mana": 200,
        "description": "Woven from starlight itself.",
        "price": 40000,
        "sell_price": 24000,
        "effects": ["Spell power +30%", "Mana regeneration"]
    },
    "tikki_blessing": {
        "name": "Tikki's Blessing",
        "type": "armor",
        "rarity": "legendary",
        "defense": 100,
        "hp": 300,
        "mana": 150,
        "description": "Blessed by the Kwami of Creation.",
        "price": 75000,
        "sell_price": 45000,
        "effects": ["Lucky Charm: 20% chance to negate attacks", "Creative regeneration"]
    },
    "void_armor": {
        "name": "Void Armor",
        "type": "armor",
        "rarity": "mythical",
        "defense": 150,
        "hp": 400,
        "description": "Forged in the depths of space.",
        "price": 200000,
        "sell_price": 120000,
        "effects": ["Void resistance", "Phase through attacks"]
    },
    "time_guardian_plate": {
        "name": "Time Guardian Plate",
        "type": "armor",
        "rarity": "divine",
        "defense": 200,
        "hp": 500,
        "description": "Protects across all timelines.",
        "price": 400000,
        "sell_price": 240000,
        "effects": ["Temporal immunity", "Time dilation field"]
    },
    "reality_aegis": {
        "name": "Reality Aegis",
        "type": "armor",
        "rarity": "cosmic",
        "defense": 9999,
        "hp": 999999,
        "mana": 999999,
        "description": "Armor that transcends reality.",
        "price": 1000000,
        "sell_price": 600000,
        "effects": ["Invulnerability", "Reality anchor"],
        "owner_only": True
    },
    "shadow_cloak": {
        "name": "Shadow Cloak",
        "type": "armor",
        "rarity": "rare",
        "defense": 30,
        "hp": 70,
        "description": "Grants stealth abilities.",
        "price": 3000,
        "sell_price": 1800,
        "effects": ["Stealth", "+15% dodge chance"]
    },
    "flame_guard": {
        "name": "Flame Guard",
        "type": "armor",
        "rarity": "rare",
        "defense": 45,
        "hp": 100,
        "description": "Provides fire protection.",
        "price": 3500,
        "sell_price": 2100,
        "effects": ["Fire immunity", "Burning aura"]
    },
    "ice_fortress": {
        "name": "Ice Fortress",
        "type": "armor",
        "rarity": "epic",
        "defense": 65,
        "hp": 180,
        "description": "Frozen armor that never melts.",
        "price": 10000,
        "sell_price": 6000,
        "effects": ["Ice immunity", "Freezing aura"]
    },
    "storm_mail": {
        "name": "Storm Mail",
        "type": "armor",
        "rarity": "epic",
        "defense": 75,
        "hp": 160,
        "description": "Crackling with electricity.",
        "price": 12000,
        "sell_price": 7200,
        "effects": ["Lightning immunity", "Shock field"]
    },
    "bone_armor": {
        "name": "Bone Armor",
        "type": "armor",
        "rarity": "uncommon",
        "defense": 22,
        "hp": 50,
        "description": "Made from monster bones.",
        "price": 800,
        "sell_price": 480,
        "effects": ["Intimidation", "Undead resistance"]
    },
    "crystal_shell": {
        "name": "Crystal Shell",
        "type": "armor",
        "rarity": "rare",
        "defense": 40,
        "hp": 90,
        "mana": 40,
        "description": "Crystalline protective layer.",
        "price": 2800,
        "sell_price": 1680,
        "effects": ["Magic reflection", "Crystal resonance"]
    },
    "demon_hide": {
        "name": "Demon Hide",
        "type": "armor",
        "rarity": "epic",
        "defense": 80,
        "hp": 170,
        "description": "Tough hide from demonic beasts.",
        "price": 14000,
        "sell_price": 8400,
        "effects": ["Dark resistance", "Fear immunity"],
        "sources": ["boss", "dungeon"]
    },
    
    # Additional armor (5 more to reach 25)
    "spirit_mail": {
        "name": "Spirit Mail",
        "type": "armor",
        "rarity": "rare",
        "defense": 42,
        "hp": 95,
        "mana": 45,
        "description": "Woven with spiritual energy.",
        "price": 3200,
        "sell_price": 1920,
        "effects": ["Spirit protection", "Mana regeneration"],
        "sources": ["shop", "explore"]
    },
    "phoenix_mail": {
        "name": "Phoenix Mail",
        "type": "armor",
        "rarity": "legendary",
        "defense": 90,
        "hp": 220,
        "description": "Armor that rises from ashes.",
        "price": 45000,
        "sell_price": 27000,
        "effects": ["Revival", "Fire immunity", "Phoenix regeneration"],
        "sources": ["boss", "legendary_monster"]
    },
    "assassin_leather": {
        "name": "Assassin's Leather",
        "type": "armor",
        "rarity": "rare",
        "defense": 35,
        "hp": 75,
        "description": "Silent and deadly protection.",
        "price": 2900,
        "sell_price": 1740,
        "effects": ["Stealth", "Critical boost"],
        "sources": ["shop", "battle"]
    },
    "holy_vestments": {
        "name": "Holy Vestments",
        "type": "armor",
        "rarity": "epic",
        "defense": 55,
        "hp": 130,
        "mana": 100,
        "description": "Blessed by divine light.",
        "price": 9500,
        "sell_price": 5700,
        "effects": ["Holy protection", "Divine blessing"],
        "sources": ["dungeon", "elite"]
    },
    "necromancer_robes": {
        "name": "Necromancer's Robes",
        "type": "armor",
        "rarity": "epic",
        "defense": 45,
        "hp": 110,
        "mana": 120,
        "description": "Dark robes of death magic.",
        "price": 11000,
        "sell_price": 6600,
        "effects": ["Undead control", "Death resistance"],
        "sources": ["boss", "dungeon"]
    },

    # CONSUMABLES (7 total)
    "health_potion": {
        "name": "Health Potion",
        "type": "consumable",
        "rarity": "common",
        "heal_amount": 100,
        "description": "Restores 100 HP instantly.",
        "price": 50,
        "sell_price": 30,
        "effects": ["heal"]
    },
    "mana_potion": {
        "name": "Mana Potion",
        "type": "consumable",
        "rarity": "common",
        "mana_amount": 50,
        "description": "Restores 50 Mana instantly.",
        "price": 75,
        "sell_price": 45,
        "effects": ["mana"]
    },
    "greater_health_potion": {
        "name": "Greater Health Potion",
        "type": "consumable",
        "rarity": "rare",
        "heal_amount": 500,
        "description": "Restores 500 HP and removes debuffs.",
        "price": 500,
        "sell_price": 300,
        "effects": ["heal", "remove_debuffs"]
    },
    "elixir_of_power": {
        "name": "Elixir of Power",
        "type": "consumable",
        "rarity": "epic",
        "description": "Temporarily doubles all stats for 5 battles.",
        "price": 2000,
        "sell_price": 1200,
        "effects": ["temporary_boost"]
    },
    "phoenix_feather": {
        "name": "Phoenix Feather",
        "type": "consumable",
        "rarity": "legendary",
        "description": "Revives with full HP and removes all debuffs.",
        "price": 10000,
        "sell_price": 6000,
        "effects": ["revival", "full_heal", "remove_debuffs"]
    },
    "plagg_cheese": {
        "name": "Plagg's Special Camembert",
        "type": "consumable",
        "rarity": "legendary",
        "heal_amount": 100,
        "description": "Plagg's favorite cheese, grants his blessing.",
        "price": 25000,
        "sell_price": 15000,
        "effects": ["cheese_blessing", "chaos_power"]
    },
    "ambrosia": {
        "name": "Ambrosia",
        "type": "consumable",
        "rarity": "divine",
        "description": "Food of the gods, grants temporary divinity.",
        "price": 100000,
        "sell_price": 60000,
        "effects": ["divine_blessing", "immortality"],
        "sources": ["legendary_monster", "cosmic_void"]
    },
    
    # Additional consumables (18 more to reach 25)
    "super_health_potion": {
        "name": "Super Health Potion",
        "type": "consumable",
        "rarity": "uncommon",
        "heal_amount": 250,
        "description": "Restores 250 HP instantly.",
        "price": 150,
        "sell_price": 90,
        "effects": ["heal"],
        "sources": ["shop", "battle"]
    },
    "mega_mana_potion": {
        "name": "Mega Mana Potion",
        "type": "consumable",
        "rarity": "uncommon",
        "mana_amount": 150,
        "description": "Restores 150 Mana instantly.",
        "price": 200,
        "sell_price": 120,
        "effects": ["mana"],
        "sources": ["shop", "battle"]
    },
    "rejuvenation_potion": {
        "name": "Rejuvenation Potion",
        "type": "consumable",
        "rarity": "rare",
        "heal_amount": 300,
        "mana_amount": 100,
        "description": "Restores both HP and Mana.",
        "price": 400,
        "sell_price": 240,
        "effects": ["heal", "mana"],
        "sources": ["shop", "dungeon"]
    },
    "strength_elixir": {
        "name": "Strength Elixir",
        "type": "consumable",
        "rarity": "uncommon",
        "description": "Temporarily increases attack power by 50%.",
        "price": 250,
        "sell_price": 150,
        "effects": ["strength_boost"],
        "sources": ["shop", "crafting"]
    },
    "speed_potion": {
        "name": "Speed Potion",
        "type": "consumable",
        "rarity": "uncommon",
        "description": "Increases movement and attack speed.",
        "price": 180,
        "sell_price": 108,
        "effects": ["speed_boost"],
        "sources": ["shop", "crafting"]
    },
    "defense_tonic": {
        "name": "Defense Tonic",
        "type": "consumable",
        "rarity": "uncommon",
        "description": "Temporarily increases defense by 40%.",
        "price": 220,
        "sell_price": 132,
        "effects": ["defense_boost"],
        "sources": ["shop", "crafting"]
    },
    "antidote": {
        "name": "Antidote",
        "type": "consumable",
        "rarity": "common",
        "description": "Cures poison and toxic effects.",
        "price": 80,
        "sell_price": 48,
        "effects": ["cure_poison"],
        "sources": ["shop", "battle"]
    },
    "holy_water": {
        "name": "Holy Water",
        "type": "consumable",
        "rarity": "rare",
        "description": "Removes curses and dark magic.",
        "price": 300,
        "sell_price": 180,
        "effects": ["remove_curse", "holy_blessing"],
        "sources": ["shop", "dungeon"]
    },
    "berserker_brew": {
        "name": "Berserker's Brew",
        "type": "consumable",
        "rarity": "rare",
        "description": "Enter a rage state with doubled attack.",
        "price": 450,
        "sell_price": 270,
        "effects": ["berserker_rage"],
        "sources": ["crafting", "elite"]
    },
    "invisibility_potion": {
        "name": "Invisibility Potion",
        "type": "consumable",
        "rarity": "epic",
        "description": "Become invisible for 3 turns.",
        "price": 800,
        "sell_price": 480,
        "effects": ["invisibility"],
        "sources": ["crafting", "boss"]
    },
    "resurrection_scroll": {
        "name": "Resurrection Scroll",
        "type": "consumable",
        "rarity": "legendary",
        "description": "Revive with 50% HP if defeated.",
        "price": 5000,
        "sell_price": 3000,
        "effects": ["auto_revive"],
        "sources": ["boss", "legendary_monster"]
    },
    "divine_nectar": {
        "name": "Divine Nectar",
        "type": "consumable",
        "rarity": "mythical",
        "heal_amount": 1000,
        "mana_amount": 500,
        "description": "The ultimate healing elixir.",
        "price": 25000,
        "sell_price": 15000,
        "effects": ["full_heal", "divine_blessing"],
        "sources": ["cosmic_void", "legendary_monster"]
    },
    "time_potion": {
        "name": "Time Acceleration Potion",
        "type": "consumable",
        "rarity": "epic",
        "description": "Act twice in one turn.",
        "price": 1200,
        "sell_price": 720,
        "effects": ["double_action"],
        "sources": ["crafting", "boss"]
    },
    "experience_elixir": {
        "name": "Experience Elixir",
        "type": "consumable",
        "rarity": "rare",
        "description": "Doubles XP gain for next 3 battles.",
        "price": 600,
        "sell_price": 360,
        "effects": ["xp_boost"],
        "sources": ["shop", "dungeon"]
    },
    "luck_potion": {
        "name": "Luck Potion",
        "type": "consumable",
        "rarity": "uncommon",
        "description": "Increases critical hit chance by 25%.",
        "price": 300,
        "sell_price": 180,
        "effects": ["luck_boost"],
        "sources": ["shop", "crafting"]
    },
    "fire_resistance_potion": {
        "name": "Fire Resistance Potion",
        "type": "consumable",
        "rarity": "uncommon",
        "description": "Immune to fire damage for 5 turns.",
        "price": 180,
        "sell_price": 108,
        "effects": ["fire_immunity"],
        "sources": ["shop", "crafting"]
    },
    "ice_resistance_potion": {
        "name": "Ice Resistance Potion",
        "type": "consumable",
        "rarity": "uncommon",
        "description": "Immune to ice damage for 5 turns.",
        "price": 180,
        "sell_price": 108,
        "effects": ["ice_immunity"],
        "sources": ["shop", "crafting"]
    },
    "mana_burn_potion": {
        "name": "Mana Burn Potion",
        "type": "consumable",
        "rarity": "rare",
        "description": "Destroys enemy mana on hit.",
        "price": 400,
        "sell_price": 240,
        "effects": ["mana_burn"],
        "sources": ["crafting", "dungeon"]
    },
    "titan_strength": {
        "name": "Titan's Strength",
        "type": "consumable",
        "rarity": "legendary",
        "description": "Become a titan for 3 turns.",
        "price": 8000,
        "sell_price": 4800,
        "effects": ["titan_form"],
        "sources": ["boss", "legendary_monster"]
    },
    "void_essence": {
        "name": "Void Essence",
        "type": "consumable",
        "rarity": "mythical",
        "description": "Absorb all damage for 1 turn.",
        "price": 15000,
        "sell_price": 9000,
        "effects": ["void_absorption"],
        "sources": ["cosmic_void", "boss"]
    },
    "camembert_supreme": {
        "name": "Supreme Camembert",
        "type": "consumable",
        "rarity": "mythical",
        "heal_amount": 500,
        "description": "Plagg's ultimate cheese creation.",
        "price": 50000,
        "sell_price": 30000,
        "effects": ["plagg_blessing", "chaos_power", "cheese_mastery"],
        "sources": ["hidden", "achievement"]
    },
    "liquid_courage": {
        "name": "Liquid Courage",
        "type": "consumable",
        "rarity": "rare",
        "description": "Immune to fear and charm effects.",
        "price": 350,
        "sell_price": 210,
        "effects": ["fear_immunity"],
        "sources": ["shop", "crafting"]
    },

    # ACCESSORIES (20 total)
    "copper_ring": {
        "name": "Copper Ring",
        "type": "accessory",
        "rarity": "common",
        "attack": 3,
        "description": "Simple copper band.",
        "price": 100,
        "sell_price": 60
    },
    "silver_ring": {
        "name": "Silver Ring",
        "type": "accessory",
        "rarity": "common",
        "attack": 5,
        "description": "A simple silver band.",
        "price": 200,
        "sell_price": 120
    },
    "gold_chain": {
        "name": "Gold Chain",
        "type": "accessory",
        "rarity": "uncommon",
        "hp": 30,
        "mana": 20,
        "description": "Elegant gold necklace.",
        "price": 500,
        "sell_price": 300
    },
    "luck_charm": {
        "name": "Lucky Charm",
        "type": "accessory",
        "rarity": "uncommon",
        "critical_chance": 10,
        "description": "Brings good fortune.",
        "price": 800,
        "sell_price": 480,
        "effects": ["+10% crit chance"]
    },
    "power_ring": {
        "name": "Ring of Power",
        "type": "accessory",
        "rarity": "rare",
        "attack": 15,
        "mana": 50,
        "description": "Amplifies magical abilities.",
        "price": 2000,
        "sell_price": 1200,
        "effects": ["Magic boost"]
    },
    "shield_amulet": {
        "name": "Shield Amulet",
        "type": "accessory",
        "rarity": "rare",
        "defense": 20,
        "hp": 80,
        "description": "Provides magical protection.",
        "price": 2500,
        "sell_price": 1500,
        "effects": ["Damage reduction 10%"]
    },
    "speed_boots": {
        "name": "Boots of Speed",
        "type": "accessory",
        "rarity": "rare",
        "description": "Increases movement and attack speed.",
        "price": 3000,
        "sell_price": 1800,
        "effects": ["+50% speed", "Extra turn chance"]
    },
    "mage_focus": {
        "name": "Mage's Focus",
        "type": "accessory",
        "rarity": "epic",
        "mana": 100,
        "description": "Enhances spell casting abilities.",
        "price": 5000,
        "sell_price": 3000,
        "effects": ["Spell cost -25%", "Spell power +20%"]
    },
    "berserker_belt": {
        "name": "Berserker's Belt",
        "type": "accessory",
        "rarity": "epic",
        "attack": 30,
        "critical_damage": 50,
        "description": "Fuels battle rage.",
        "price": 6000,
        "sell_price": 3600,
        "effects": ["Rage mode", "Critical fury"]
    },
    "phoenix_pendant": {
        "name": "Phoenix Pendant",
        "type": "accessory",
        "rarity": "legendary",
        "hp": 200,
        "description": "Grants phoenix-like regeneration.",
        "price": 20000,
        "sell_price": 12000,
        "effects": ["Auto-revival once per battle", "Fire immunity"]
    },
    "void_crystal": {
        "name": "Void Crystal",
        "type": "accessory",
        "rarity": "mythical",
        "attack": 50,
        "mana": 150,
        "description": "Contains the power of the void.",
        "price": 80000,
        "sell_price": 48000,
        "effects": ["Void magic", "Reality manipulation"]
    },
    "time_jewel": {
        "name": "Jewel of Time",
        "type": "accessory",
        "rarity": "divine",
        "description": "Controls the flow of time.",
        "price": 200000,
        "sell_price": 120000,
        "effects": ["Time control", "Temporal immunity"]
    },
    "reality_fragment": {
        "name": "Reality Fragment",
        "type": "accessory",
        "rarity": "cosmic",
        "attack": 100,
        "defense": 100,
        "hp": 500,
        "mana": 500,
        "description": "A piece of reality itself.",
        "price": 500000,
        "sell_price": 300000,
        "effects": ["Reality control", "Universal power"],
        "owner_only": True
    },
    "shadow_mask": {
        "name": "Shadow Mask",
        "type": "accessory",
        "rarity": "rare",
        "critical_chance": 15,
        "description": "Conceals identity and intent.",
        "price": 2200,
        "sell_price": 1320,
        "effects": ["Stealth", "Sneak attack"]
    },
    "flame_crown": {
        "name": "Crown of Flames",
        "type": "accessory",
        "rarity": "epic",
        "attack": 25,
        "mana": 80,
        "description": "Burns with eternal fire.",
        "price": 7000,
        "sell_price": 4200,
        "effects": ["Fire mastery", "Burning aura"]
    },
    "ice_tiara": {
        "name": "Ice Tiara",
        "type": "accessory",
        "rarity": "epic",
        "defense": 30,
        "mana": 90,
        "description": "Frozen crown that never melts.",
        "price": 7500,
        "sell_price": 4500,
        "effects": ["Ice mastery", "Freezing aura"]
    },
    "storm_bracelet": {
        "name": "Storm Bracelet",
        "type": "accessory",
        "rarity": "rare",
        "attack": 18,
        "description": "Crackling with electricity.",
        "price": 2800,
        "sell_price": 1680,
        "effects": ["Lightning damage", "Chain lightning"]
    },
    "earth_gauntlets": {
        "name": "Earth Gauntlets",
        "type": "accessory",
        "rarity": "rare",
        "defense": 25,
        "hp": 60,
        "description": "Grants power over earth.",
        "price": 3200,
        "sell_price": 1920,
        "effects": ["Earth mastery", "Stone skin"]
    },
    "wind_cloak": {
        "name": "Cloak of Winds",
        "type": "accessory",
        "rarity": "epic",
        "description": "Grants mastery over air currents.",
        "price": 6500,
        "sell_price": 3900,
        "effects": ["Flight", "Wind mastery", "+30% dodge"]
    },
    "dragon_heart": {
        "name": "Dragon Heart",
        "type": "accessory",
        "rarity": "legendary",
        "attack": 40,
        "hp": 300,
        "description": "Still beats with dragon power.",
        "price": 50000,
        "sell_price": 30000,
        "effects": ["Dragon power", "Fire immunity", "Intimidation"]
    },

    # MATERIALS (25 total)
    "iron_ore": {
        "name": "Iron Ore",
        "type": "material",
        "rarity": "common",
        "description": "Basic crafting material.",
        "price": 10,
        "sell_price": 6,
        "sources": ["battle", "explore", "shop"]
    },
    "steel_ingot": {
        "name": "Steel Ingot",
        "type": "material", 
        "rarity": "uncommon",
        "description": "Refined metal for crafting.",
        "price": 25,
        "sell_price": 15,
        "sources": ["crafting", "shop", "battle"]
    },
    "mithril_ore": {
        "name": "Mithril Ore",
        "type": "material",
        "rarity": "rare",
        "description": "Precious crafting metal.",
        "price": 100,
        "sell_price": 60,
        "sources": ["dungeon", "elite", "explore"]
    },
    "dragon_scale": {
        "name": "Dragon Scale",
        "type": "material",
        "rarity": "epic",
        "description": "Scales from ancient dragons.",
        "price": 500,
        "sell_price": 300,
        "sources": ["boss", "dragon_lair", "legendary_monster"]
    },
    "void_crystal": {
        "name": "Void Crystal",
        "type": "material",
        "rarity": "legendary",
        "description": "Crystal from the void realm.",
        "price": 2000,
        "sell_price": 1200,
        "sources": ["cosmic_void", "boss"]
    },
    "time_shard": {
        "name": "Time Shard",
        "type": "material",
        "rarity": "mythical",
        "description": "Fragment of crystallized time.",
        "price": 5000,
        "sell_price": 3000,
        "sources": ["cosmic_void", "legendary_monster"]
    },
    "shadow_essence": {
        "name": "Shadow Essence",
        "type": "material",
        "rarity": "rare",
        "description": "Pure essence of darkness.",
        "price": 150,
        "sell_price": 90,
        "sources": ["shadow_fortress", "battle"]
    },
    "light_crystal": {
        "name": "Light Crystal",
        "type": "material",
        "rarity": "epic",
        "description": "Crystallized pure light.",
        "price": 400,
        "sell_price": 240,
        "sources": ["dungeon", "elite"]
    },
    "phoenix_feather": {
        "name": "Phoenix Feather",
        "type": "material",
        "rarity": "legendary",
        "description": "Feather from a phoenix.",
        "price": 1500,
        "sell_price": 900,
        "sources": ["boss", "legendary_monster"]
    },
    "demon_horn": {
        "name": "Demon Horn",
        "type": "material",
        "rarity": "epic",
        "description": "Horn from demonic creatures.",
        "price": 350,
        "sell_price": 210,
        "sources": ["boss", "dungeon"]
    },
    "angel_wing": {
        "name": "Angel Wing",
        "type": "material",
        "rarity": "legendary",
        "description": "Wing from celestial beings.",
        "price": 1800,
        "sell_price": 1080,
        "sources": ["boss", "cosmic_void"]
    },
    "unicorn_hair": {
        "name": "Unicorn Hair",
        "type": "material",
        "rarity": "rare",
        "description": "Hair from a unicorn's mane.",
        "price": 200,
        "sell_price": 120,
        "sources": ["explore", "elite"]
    },
    "spider_silk": {
        "name": "Spider Silk",
        "type": "material",
        "rarity": "common",
        "description": "Strong silk from giant spiders.",
        "price": 15,
        "sell_price": 9,
        "sources": ["battle", "goblin_caves"]
    },
    "magic_dust": {
        "name": "Magic Dust",
        "type": "material",
        "rarity": "uncommon",
        "description": "Sparkling magical dust.",
        "price": 30,
        "sell_price": 18,
        "sources": ["battle", "crafting"]
    },
    "blood_ruby": {
        "name": "Blood Ruby",
        "type": "material",
        "rarity": "epic",
        "description": "Ruby stained with ancient blood.",
        "price": 600,
        "sell_price": 360,
        "sources": ["boss", "dungeon"]
    },
    "soul_gem": {
        "name": "Soul Gem",
        "type": "material",
        "rarity": "legendary",
        "description": "Gem containing trapped souls.",
        "price": 2500,
        "sell_price": 1500,
        "sources": ["boss", "legendary_monster"]
    },
    "chaos_shard": {
        "name": "Chaos Shard",
        "type": "material",
        "rarity": "mythical",
        "description": "Fragment of pure chaos.",
        "price": 8000,
        "sell_price": 4800,
        "sources": ["cosmic_void", "hidden"]
    },
    "moonstone": {
        "name": "Moonstone",
        "type": "material",
        "rarity": "rare",
        "description": "Stone blessed by moonlight.",
        "price": 120,
        "sell_price": 72,
        "sources": ["explore", "shop"]
    },
    "sunstone": {
        "name": "Sunstone",
        "type": "material",
        "rarity": "rare",
        "description": "Stone blessed by sunlight.",
        "price": 120,
        "sell_price": 72,
        "sources": ["explore", "shop"]
    },
    "ancient_bone": {
        "name": "Ancient Bone",
        "type": "material",
        "rarity": "uncommon",
        "description": "Bone from prehistoric creatures.",
        "price": 40,
        "sell_price": 24,
        "sources": ["dungeon", "battle"]
    },
    "crystal_core": {
        "name": "Crystal Core",
        "type": "material",
        "rarity": "epic",
        "description": "Core of a crystal golem.",
        "price": 450,
        "sell_price": 270,
        "sources": ["elite", "dungeon"]
    },
    "elemental_essence": {
        "name": "Elemental Essence",
        "type": "material",
        "rarity": "rare",
        "description": "Essence from elemental beings.",
        "price": 180,
        "sell_price": 108,
        "sources": ["battle", "dungeon"]
    },
    "star_fragment": {
        "name": "Star Fragment",
        "type": "material",
        "rarity": "legendary",
        "description": "Fragment fallen from the stars.",
        "price": 3000,
        "sell_price": 1800,
        "sources": ["cosmic_void", "legendary_monster"]
    },
    "reality_dust": {
        "name": "Reality Dust",
        "type": "material",
        "rarity": "cosmic",
        "description": "Dust from the fabric of reality.",
        "price": 0,  # Cannot be bought
        "sell_price": 10000,
        "sources": ["cosmic_void", "owner_only"]
    },
    "cheese_rind": {
        "name": "Aged Cheese Rind",
        "type": "material",
        "rarity": "legendary",
        "description": "Rind from Plagg's favorite cheese.",
        "price": 0,  # Cannot be bought
        "sell_price": 5000,
        "sources": ["hidden", "achievement"]
    },

    # SUPER OP ITEMS (10 total - Achievement locked)
    "genesis_sword": {
        "name": "Genesis - The First Blade",
        "type": "weapon",
        "rarity": "cosmic",
        "attack": 1000,
        "critical_chance": 100,
        "critical_damage": 1000,
        "description": "The very first weapon ever created, forged at the dawn of time.",
        "price": 0,  # Cannot be bought
        "sell_price": 0,  # Cannot be sold
        "effects": ["Genesis Strike: Always critical hit", "Creation Force: Ignores all defenses"],
        "sources": ["achievement"],
        "achievement_req": "first_blade_master",
        "level_req": 50,
        "hidden": True,
        "owner_only": False
    },
    "eternity_armor": {
        "name": "Eternity - Armor of Ages",
        "type": "armor",
        "rarity": "cosmic",
        "defense": 500,
        "hp": 10000,
        "mana": 5000,
        "description": "Armor that has existed since the beginning of time.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Timeless: Immune to aging effects", "Eternal Protection: Reduces all damage by 90%"],
        "sources": ["achievement"],
        "achievement_req": "eternal_guardian",
        "level_req": 45,
        "hidden": True
    },
    "omnipotence_ring": {
        "name": "Omnipotence - Ring of All Power",
        "type": "accessory",
        "rarity": "cosmic",
        "attack": 300,
        "defense": 300,
        "hp": 3000,
        "mana": 3000,
        "critical_chance": 50,
        "description": "A ring containing unlimited power over all things.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Omnipotence: All abilities cost no resources", "Reality Control: Can alter battle conditions"],
        "sources": ["achievement"],
        "achievement_req": "power_absolute",
        "level_req": 40,
        "hidden": True
    },
    "void_crown": {
        "name": "The Void Crown",
        "type": "accessory",
        "rarity": "cosmic",
        "attack": 200,
        "defense": 200,
        "hp": 2000,
        "mana": 2000,
        "description": "Crown of the ruler of the void realm.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Void Mastery: Control over void magic", "Null Field: Cancel enemy abilities"],
        "sources": ["achievement"],
        "achievement_req": "void_conqueror",
        "level_req": 35,
        "hidden": True
    },
    "time_master_staff": {
        "name": "Chronos - Master of Time",
        "type": "weapon",
        "rarity": "cosmic",
        "attack": 800,
        "mana": 1000,
        "description": "Staff that controls the flow of time itself.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Time Control: Can stop, rewind, or fast-forward time", "Temporal Mastery: Act multiple times per turn"],
        "sources": ["achievement"],
        "achievement_req": "time_sovereign",
        "level_req": 50,
        "hidden": True
    },
    "soul_harvester": {
        "name": "Soul Harvester - Death's Scythe",
        "type": "weapon",
        "rarity": "cosmic",
        "attack": 900,
        "critical_chance": 75,
        "description": "The scythe of Death itself, harvester of souls.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Soul Harvest: Gain power from defeated enemies", "Death Touch: 25% chance to instantly kill"],
        "sources": ["achievement"],
        "achievement_req": "death_incarnate",
        "level_req": 48,
        "hidden": True
    },
    "creation_gauntlets": {
        "name": "Genesis Gauntlets",
        "type": "accessory",
        "rarity": "cosmic",
        "attack": 250,
        "hp": 2500,
        "description": "Gauntlets with the power of creation.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Creation: Can create any item once per day", "Matter Manipulation: Change enemy equipment"],
        "sources": ["achievement"],
        "achievement_req": "master_creator",
        "level_req": 42,
        "hidden": True
    },
    "plagg_true_ring": {
        "name": "Plagg's True Ring of Destruction",
        "type": "accessory",
        "rarity": "cosmic",
        "attack": 999,
        "critical_chance": 99,
        "critical_damage": 999,
        "description": "Plagg's personal ring, containing his true power.",
        "price": 0,
        "sell_price": 0,
        "effects": ["True Cataclysm: Destroy anything", "Cheese Mastery: All cheese effects are maximized"],
        "sources": ["achievement"],
        "achievement_req": "plagg_chosen_one",
        "level_req": 50,
        "hidden": True
    },
    "infinity_blade": {
        "name": "∞ Infinity Blade",
        "type": "weapon",
        "rarity": "cosmic",
        "attack": 2000,
        "critical_chance": 100,
        "description": "A blade with infinite sharpness and power.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Infinite Cut: Ignores all defenses and resistances", "∞ Power: Damage scales infinitely"],
        "sources": ["achievement"],
        "achievement_req": "infinite_warrior",
        "level_req": 50,
        "hidden": True
    },
    "reality_gem": {
        "name": "The Reality Gem",
        "type": "consumable",
        "rarity": "cosmic",
        "description": "A gem that can rewrite reality itself. Single use.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Reality Rewrite: Change any aspect of your character", "Wish: Grant any reasonable wish"],
        "sources": ["achievement"],
        "achievement_req": "reality_master",
        "level_req": 50,
        "hidden": True
    },

    # ARTIFACTS (20 total - Kwami Artifacts)
    "tikki_earrings": {
        "name": "Tikki's Earrings",
        "type": "artifact",
        "rarity": "legendary",
        "hp": 200,
        "mana": 150,
        "description": "The miraculous of the ladybug.",
        "price": 0,  # Cannot be bought
        "sell_price": 0,  # Cannot be sold
        "effects": ["Lucky Charm", "Miraculous Ladybug", "Creation power"],
        "set": "creation_set",
        "auction_only": True
    },
    "plagg_ring": {
        "name": "Plagg's Ring",
        "type": "artifact",
        "rarity": "legendary",
        "attack": 100,
        "critical_damage": 50,
        "description": "The miraculous of the black cat.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Cataclysm", "Nine Lives", "Destruction power"],
        "set": "destruction_set",
        "auction_only": True
    },
    "trixx_necklace": {
        "name": "Trixx's Necklace",
        "type": "artifact",
        "rarity": "legendary",
        "description": "The miraculous of the fox.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Mirage", "Illusion mastery", "Deception"],
        "set": "illusion_set",
        "auction_only": True
    },
    "pollen_comb": {
        "name": "Pollen's Comb",
        "type": "artifact",
        "rarity": "legendary",
        "description": "The miraculous of the bee.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Venom", "Paralysis", "Command"],
        "set": "paralysis_set",
        "auction_only": True
    },
    "wayzz_bracelet": {
        "name": "Wayzz's Bracelet",
        "type": "artifact",
        "rarity": "legendary",
        "defense": 80,
        "hp": 300,
        "description": "The miraculous of the turtle.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Shelter", "Protection", "Shell armor"],
        "set": "protection_set",
        "auction_only": True
    },
    "duusu_brooch": {
        "name": "Duusu's Brooch",
        "type": "artifact",
        "rarity": "legendary",
        "mana": 250,
        "description": "The miraculous of the peacock.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Amok", "Emotion control", "Sentimonster creation"],
        "set": "emotion_set",
        "auction_only": True
    },
    "nooroo_brooch": {
        "name": "Nooroo's Brooch",
        "type": "artifact",
        "rarity": "mythical",
        "mana": 300,
        "description": "The miraculous of transmission.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Akumatization", "Power transmission", "Dark energy"],
        "set": "transmission_set",
        "auction_only": True
    },
    "longg_necklace": {
        "name": "Longg's Necklace",
        "type": "artifact",
        "rarity": "legendary",
        "attack": 90,
        "description": "The miraculous of the dragon.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Storm", "Lightning", "Wind", "Water"],
        "set": "storm_set",
        "auction_only": True
    },
    "sass_bracelet": {
        "name": "Sass's Bracelet",
        "type": "artifact",
        "rarity": "legendary",
        "description": "The miraculous of the snake.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Second Chance", "Time loops", "Temporal reset"],
        "set": "time_set",
        "auction_only": True
    },
    "kaalki_glasses": {
        "name": "Kaalki's Glasses",
        "type": "artifact",
        "rarity": "legendary",
        "description": "The miraculous of the horse.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Voyage", "Portal creation", "Teleportation"],
        "set": "portal_set",
        "auction_only": True
    },
    "ziggy_goat": {
        "name": "Ziggy's Choker",
        "type": "artifact",
        "rarity": "legendary",
        "description": "The miraculous of the goat.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Genesis", "Object creation", "Material mastery"],
        "set": "creation_minor_set",
        "auction_only": True
    },
    "xuppu_crown": {
        "name": "Xuppu's Crown",
        "type": "artifact",
        "rarity": "legendary",
        "description": "The miraculous of the monkey.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Uproar", "Power disruption", "Chaos"],
        "set": "disruption_set",
        "auction_only": True
    },
    "orikko_rooster": {
        "name": "Orikko's Talon",
        "type": "artifact",
        "rarity": "legendary",
        "description": "The miraculous of the rooster.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Sublimation", "Power manifestation", "Ability creation"],
        "set": "manifestation_set",
        "auction_only": True
    },
    "barkk_collar": {
        "name": "Barkk's Collar",
        "type": "artifact",
        "rarity": "legendary",
        "description": "The miraculous of the dog.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Fetch", "Location tracking", "Retrieval"],
        "set": "tracking_set",
        "auction_only": True
    },
    "mullo_pendant": {
        "name": "Mullo's Pendant",
        "type": "artifact",
        "rarity": "legendary",
        "description": "The miraculous of the mouse.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Multitude", "Size manipulation", "Multiplication"],
        "set": "multiplication_set",
        "auction_only": True
    },
    "stompp_nose_ring": {
        "name": "Stompp's Nose Ring",
        "type": "artifact",
        "rarity": "legendary",
        "attack": 70,
        "description": "The miraculous of the ox.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Resistance", "Immovable force", "Strength boost"],
        "set": "strength_set",
        "auction_only": True
    },
    "roaar_tiger": {
        "name": "Roaar's Panjas",
        "type": "artifact",
        "rarity": "legendary",
        "attack": 85,
        "description": "The miraculous of the tiger.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Clout", "Energy projection", "Force blast"],
        "set": "energy_set",
        "auction_only": True
    },
    "fluff_watch": {
        "name": "Fluff's Watch",
        "type": "artifact",
        "rarity": "mythical",
        "description": "The miraculous of the rabbit.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Burrow", "Time travel", "Timeline access"],
        "set": "time_master_set",
        "auction_only": True
    },
    "liiri_eagle": {
        "name": "Liiri's Talon",
        "type": "artifact",
        "rarity": "legendary",
        "description": "The miraculous of the eagle.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Liberation", "Freedom", "Barrier breaking"],
        "set": "liberation_set",
        "auction_only": True
    },
    "gimmi_reality": {
        "name": "Gimmi's Reality Stone",
        "type": "artifact",
        "rarity": "cosmic",
        "attack": 500,
        "defense": 500,
        "hp": 1000,
        "mana": 1000,
        "description": "The ultimate kwami artifact.",
        "price": 0,
        "sell_price": 0,
        "effects": ["Reality control", "Wish granting", "Universe manipulation"],
        "set": "reality_set",
        "auction_only": True,
        "owner_only": True
    }
}

# Kwami Artifact Sets
KWAMI_ARTIFACT_SETS = {
    "ladybug": {
        "name": "Ladybug Set",
        "emoji": "🐞",
        "pieces": ["Ladybug Earrings", "Ladybug Suit", "Ladybug Yo-yo", "Ladybug Mask", "Ladybug Boots", "Ladybug Gloves"],
        "set_bonuses": {
            2: "Lucky Strike: +10% critical hit chance",
            4: "Miraculous Luck: +15% dodge chance", 
            6: "Lucky Charm: Can create beneficial items once per battle"
        },
        "theme": "Luck and Protection"
    },
    "cat": {
        "name": "Cat Set",
        "emoji": "🐱",
        "pieces": ["Cat Ring", "Cat Suit", "Cat Staff", "Cat Mask", "Cat Boots", "Cat Gloves"],
        "set_bonuses": {
            2: "Destruction Focus: +10% critical hit chance",
            4: "Cataclysm Power: +20% critical hit damage",
            6: "Plagg's Chaos: Critical hits have 25% chance to trigger Cataclysm"
        },
        "theme": "Destruction and Critical Hits"
    },
    "bee": {
        "name": "Bee Set", 
        "emoji": "🐝",
        "pieces": ["Bee Comb", "Bee Suit", "Bee Spinner", "Bee Mask", "Bee Boots", "Bee Gloves"],
        "set_bonuses": {
            2: "Venom Sting: +15% status effect chance",
            4: "Paralysis: Critical hits paralyze enemies for 1 turn",
            6: "Queen Bee: Can command paralyzed enemies to attack each other"
        },
        "theme": "Paralysis and Control"
    },
    "fox": {
        "name": "Fox Set",
        "emoji": "🦊", 
        "pieces": ["Fox Necklace", "Fox Suit", "Fox Flute", "Fox Mask", "Fox Boots", "Fox Gloves"],
        "set_bonuses": {
            2: "Illusion: +10% dodge chance",
            4: "Mirage: When hit, 30% chance to create illusion copy",
            6: "Grand Illusion: Can become invisible for 2 turns once per battle"
        },
        "theme": "Illusion and Deception"
    },
    "turtle": {
        "name": "Turtle Set",
        "emoji": "🐢",
        "pieces": ["Turtle Bracelet", "Turtle Suit", "Turtle Shield", "Turtle Mask", "Turtle Boots", "Turtle Gloves"],
        "set_bonuses": {
            2: "Shell Defense: +200 Max HP",
            4: "Protective Aura: +20% healing received",
            6: "Shelter: Can protect all allies with impenetrable shield for 1 turn"
        },
        "theme": "Defense and Healing"
    },
    "peacock": {
        "name": "Peacock Set",
        "emoji": "🦚",
        "pieces": ["Peacock Brooch", "Peacock Suit", "Peacock Fan", "Peacock Mask", "Peacock Boots", "Peacock Gloves"],
        "set_bonuses": {
            2: "Emotional Resonance: +100 Max MP",
            4: "Amok Creation: Can create emotion-based minions",
            6: "Emotional Mastery: Can control enemy emotions and actions"
        },
        "theme": "Emotion and Mind Control"
    }
}

# Tactical Monsters for Combat
TACTICAL_MONSTERS = {
    "goblin": {
        "name": "Goblin Warrior",
        "level": 1,
        "hp": 80,
        "attack": 12,
        "defense": 8,
        "weaknesses": ["Fire", "Light"],
        "resistances": ["Dark"],
        "skills": ["Crude Strike", "Goblin Shriek"],
        "xp_reward": 300,  # Doubled
        "gold_reward": 150,  # Doubled
        "item_drops": ["iron_ore", "health_potion", "mana_potion"],
        "drop_rates": {"common": 60, "uncommon": 25, "rare": 10},
        "description": "A small but vicious green-skinned warrior."
    },
    "orc": {
        "name": "Orc Brute", 
        "level": 5,
        "hp": 200,
        "attack": 25,
        "defense": 15,
        "weaknesses": ["Ice", "Lightning"],
        "resistances": ["Physical"],
        "skills": ["Brutal Swing", "War Cry", "Berserker Rage"],
        "xp_reward": 800,  # Doubled
        "gold_reward": 400,  # Doubled
        "item_drops": ["steel_ingot", "strength_elixir", "iron_sword"],
        "drop_rates": {"common": 50, "uncommon": 30, "rare": 15, "epic": 5},
        "description": "A massive green warrior with incredible strength."
    },
    "skeleton": {
        "name": "Undead Skeleton",
        "level": 3,
        "hp": 120,
        "attack": 18,
        "defense": 12,
        "weaknesses": ["Holy", "Fire"],
        "resistances": ["Dark", "Physical"],
        "skills": ["Bone Strike", "Death Rattle"],
        "xp_reward": 500,  # Doubled
        "gold_reward": 250,  # Doubled
        "item_drops": ["ancient_bone", "holy_water", "bone_armor"],
        "drop_rates": {"common": 55, "uncommon": 25, "rare": 15, "epic": 5},
        "description": "The reanimated bones of a fallen warrior."
    },
    "dragon": {
        "name": "Ancient Dragon",
        "level": 25,
        "hp": 2000,
        "attack": 80,
        "defense": 40,
        "weaknesses": ["Ice", "Dragon"],
        "resistances": ["Fire", "Physical"],
        "skills": ["Dragon Breath", "Wing Buffet", "Ancient Roar", "Fire Storm"],
        "xp_reward": 15000,  # Tripled
        "gold_reward": 7500,  # Tripled
        "item_drops": ["dragon_scale", "dragon_fang", "phoenix_feather", "fire_resistance_potion"],
        "drop_rates": {"uncommon": 40, "rare": 30, "epic": 20, "legendary": 10},
        "description": "A massive ancient dragon with scales like armor."
    },
    "akuma": {
        "name": "Akumatized Villain",
        "level": 10,
        "hp": 500,
        "attack": 35,
        "defense": 20,
        "weaknesses": ["Light", "Purification"],
        "resistances": ["Dark", "Emotional"],
        "skills": ["Emotional Outburst", "Dark Power", "Villain Transformation"],
        "xp_reward": 1600,  # Doubled
        "gold_reward": 800,  # Doubled
        "item_drops": ["shadow_essence", "emotion_crystal", "dark_armor"],
        "drop_rates": {"common": 45, "uncommon": 30, "rare": 20, "epic": 5},
        "description": "A person corrupted by Hawk Moth's dark magic."
    }
}

# Dungeon Data
DUNGEONS = {
    "sewer": {
        "name": "Sewer Depths",
        "min_level": 1,
        "max_level": 10,
        "floors": 5,
        "description": "Dark tunnels beneath Paris filled with mutated creatures.",
        "monsters": ["goblin", "skeleton", "sewer_rat"],
        "boss": "Sewer King",
        "rewards": ["Sewer Key", "Rat Fang", "Moldy Cheese"]
    },
    "cathedral": {
        "name": "Abandoned Cathedral", 
        "min_level": 10,
        "max_level": 20,
        "floors": 7,
        "description": "A once-holy place now corrupted by dark forces.",
        "monsters": ["skeleton", "ghost", "gargoyle"],
        "boss": "Fallen Angel",
        "rewards": ["Holy Water", "Angel Feather", "Blessed Sword"]
    },
    "stronghold": {
        "name": "Akuma Stronghold",
        "min_level": 20,
        "max_level": 30,
        "floors": 10,
        "description": "Hawk Moth's fortress where akumas are created.",
        "monsters": ["akuma", "sentimonster", "dark_moth"],
        "boss": "Shadow Moth",
        "rewards": ["Akuma Butterfly", "Dark Miraculous", "Evil Energy"]
    }
}

# Achievement Categories and Tiers
ACHIEVEMENT_TIERS = {
    "bronze": {
        "name": "Bronze",
        "emoji": "🥉",
        "color": 0xCD7F32,
        "xp_range": (100, 500),
        "gold_range": (100, 1000)
    },
    "silver": {
        "name": "Silver", 
        "emoji": "🥈",
        "color": 0xC0C0C0,
        "xp_range": (500, 1500),
        "gold_range": (1000, 5000)
    },
    "gold": {
        "name": "Gold",
        "emoji": "🥇",
        "color": 0xFFD700,
        "xp_range": (1500, 3000),
        "gold_range": (5000, 15000)
    },
    "platinum": {
        "name": "Platinum",
        "emoji": "💎",
        "color": 0xE5E4E2,
        "xp_range": (3000, 7500),
        "gold_range": (15000, 50000)
    },
    "legendary": {
        "name": "Legendary",
        "emoji": "🌟",
        "color": 0xFF6600,
        "xp_range": (7500, 15000),
        "gold_range": (50000, 150000)
    },
    "mythic": {
        "name": "Mythic",
        "emoji": "✨",
        "color": 0x9932CC,
        "xp_range": (15000, 30000),
        "gold_range": (150000, 500000)
    }
}

# Bot Owner ID with special privileges
OWNER_ID = 1297013439125917766

# Owner commands and abilities
OWNER_PRIVILEGES = {
    "unlimited_gold": True,
    "all_items": True,
    "admin_commands": True,
    "spawn_items": True,
    "modify_player_data": True,
    "create_events": True,
    "access_hidden_content": True
}

# Character Classes with enhanced data
CHARACTER_CLASSES = {
    "warrior": {
        "name": "Warrior",
        "emoji": "⚔️",
        "role": "Tank/DPS",
        "description": "Masters of physical combat and unwavering defense",
        "base_stats": {"strength": 15, "constitution": 12, "dexterity": 8, "intelligence": 5, "wisdom": 8, "charisma": 7},
        "starting_skills": ["shield_bash", "berserker_rage", "taunt"],
        "passive": "Iron Will: +25% resistance to debuffs and fear effects",
        "ultimate": "Blade Storm: Devastating multi-hit attack that ignores armor",
        "preferred_weapons": ["sword", "axe", "mace"],
        "class_bonus": {"physical_damage": 0.15, "armor_penetration": 0.10}
    },
    "mage": {
        "name": "Mage",
        "emoji": "🔮",
        "role": "Burst DPS",
        "description": "Wielders of arcane magic and elemental destruction",
        "base_stats": {"strength": 5, "constitution": 8, "dexterity": 7, "intelligence": 15, "wisdom": 12, "charisma": 8},
        "starting_skills": ["fireball", "ice_shard", "mana_shield"],
        "passive": "Arcane Mastery: Spells have 15% chance to not consume mana",
        "ultimate": "Arcane Devastation: Massive area spell that pierces all resistances",
        "preferred_weapons": ["staff", "wand", "orb"],
        "class_bonus": {"spell_damage": 0.20, "mana_efficiency": 0.15}
    },
    "rogue": {
        "name": "Rogue",
        "emoji": "🗡️",
        "role": "Assassin",
        "description": "Swift shadows who strike from darkness with lethal precision",
        "base_stats": {"strength": 8, "constitution": 10, "dexterity": 15, "intelligence": 10, "wisdom": 7, "charisma": 5},
        "starting_skills": ["stealth_strike", "poison_blade", "shadow_step"],
        "passive": "Shadow Mastery: First attack each combat is guaranteed critical hit",
        "ultimate": "Thousand Cuts: Rapid succession of strikes with increasing damage",
        "preferred_weapons": ["dagger", "short_sword", "bow"],
        "class_bonus": {"critical_chance": 0.15, "dodge_chance": 0.10}
    },
    "archer": {
        "name": "Archer",
        "emoji": "🏹",
        "role": "Ranged DPS",
        "description": "Masters of precision who rain death from afar",
        "base_stats": {"strength": 10, "constitution": 9, "dexterity": 15, "intelligence": 8, "wisdom": 10, "charisma": 3},
        "starting_skills": ["piercing_shot", "multi_shot", "eagle_eye"],
        "passive": "Eagle Eye: Attacks ignore 50% of enemy dodge chance",
        "ultimate": "Rain of Arrows: Devastating barrage that hits all enemies",
        "preferred_weapons": ["bow", "crossbow", "throwing_weapon"],
        "class_bonus": {"range_damage": 0.20, "accuracy": 0.15}
    },
    "healer": {
        "name": "Healer",
        "emoji": "✨",
        "role": "Support",
        "description": "Divine conduits who mend wounds and protect allies",
        "base_stats": {"strength": 5, "constitution": 10, "dexterity": 7, "intelligence": 12, "wisdom": 15, "charisma": 6},
        "starting_skills": ["heal", "group_heal", "divine_protection"],
        "passive": "Divine Favor: Healing spells have 25% chance to grant temporary immunity",
        "ultimate": "Divine Intervention: Massive heal and resurrection of fallen allies",
        "preferred_weapons": ["staff", "mace", "holy_symbol"],
        "class_bonus": {"healing_power": 0.30, "support_effectiveness": 0.20}
    },
    "battlemage": {
        "name": "Battlemage",
        "emoji": "⚡",
        "role": "Hybrid DPS",
        "description": "Warriors who blend steel and sorcery in perfect harmony",
        "base_stats": {"strength": 12, "constitution": 10, "dexterity": 8, "intelligence": 12, "wisdom": 9, "charisma": 9},
        "starting_skills": ["flame_blade", "spell_sword", "elemental_weapon"],
        "passive": "Spell Sword: Weapon attacks have 20% chance to trigger spell effects",
        "ultimate": "Elemental Fury: Weapons become infused with all elements temporarily",
        "preferred_weapons": ["enchanted_sword", "staff", "magical_weapon"],
        "class_bonus": {"hybrid_damage": 0.15, "elemental_mastery": 0.10}
    },
    "chrono_knight": {
        "name": "Chrono Knight",
        "emoji": "⏰",
        "role": "Time Manipulator",
        "description": "Temporal warriors who bend time itself to their will",
        "base_stats": {"strength": 11, "constitution": 11, "dexterity": 12, "intelligence": 11, "wisdom": 12, "charisma": 8},
        "starting_skills": ["time_strike", "temporal_shield", "chronos_blessing"],
        "passive": "Temporal Mastery: 15% chance to take an extra turn after any action",
        "ultimate": "Time Fracture: Rewind enemy actions and multiply your own",
        "preferred_weapons": ["temporal_blade", "chrono_staff", "time_crystal"],
        "class_bonus": {"time_manipulation": 0.20, "turn_efficiency": 0.15}
    }
}

# Level progression
def XP_FOR_NEXT_LEVEL(level):
    """Calculate XP needed for next level."""
    return int(100 * (1.5 ** (level - 1)))

STAT_POINTS_PER_LEVEL = 2

# Rarity colors for embeds
RARITY_COLORS = {
    'common': 0x808080,     # Gray
    'uncommon': 0x00FF00,   # Green  
    'rare': 0x0080FF,       # Blue
    'epic': 0x8000FF,       # Purple
    'legendary': 0xFFD700,  # Gold
    'mythic': 0xFF0080,     # Pink
    'divine': 0x00FFFF,     # Cyan
    'cosmic': 0xFF4500      # Orange Red
}

# Expanded item database with detailed stats and hidden items
ITEMS = {
    # Common Weapons
    "rusty_dagger": {
        "name": "Rusty Dagger",
        "type": "weapon",
        "rarity": "common",
        "price": 50,
        "attack": 8,
        "description": "A worn dagger that's seen better days",
        "effects": []
    },
    "wooden_sword": {
        "name": "Wooden Sword",
        "type": "weapon",
        "rarity": "common",
        "price": 100,
        "attack": 12,
        "description": "Basic training sword made of sturdy oak",
        "effects": []
    },
    "iron_sword": {
        "name": "Iron Sword",
        "type": "weapon",
        "rarity": "uncommon",
        "price": 500,
        "attack": 25,
        "description": "A reliable iron blade forged by skilled smiths",
        "effects": []
    },
    "steel_blade": {
        "name": "Steel Blade",
        "type": "weapon",
        "rarity": "rare",
        "price": 2000,
        "attack": 45,
        "critical_chance": 5,
        "description": "Superior steel crafted with precision",
        "effects": ["5% chance to ignore armor"]
    },
    "mithril_sword": {
        "name": "Mithril Sword",
        "type": "weapon",
        "rarity": "epic",
        "price": 10000,
        "attack": 75,
        "critical_chance": 10,
        "critical_damage": 150,
        "description": "Legendary mithril blade, light as a feather, sharp as death",
        "effects": ["Ignores 25% of enemy defense", "10% chance for double strike"]
    },

    # Legendary Weapons
    "plagg_claw": {
        "name": "Plagg's Claw",
        "type": "weapon",
        "rarity": "legendary",
        "price": 100000,
        "attack": 150,
        "critical_chance": 25,
        "critical_damage": 200,
        "description": "Forged from Plagg's own essence, radiates chaotic power",
        "effects": ["Cataclysm: 15% chance to destroy enemy equipment", "Chaos Strike: Damage varies wildly (50-300% base)"],
        "set_bonus": "Destruction Set: +50% damage to structures"
    },

    # Hidden/Divine Weapons (Owner only)
    "reality_render": {
        "name": "Reality Render",
        "type": "weapon",
        "rarity": "cosmic",
        "price": 1000000,
        "attack": 500,
        "critical_chance": 50,
        "critical_damage": 500,
        "description": "A blade that cuts through the fabric of reality itself",
        "effects": ["Dimensional Slash: Ignores all defenses", "Reality Break: 25% chance to delete enemy from existence"],
        "owner_only": True
    },

    # Armor Sets
    "leather_vest": {
        "name": "Leather Vest",
        "type": "armor",
        "rarity": "common",
        "price": 150,
        "defense": 10,
        "hp": 25,
        "description": "Basic leather protection for novice adventurers",
        "effects": []
    },
    "chainmail_armor": {
        "name": "Chainmail Armor",
        "type": "armor",
        "rarity": "uncommon",
        "price": 800,
        "defense": 25,
        "hp": 75,
        "description": "Interlocked metal rings provide solid protection",
        "effects": ["10% chance to reduce incoming damage by half"]
    },
    "plate_armor": {
        "name": "Plate Armor",
        "type": "armor",
        "rarity": "rare",
        "price": 3000,
        "defense": 50,
        "hp": 150,
        "description": "Heavy plate armor favored by knights",
        "effects": ["Damage reduction: -5 damage from all attacks", "Immunity to critical hits from common weapons"]
    },
    "dragon_scale_mail": {
        "name": "Dragon Scale Mail",
        "type": "armor",
        "rarity": "epic",
        "price": 15000,
        "defense": 100,
        "hp": 300,
        "mana": 100,
        "description": "Armor crafted from authentic dragon scales",
        "effects": ["Fire immunity", "25% magic resistance", "Intimidation aura: -10% enemy accuracy"]
    },

    # Legendary Armor
    "tikki_blessing": {
        "name": "Tikki's Blessing",
        "type": "armor",
        "rarity": "legendary",
        "price": 75000,
        "defense": 200,
        "hp": 500,
        "mana": 200,
        "description": "Blessed by the Kwami of Creation herself",
        "effects": ["Lucky Charm: 20% chance to negate any attack", "Creative Force: Regenerate 5% HP per turn", "Miraculous Shield: Immunity to instant death"],
        "set_bonus": "Creation Set: All abilities cost no mana"
    },

    # Consumables
    "health_potion": {
        "name": "Health Potion",
        "type": "consumable",
        "rarity": "common",
        "price": 50,
        "heal_amount": 100,
        "description": "Restores 100 HP instantly",
        "effects": ["Instant heal: +100 HP"]
    },
    "mana_potion": {
        "name": "Mana Potion",
        "type": "consumable",
        "rarity": "common",
        "price": 75,
        "mana_amount": 50,
        "description": "Restores 50 Mana instantly",
        "effects": ["Instant mana: +50 MP"]
    },
    "greater_health_potion": {
        "name": "Greater Health Potion",
        "type": "consumable",
        "rarity": "rare",
        "price": 500,
        "heal_amount": 500,
        "description": "Restores 500 HP and removes debuffs",
        "effects": ["Instant heal: +500 HP", "Removes all negative status effects"]
    },
    "elixir_of_power": {
        "name": "Elixir of Power",
        "type": "consumable",
        "rarity": "epic",
        "price": 2000,
        "description": "Temporarily doubles all stats for 5 battles",
        "effects": ["Power Surge: +100% to all stats for 5 battles"]
    },

    # Combat Consumables
    "explosive_arrow": {
        "name": "Explosive Arrow",
        "type": "consumable",
        "rarity": "uncommon",
        "price": 150,
        "description": "Special arrow that explodes on impact",
        "effects": ["Required for Archer's Explosive Shot skill"]
    },
    "holy_water": {
        "name": "Holy Water",
        "type": "consumable",
        "rarity": "rare",
        "price": 300,
        "description": "Blessed water that enhances healing abilities",
        "effects": ["Required for Healer's Mass Heal skill"]
    },
    "smoke_bomb": {
        "name": "Smoke Bomb",
        "type": "consumable",
        "rarity": "uncommon",
        "price": 200,
        "description": "Creates a cloud of concealing smoke",
        "effects": ["Required for Rogue's Vanish skill"]
    },
    "energy_drink": {
        "name": "Energy Drink",
        "type": "consumable",
        "rarity": "common",
        "price": 100,
        "ultimate_energy": 30,
        "description": "Caffeinated beverage that boosts energy",
        "effects": ["ultimate_energy"]
    },
    "battle_ration": {
        "name": "Battle Ration",
        "type": "consumable",
        "rarity": "common",
        "price": 75,
        "heal_amount": 35,
        "mana_amount": 15,
        "description": "Military-grade food that restores HP and Mana",
        "effects": []
    },
    "berserker_brew": {
        "name": "Berserker Brew",
        "type": "consumable",
        "rarity": "rare",
        "price": 400,
        "description": "Dangerous potion that grants temporary power",
        "effects": ["temporary_boost", "remove_debuffs"]
    },

    # Hidden Consumables
    "plagg_cheese": {
        "name": "Plagg's Special Camembert",
        "type": "consumable",
        "rarity": "legendary",
        "price": 10000,
        "heal_amount": 100,
        "description": "Plagg's favorite cheese, grants his blessing",
        "effects": ["chaos_blessing", "ultimate_energy"]
    },

    # Accessories
    "silver_ring": {
        "name": "Silver Ring",
        "type": "accessory",
        "rarity": "common",
        "price": 200,
        "attack": 5,
        "description": "A simple silver band with minor enchantments",
        "effects": []
    },
    "amulet_of_protection": {
        "name": "Amulet of Protection",
        "type": "accessory",
        "rarity": "uncommon",
        "price": 1000,
        "defense": 15,
        "hp": 50,
        "description": "Provides magical protection against harm",
        "effects": ["5% chance to completely avoid damage"]
    },
    "ring_of_power": {
        "name": "Ring of Power",
        "type": "accessory",
        "rarity": "rare",
        "price": 5000,
        "attack": 25,
        "mana": 100,
        "critical_chance": 10,
        "description": "Ancient ring pulsing with magical energy",
        "effects": ["Spell crit: Magic attacks can critical hit", "Mana efficiency: -25% spell costs"]
    },

    # Kwami Artifacts (Set items)
    "tikki_earrings": {
        "name": "Tikki's Earrings",
        "type": "artifact",
        "rarity": "legendary",
        "price": 50000,
        "slot": "head",
        "set": "creation_set",
        "hp": 200,
        "mana": 150,
        "description": "The miraculous of the ladybug, grants creation powers",
        "effects": ["Lucky Charm: Create helpful items in battle", "Miraculous Ladybug: Heal all allies"],
        "set_bonus": "2-piece: +25% healing | 4-piece: Revive with 50% HP when defeated"
    },
    "plagg_ring": {
        "name": "Plagg's Ring",
        "type": "artifact",
        "rarity": "legendary",
        "price": 50000,
        "slot": "hands",
        "set": "destruction_set",
        "attack": 100,
        "critical_damage": 50,
        "description": "The miraculous of the black cat, grants destruction powers",
        "effects": ["Cataclysm: Destroy enemy equipment", "Nine Lives: Avoid death 9 times"],
        "set_bonus": "2-piece: +50% crit damage | 4-piece: Cataclysm affects all enemies"
    },

    # Owner-only God Items
    "admin_blade": {
        "name": "Administrator's Edge",
        "type": "weapon",
        "rarity": "divine",
        "price": 0,
        "attack": 9999,
        "critical_chance": 100,
        "critical_damage": 1000,
        "description": "The weapon of absolute authority",
        "effects": ["Admin Strike: Instantly defeats any non-boss enemy", "Command: Force enemies to flee", "Debug: See all hidden stats"],
        "owner_only": True
    },
    "god_armor": {
        "name": "Divinity's Embrace",
        "type": "armor",
        "rarity": "divine",
        "price": 0,
        "defense": 9999,
        "hp": 999999,
        "mana": 999999,
        "description": "Armor befitting a god",
        "effects": ["Invulnerability: Immune to all damage", "Omnipresence: Act infinite times per turn", "Divine Aura: All allies gain +1000% stats"],
        "owner_only": True
    }
}

# Kwami Artifact Sets
KWAMI_ARTIFACT_SETS = {
    "creation_set": {
        "name": "Miraculous of Creation",
        "kwami": "Tikki",
        "bonuses": {
            2: {"description": "+25% healing power", "effect": "healing_boost_25"},
            4: {"description": "Revive with 50% HP when defeated", "effect": "miraculous_revival"}
        }
    },
    "destruction_set": {
        "name": "Miraculous of Destruction", 
        "kwami": "Plagg",
        "bonuses": {
            2: {"description": "+50% critical damage", "effect": "crit_damage_boost_50"},
            4: {"description": "Cataclysm affects all enemies", "effect": "area_cataclysm"}
        }
    },
    "illusion_set": {
        "name": "Miraculous of Illusion",
        "kwami": "Trixx",
        "bonuses": {
            2: {"description": "+30% dodge chance", "effect": "dodge_boost_30"},
            4: {"description": "Mirage: Confuse all enemies", "effect": "mass_confusion"}
        }
    },
    "transmission_set": {
        "name": "Miraculous of Transmission",
        "kwami": "Nooroo",
        "bonuses": {
            2: {"description": "+40% ability range", "effect": "range_boost_40"},
            4: {"description": "Share abilities with all allies", "effect": "power_transmission"}
        }
    },
    "emotion_set": {
        "name": "Miraculous of Emotion",
        "kwami": "Duusu",
        "bonuses": {
            2: {"description": "+35% status effect duration", "effect": "status_duration_35"},
            4: {"description": "Amok: Create powerful sentient beings", "effect": "amok_creation"}
        }
    }
}

# Crafting Recipes
CRAFTING_RECIPES = {
    "iron_sword": {
        "name": "Iron Sword",
        "materials": {"iron_ore": 3, "wood": 2},
        "result": "iron_sword",
        "skill_required": 1,
        "xp_reward": 15
    },
    "steel_armor": {
        "name": "Steel Armor",
        "materials": {"steel_ingot": 5, "leather": 3},
        "result": "steel_armor", 
        "skill_required": 3,
        "xp_reward": 25
    },
    "health_potion": {
        "name": "Health Potion",
        "materials": {"healing_herbs": 2, "water": 1},
        "result": "health_potion",
        "skill_required": 1,
        "xp_reward": 10
    },
    "mana_potion": {
        "name": "Mana Potion",
        "materials": {"mana_crystal": 1, "water": 1},
        "result": "mana_potion",
        "skill_required": 2,
        "xp_reward": 12
    }
}

# Tactical Skills for combat
TACTICAL_SKILLS = {
    "warrior": {
        "shield_bash": {
            "name": "Shield Bash",
            "description": "Stun enemy for 1 turn",
            "damage": 15,
            "mana_cost": 10,
            "cooldown": 2,
            "effect": "stun"
        },
        "berserker_rage": {
            "name": "Berserker Rage", 
            "description": "Double damage for 2 turns",
            "damage": 0,
            "mana_cost": 20,
            "cooldown": 4,
            "effect": "rage"
        }
    },
    "mage": {
        "fireball": {
            "name": "Fireball",
            "description": "High damage fire attack",
            "damage": 35,
            "mana_cost": 15,
            "cooldown": 1,
            "effect": "burn"
        },
        "ice_shard": {
            "name": "Ice Shard",
            "description": "Slow enemy movement",
            "damage": 25,
            "mana_cost": 12,
            "cooldown": 1,
            "effect": "slow"
        }
    },
    "rogue": {
        "stealth_strike": {
            "name": "Stealth Strike",
            "description": "High crit chance attack",
            "damage": 30,
            "mana_cost": 10,
            "cooldown": 2,
            "effect": "crit"
        },
        "poison_blade": {
            "name": "Poison Blade",
            "description": "Poison damage over time",
            "damage": 20,
            "mana_cost": 8,
            "cooldown": 1,
            "effect": "poison"
        }
    },
    "archer": {
        "piercing_shot": {
            "name": "Piercing Shot",
            "description": "Ignores armor",
            "damage": 28,
            "mana_cost": 12,
            "cooldown": 2,
            "effect": "pierce"
        },
        "multi_shot": {
            "name": "Multi Shot",
            "description": "Hit multiple targets",
            "damage": 20,
            "mana_cost": 15,
            "cooldown": 3,
            "effect": "multi"
        }
    },
    "healer": {
        "heal": {
            "name": "Heal",
            "description": "Restore HP to ally",
            "damage": -30,
            "mana_cost": 10,
            "cooldown": 1,
            "effect": "heal"
        },
        "group_heal": {
            "name": "Group Heal",
            "description": "Heal entire party",
            "damage": -20,
            "mana_cost": 25,
            "cooldown": 4,
            "effect": "group_heal"
        }
    }
}

# Tactical Monsters for combat encounters
TACTICAL_MONSTERS = {
    "goblin_warrior": {
        "name": "Goblin Warrior",
        "level": 3,
        "hp": 80,
        "max_hp": 80,
        "attack": 15,
        "defense": 8,
        "speed": 12,
        "xp_reward": 50,
        "gold_reward": 25,
        "rarity": "common",
        "ai_type": "aggressive",
        "abilities": ["power_strike", "intimidate"],
        "resistances": {},
        "weaknesses": {"fire": 1.5},
        "loot_table": {
            "rusty_dagger": 0.3,
            "health_potion": 0.5,
            "goblin_fang": 0.2
        }
    },
    "frost_elemental": {
        "name": "Frost Elemental",
        "level": 8,
        "hp": 150,
        "max_hp": 150,
        "attack": 25,
        "defense": 15,
        "speed": 8,
        "xp_reward": 120,
        "gold_reward": 60,
        "rarity": "uncommon",
        "ai_type": "defensive",
        "abilities": ["ice_shard", "frost_armor", "freeze"],
        "resistances": {"ice": 0.5, "water": 0.5},
        "weaknesses": {"fire": 2.0},
        "loot_table": {
            "ice_crystal": 0.6,
            "frost_essence": 0.3,
            "mana_potion": 0.4
        }
    },
    "shadow_assassin": {
        "name": "Shadow Assassin",
        "level": 12,
        "hp": 120,
        "max_hp": 120,
        "attack": 40,
        "defense": 10,
        "speed": 20,
        "xp_reward": 180,
        "gold_reward": 90,
        "rarity": "rare",
        "ai_type": "tactical",
        "abilities": ["stealth_strike", "shadow_step", "poison_blade"],
        "resistances": {"dark": 0.3},
        "weaknesses": {"light": 1.8},
        "loot_table": {
            "shadow_essence": 0.5,
            "poison_vial": 0.3,
            "stealth_cloak": 0.1
        }
    },
    "ancient_dragon": {
        "name": "Ancient Dragon",
        "level": 25,
        "hp": 800,
        "max_hp": 800,
        "attack": 80,
        "defense": 40,
        "speed": 15,
        "xp_reward": 1000,
        "gold_reward": 500,
        "rarity": "legendary",
        "ai_type": "boss",
        "abilities": ["dragon_breath", "wing_buffet", "tail_sweep", "intimidating_roar"],
        "resistances": {"fire": 0.2, "physical": 0.8},
        "weaknesses": {"ice": 1.5},
        "loot_table": {
            "dragon_scale": 0.8,
            "dragon_heart": 0.3,
            "legendary_gem": 0.1,
            "ancient_gold": 1.0
        }
    },
    "goblin_chieftain": {
        "name": "Goblin Chieftain",
        "level": 6,
        "hp": 200,
        "max_hp": 200,
        "attack": 30,
        "defense": 18,
        "speed": 10,
        "xp_reward": 300,
        "gold_reward": 150,
        "rarity": "rare",
        "ai_type": "boss",
        "abilities": ["war_cry", "tribal_rage", "commanding_shout"],
        "resistances": {},
        "weaknesses": {"magic": 1.3},
        "loot_table": {
            "chieftain_axe": 0.4,
            "tribal_mask": 0.3,
            "gold_pouch": 0.8
        }
    },
    "shadow_lord": {
        "name": "Shadow Lord",
        "level": 18,
        "hp": 500,
        "max_hp": 500,
        "attack": 60,
        "defense": 30,
        "speed": 18,
        "xp_reward": 800,
        "gold_reward": 400,
        "rarity": "epic",
        "ai_type": "boss",
        "abilities": ["shadow_realm", "dark_manipulation", "void_strike", "shadow_army"],
        "resistances": {"dark": 0.1, "physical": 0.7},
        "weaknesses": {"light": 2.0},
        "loot_table": {
            "shadow_crown": 0.5,
            "void_crystal": 0.4,
            "dark_essence": 0.8
        }
    },
    "ancient_red_dragon": {
        "name": "Ancient Red Dragon",
        "level": 35,
        "hp": 1500,
        "max_hp": 1500,
        "attack": 120,
        "defense": 60,
        "speed": 20,
        "xp_reward": 2000,
        "gold_reward": 1000,
        "rarity": "legendary",
        "ai_type": "boss",
        "abilities": ["inferno_breath", "meteor_strike", "dragon_fear", "ancient_magic", "fire_shield"],
        "resistances": {"fire": 0.0, "physical": 0.6},
        "weaknesses": {"ice": 1.8, "water": 1.5},
        "loot_table": {
            "red_dragon_scale": 0.9,
            "dragon_lord_heart": 0.5,
            "ancient_ruby": 0.3,
            "fire_essence": 0.8,
            "legendary_treasure": 0.2
        }
    },
    "artifact_guardian": {
        "name": "Artifact Guardian",
        "level": 20,
        "hp": 400,
        "max_hp": 400,
        "attack": 50,
        "defense": 35,
        "speed": 12,
        "xp_reward": 600,
        "gold_reward": 300,
        "rarity": "epic",
        "ai_type": "defensive",
        "abilities": ["guardian_shield", "artifact_power", "protective_barrier"],
        "resistances": {"magic": 0.5},
        "weaknesses": {"chaos": 1.5},
        "loot_table": {
            "artifact_fragment": 0.8,
            "guardian_essence": 0.4,
            "protection_rune": 0.3
        }
    },
    "kwami_phantom": {
        "name": "Kwami Phantom",
        "level": 22,
        "hp": 300,
        "max_hp": 300,
        "attack": 45,
        "defense": 25,
        "speed": 25,
        "xp_reward": 700,
        "gold_reward": 350,
        "rarity": "epic",
        "ai_type": "tactical",
        "abilities": ["phase_shift", "spectral_attack", "kwami_blessing"],
        "resistances": {"physical": 0.3},
        "weaknesses": {"miraculous": 2.0},
        "loot_table": {
            "kwami_essence": 0.7,
            "phantom_dust": 0.3,
            "ethereal_shard": 0.2
        }
    }
}

# Consumable Effects
CONSUMABLE_EFFECTS = {
    "health_potion": {
        "name": "Health Potion",
        "description": "Restores 100 HP",
        "effect_type": "heal",
        "amount": 100
    },
    "mana_potion": {
        "name": "Mana Potion",
        "description": "Restores 50 MP",
        "effect_type": "mana",
        "amount": 50
    },
    "greater_health_potion": {
        "name": "Greater Health Potion",
        "description": "Restores 500 HP and removes debuffs",
        "effect_type": "heal",
        "amount": 500,
        "remove_debuffs": True
    },
    "elixir_of_power": {
        "name": "Elixir of Power",
        "description": "Doubles all stats for 5 battles",
        "effect_type": "stat_boost",
        "duration": 5,
        "stat_multiplier": 2
    },
    "plagg_cheese": {
        "name": "Plagg's Special Camembert",
        "description": "Random massive stat boost",
        "effect_type": "random_stat_boost",
        "stat_range": (1.5, 3)
    }
}

# Dungeon Data with expanded info
DUNGEONS = {
    "sewer": {
        "name": "Sewer Depths",
        "description": "Dark tunnels beneath Paris filled with mutated creatures.",
        "min_level": 1,
        "max_level": 10,
        "floors": 5,
        "monsters": ["goblin_warrior", "sewer_rat", "slime"],
        "boss": "Sewer King",
        "boss_level": 8,
        "rewards": ["rusty_dagger", "health_potion", "sewer_key"],
        "environment": "dark",
        "threat_level": "low"
    },
    "forest": {
        "name": "Enchanted Forest",
        "description": "A mystical forest teeming with ancient spirits and magical beasts.",
        "min_level": 5,
        "max_level": 15,
        "floors": 7,
        "monsters": ["forest_sprite", "giant_spider", "treant"],
        "boss": "Forest Guardian",
        "boss_level": 12,
        "rewards": ["wooden_bow", "mana_potion", "forest_essence"],
        "environment": "lush",
        "threat_level": "medium"
    },
    "mountain": {
        "name": "Mount Cinderpeak",
        "description": "A volcanic mountain where fire elementals and dragons dwell.",
        "min_level": 10,
        "max_level": 20,
        "floors": 10,
        "monsters": ["fire_elemental", "lava_golem", "young_dragon"],
        "boss": "Magma Dragon",
        "boss_level": 18,
        "rewards": ["steel_blade", "fire_resistance_potion", "dragon_scale"],
        "environment": "scorched",
        "threat_level": "high"
    },
    "ice_cave": {
        "name": "Glacier's Maw",
        "description": "A frozen cavern guarded by frost elementals and ice giants.",
        "min_level": 15,
        "max_level": 25,
        "floors": 8,
        "monsters": ["ice_elemental", "frost_giant", "snow_leopard"],
        "boss": "Ice Queen",
        "boss_level": 22,
        "rewards": ["mithril_sword", "ice_amulet", "frost_essence"],
        "environment": "frozen",
        "threat_level": "dangerous"
    },
    "akuma_lair": {
        "name": "Hawk Moth's Lair",
        "description": "The hidden base of Hawk Moth where akumas are created.",
        "min_level": 20,
        "max_level": 30,
        "floors": 12,
        "monsters": ["akumatized_villain", "sentimonster", "shadow_minion"],
        "boss": "Hawk Moth",
        "boss_level": 28,
        "rewards": ["tikki_earrings", "plagg_ring", "akuma_butterfly"],
        "environment": "dark",
        "threat_level": "extreme"
    }
}

# Achievement Data with detailed requirements
ACHIEVEMENTS = {
    "first_steps": {
        "name": "First Steps",
        "description": "Embark on your RPG journey",
        "category": "exploration",
        "tier": "bronze",
        "xp_reward": 100,
        "gold_reward": 50,
        "requirement": "create_character"
    },
    "monster_slayer": {
        "name": "Monster Slayer",
        "description": "Defeat 10 monsters",
        "category": "combat",
        "tier": "silver",
        "xp_reward": 300,
        "gold_reward": 150,
        "requirement": "defeat_monsters",
        "amount": 10
    },
    "item_collector": {
        "name": "Item Collector",
        "description": "Collect 20 items",
        "category": "collection",
        "tier": "gold",
        "xp_reward": 500,
        "gold_reward": 250,
        "requirement": "collect_items",
        "amount": 20
    },
    "dungeon_delver": {
        "name": "Dungeon Delver",
        "description": "Complete 5 dungeons",
        "category": "exploration",
        "tier": "platinum",
        "xp_reward": 800,
        "gold_reward": 400,
        "requirement": "complete_dungeons",
        "amount": 5
    },
    "dragon_slayer": {
        "name": "Dragon Slayer",
        "description": "Defeat an Ancient Dragon",
        "category": "combat",
        "tier": "legendary",
        "xp_reward": 1200,
        "gold_reward": 600,
        "requirement": "defeat_boss",
        "boss": "ancient_dragon"
    },
    "hero_of_paris": {
        "name": "Hero of Paris",
        "description": "Defeat Hawk Moth in his lair",
        "category": "story",
        "tier": "mythic",
        "xp_reward": 2000,
        "gold_reward": 1000,
        "requirement": "defeat_boss",
        "boss": "hawk_moth"
    }
}

# Skill Tree Data
SKILL_TREES = {
    "warrior": {
        "name": "Warrior Skill Tree",
        "skills": {
            "shield_bash": {
                "name": "Shield Bash",
                "description": "Stuns the enemy with a powerful shield attack.",
                "type": "attack",
                "damage": 20,
                "mana_cost": 10,
                "cooldown": 2,
                "required_level": 1
            },
            "berserker_rage": {
                "name": "Berserker Rage",
                "description": "Increases attack damage but lowers defense for a short duration.",
                "type": "buff",
                "attack_boost": 0.5,
                "defense_nerf": 0.3,
                "duration": 3,
                "mana_cost": 20,
                "cooldown": 5,
                "required_level": 5
            },
            "iron_will": {
                "name": "Iron Will",
                "description": "Passive skill that increases resistance to status effects.",
                "type": "passive",
                "status_resistance": 0.25,
                "required_level": 10
            },
            "blade_storm": {
                "name": "Blade Storm",
                "description": "Unleashes a whirlwind of attacks hitting multiple enemies.",
                "type": "attack",
                "damage": 30,
                "targets": "all",
                "mana_cost": 30,
                "cooldown": 8,
                "required_level": 15
            }
        }
    },
    "mage": {
        "name": "Mage Skill Tree",
        "skills": {
            "fireball": {
                "name": "Fireball",
                "description": "Hurls a ball of fire dealing high damage.",
                "type": "attack",
                "damage": 40,
                "mana_cost": 15,
                "cooldown": 1,
                "required_level": 1
            },
            "ice_shard": {
                "name": "Ice Shard",
                "description": "Launches shards of ice that slow down enemies.",
                "type": "attack",
                "damage": 25,
                "slow_duration": 2,
                "mana_cost": 12,
                "cooldown": 1,
                "required_level": 5
            },
            "arcane_mastery": {
                "name": "Arcane Mastery",
                "description": "Passive skill that reduces mana cost for spells.",
                "type": "passive",
                "mana_cost_reduction": 0.15,
                "required_level": 10
            },
            "arcane_devastation": {
                "name": "Arcane Devastation",
                "description": "Unleashes a massive area spell dealing high damage.",
                "type": "attack",
                "damage": 50,
                "targets": "all",
                "mana_cost": 40,
                "cooldown": 10,
                "required_level": 15
            }
        }
    },
    "rogue": {
        "name": "Rogue Skill Tree",
        "skills": {
            "stealth_strike": {
                "name": "Stealth Strike",
                "description": "Deals high critical damage from stealth.",
                "type": "attack",
                "damage": 35,
                "crit_chance": 0.5,
                "mana_cost": 10,
                "cooldown": 3,
                "required_level": 1
            },
            "poison_blade": {
                "name": "Poison Blade",
                "description": "Poisons the enemy dealing damage over time.",
                "type": "attack",
                "damage": 15,
                "poison_duration": 3,
                "mana_cost": 8,
                "cooldown": 1,
                "required_level": 5
            },
            "shadow_mastery": {
                "name": "Shadow Mastery",
                "description": "Passive skill that increases critical hit chance.",
                "type": "passive",
                "crit_chance_boost": 0.15,
                "required_level": 10
            },
            "thousand_cuts": {
                "name": "Thousand Cuts",
                "description": "Rapidly strikes the enemy multiple times.",
                "type": "attack",
                "damage": 20,
                "hits": 5,
                "mana_cost": 30,
                "cooldown": 8,
                "required_level": 15
            }
        }
    },
    "archer": {
        "name": "Archer Skill Tree",
        "skills": {
            "piercing_shot": {
                "name": "Piercing Shot",
                "description": "Fires a shot that ignores enemy armor.",
                "type": "attack",
                "damage": 30,
                "armor_penetration": 1.0,
                "mana_cost": 12,
                "cooldown": 2,
                "required_level": 1
            },
            "multi_shot": {
                "name": "Multi Shot",
                "description": "Fires multiple arrows hitting multiple enemies.",
                "type": "attack",
                "damage": 15,
                "targets": "all",
                "mana_cost": 15,
                "cooldown": 3,
                "required_level": 5
            },
            "eagle_eye": {
                "name": "Eagle Eye",
                "description": "Passive skill that increases accuracy.",
                "type": "passive",
                "accuracy_boost": 0.20,
                "required_level": 10
            },
            "rain_of_arrows": {
                "name": "Rain of Arrows",
                "description": "Calls down a rain of arrows on all enemies.",
                "type": "attack",
                "damage": 25,
                "targets": "all",
                "mana_cost": 35,
                "cooldown": 10,
                "required_level": 15
            }
        }
    },
    "healer": {
        "name": "Healer Skill Tree",
        "skills": {
            "heal": {
                "name": "Heal",
                "description": "Restores health to an ally.",
                "type": "heal",
                "heal_amount": 50,
                "mana_cost": 10,
                "cooldown": 1,
                "required_level": 1
            },
            "group_heal": {
                "name": "Group Heal",
                "description": "Restores health to all allies.",
                "type": "heal",
                "heal_amount": 30,
                "targets": "all",
                "mana_cost": 25,
                "cooldown": 4,
                "required_level": 5
            },
            "divine_favor": {
                "name": "Divine Favor",
                "description": "Passive skill that increases healing power.",
                "type": "passive",
                "healing_boost": 0.20,
                "required_level": 10
            },
            "divine_intervention": {
                "name": "Divine Intervention",
                "description": "Massive heal and resurrection of fallen allies.",
                "type": "heal",
                "heal_amount": 100,
                "targets": "all",
                "resurrect": True,
                "mana_cost": 50,
                "cooldown": 12,
                "required_level": 15
            }
        }
    },
    "battlemage": {
        "name": "Battlemage Skill Tree",
        "skills": {
            "flame_blade": {
                "name": "Flame Blade",
                "description": "Enchants weapon with fire dealing extra damage.",
                "type": "attack",
                "damage": 15,
                "fire_damage": 10,
                "mana_cost": 15,
                "cooldown": 3,
                "required_level": 1
            },
            "spell_sword": {
                "name": "Spell Sword",
                "description": "Combines weapon attacks with spell effects.",
                "type": "attack",
                "damage": 20,
                "spell_chance": 0.3,
                "mana_cost": 18,
                "cooldown": 4,
                "required_level": 5
            },
            "spellsword": {
                "name": "Spellsword",
                "description": "Passive skill: Weapon attacks trigger spell effects.",
                "type": "passive",
                "spell_trigger_chance": 0.20,
                "required_level": 10
            },
            "elemental_fury": {
                "name": "Elemental Fury",
                "description": "Infuses weapon with all elements temporarily.",
                "type": "attack",
                "elemental_damage": 30,
                "duration": 4,
                "mana_cost": 35,
                "cooldown": 10,
                "required_level": 15
            }
        }
    },
    "chrono_knight": {
        "name": "Chrono Knight Skill Tree",
        "skills": {
            "time_strike": {
                "name": "Time Strike",
                "description": "Deals damage and slows down enemy's time.",
                "type": "attack",
                "damage": 25,
                "slow_duration": 1,
                "mana_cost": 12,
                "cooldown": 2,
                "required_level": 1
            },
            "temporal_shield": {
                "name": "Temporal Shield",
                "description": "Creates a shield that distorts time.",
                "type": "buff",
                "shield_amount": 50,
                "duration": 2,
                "mana_cost": 15,
                "cooldown": 3,
                "required_level": 5
            },
            "temporal_mastery": {
                "name": "Temporal Mastery",
                "description": "Passive skill: Chance to take extra turn.",
                "type": "passive",
                "extra_turn_chance": 0.15,
                "required_level": 10
            },
            "time_fracture": {
                "name": "Time Fracture",
                "description": "Rewinds enemy actions and multiplies yours.",
                "type": "attack",
                "rewind_chance": 0.2,
                "multiplier": 2,
                "mana_cost": 40,
                "cooldown": 12,
                "required_level": 15
            }
        }
    }
}

# Starting Items for Each Class
STARTING_ITEMS = {
    "warrior": ["iron_sword", "leather_vest", "health_potion"],
    "mage": ["wooden_staff", "mana_potion", "silver_ring"],
    "rogue": ["rusty_dagger", "leather_vest", "mana_potion"],
    "archer": ["wooden_bow", "leather_vest", "health_potion"],
    "healer": ["wooden_mace", "leather_vest", "mana_potion"],
    "battlemage": ["iron_sword", "mana_potion", "health_potion"],
    "chrono_knight": ["temporal_blade", "time_crystal", "health_potion"]
}

# Locations
LOCATIONS = {
    "paris": {
        "name": "Paris",
        "description": "The capital city of France, filled with iconic landmarks and hidden dangers.",
        "type": "city",
        "shops": ["weapon_shop", "armor_shop", "potion_shop"],
        "dungeons": ["sewer", "cathedral", "akuma_lair"],
        "events": ["akuma_attack", "fashion_show", "thief_encounter"],
        "population": "large",
        "threat_level": "medium"
    },
    "eiffel_tower": {
        "name": "Eiffel Tower",
        "description": "A famous landmark offering a stunning view of Paris.",
        "type": "landmark",
        "events": ["akuma_attack", "romantic_encounter"],
        "threat_level": "low",
        "population": "high"
    },
    "louvre_museum": {
        "name": "Louvre Museum",
        "description": "A world-renowned museum housing priceless artifacts.",
        "type": "landmark",
        "events": ["thief_encounter", "artifact_discovery"],
        "threat_level": "medium",
        "population": "high"
    },
    "notre_dame": {
        "name": "Notre Dame Cathedral",
        "description": "A historic cathedral undergoing restoration.",
        "type": "landmark",
        "events": ["ghost_encounter", "holy_relic"],
        "threat_level": "medium",
        "population": "low"
    },
    "sewer_system": {
        "name": "Paris Sewer System",
        "description": "A labyrinthine network beneath the city, home to mutated creatures.",
        "type": "dungeon",
        "dungeon": "sewer",
        "threat_level": "high"
    },
    "enchanted_forest": {
        "name": "Enchanted Forest",
        "description": "A mystical forest filled with magical creatures.",
        "type": "wilderness",
        "dungeons": ["forest"],
        "events": ["fairy_encounter", "lost_traveler"],
        "threat_level": "medium"
    }
}

# World Events
WORLD_EVENTS = {
    "akuma_attack": {
        "name": "Akuma Attack",
        "description": "An akumatized villain terrorizes the city.",
        "type": "combat",
        "monsters": ["akumatized_villain", "sentimonster"],
        "rewards": ["tikki_earrings", "plagg_ring", "akuma_butterfly"],
        "duration": 5,
        "location": "paris"
    },
    "fashion_show": {
        "name": "Paris Fashion Week",
        "description": "A glamorous event attracting celebrities and fashion enthusiasts.",
        "type": "social",
        "events": ["celebrity_encounter", "fashion_contest"],
        "duration": 3,
        "location": "paris"
    },
    "thief_encounter": {
        "name": "Thief Encounter",
        "description": "A cunning thief attempts to steal valuable items.",
        "type": "stealth",
        "monsters": ["thief"],
        "rewards": ["stolen_goods", "gold"],
        "duration": 1,
        "location": "paris"
    },
    "lost_traveler": {
        "name": "Lost Traveler",
        "description": "A wanderer seeks help finding their way.",
        "type": "quest",
        "rewards": ["compass", "map"],
        "duration": 1,
        "location": "enchanted_forest"
    }
}

# Shop Inventory Data
SHOP_INVENTORY = {
    "weapon_shop": {
        "name": "Weapon Shop",
        "items": ["rusty_dagger", "iron_sword", "steel_blade", "mithril_sword"],
        "location": "paris"
    },
    "armor_shop": {
        "name": "Armor Shop",
        "items": ["leather_vest", "chainmail_armor", "plate_armor", "dragon_scale_mail"],
        "location": "paris"
    },
    "potion_shop": {
        "name": "Potion Shop",
        "items": ["health_potion", "mana_potion", "greater_health_potion", "elixir_of_power"],
        "location": "paris"
    }
}

# Weaknesses and Resistances
ELEMENTAL_CHART = {
    "fire": {
        "weak_to": ["water", "ice"],
        "resists": ["fire", "earth"]
    },
    "water": {
        "weak_to": ["lightning", "earth"],
        "resists": ["water", "ice"]
    },
    "lightning": {
        "weak_to": ["earth"],
        "resists": ["lightning", "air"]
    },
    "ice": {
        "weak_to": ["fire"],
        "resists": ["water", "ice"]
    },
    "earth": {
        "weak_to": ["water", "air"],
        "resists": ["lightning", "earth"]
    },
    "air": {
        "weak_to": ["earth"],
        "resists": ["lightning", "air"]
    },
    "light": {
        "weak_to": ["dark"],
        "resists": ["holy"]
    },
    "dark": {
        "weak_to": ["light", "holy"],
        "resists": ["dark"]
    },
    "holy": {
        "weak_to": ["dark"],
        "resists": ["holy", "light"]
    },
}

# Status Effects
STATUS_EFFECTS = {
    "poison": {
        "name": "Poison",
        "description": "Deals damage over time.",
        "type": "debuff",
        "damage_per_turn": 5,
        "duration": 3
    },
    "stun": {
        "name": "Stun",
        "description": "Prevents the target from acting.",
        "type": "debuff",
        "duration": 1
    },
    "burn": {
        "name": "Burn",
        "description": "Deals fire damage over time.",
        "type": "debuff",
        "damage_per_turn": 8,
        "duration": 2
    },
    "slow": {
        "name": "Slow",
        "description": "Reduces the target's speed.",
        "type": "debuff",
        "speed_reduction": 0.5,
        "duration": 2
    },
    "rage": {
        "name": "Rage",
        "description": "Increases attack but reduces defense.",
        "type": "buff",
        "attack_boost": 0.3,
        "defense_reduction": 0.2,
        "duration": 3
    }
}

# AI Behavior
AI_BEHAVIOR = {
    "aggressive": {
        "description": "Always attacks the nearest target.",
        "priority": ["attack"]
    },
    "defensive": {
        "description": "Protects allies and heals when necessary.",
        "priority": ["defend", "heal"]
    },
    "tactical": {
        "description": "Uses skills strategically to exploit weaknesses.",
        "priority": ["debuff", "attack"]
    },
    "support": {
        "description": "Focuses on healing and buffing allies.",
        "priority": ["heal", "buff"]
    }
}

# Loot Tables
LOOT_TABLES = {
    "common": {
        "items": ["health_potion", "mana_potion", "rusty_dagger", "wooden_sword"],
        "chance": [0.3, 0.3, 0.2, 0.2]
    },
    "uncommon": {
        "items": ["steel_sword", "chainmail_armor", "greater_health_potion", "mana_potion"],
        "chance": [0.25, 0.25, 0.25, 0.25]
    },
    "rare": {
        "items": ["mithril_sword", "plate_armor", "elixir_of_power", "ring_of_power"],
        "chance": [0.2, 0.2, 0.3, 0.3]
    },
    "boss": {
        "items": ["tikki_earrings", "plagg_ring", "admin_blade", "god_armor"],
        "chance": [0.25, 0.25, 0.25, 0.25]
    }
}

# Quest Data
QUESTS = {
    "rescue_princess": {
        "name": "Rescue the Princess",
        "description": "A princess has been captured by a dragon and needs rescuing.",
        "objective": "Defeat the dragon and rescue the princess",
        "location": "mountain",
        "rewards": ["gold", "experience", "legendary_item"],
        "difficulty": "hard"
    },
    "recover_artifact": {
        "name": "Recover the Lost Artifact",
        "description": "A powerful artifact has been stolen and needs to be recovered.",
        "objective": "Find the artifact and return it to the museum",
        "location": "louvre_museum",
        "rewards": ["gold", "experience", "rare_item"],
        "difficulty": "medium"
    },
    "eliminate_threat": {
        "name": "Eliminate the Threat",
        "description": "A dangerous monster is terrorizing the town and needs to be eliminated.",
        "objective": "Defeat the monster and protect the town",
        "location": "paris",
        "rewards": ["gold", "experience", "uncommon_item"],
        "difficulty": "easy"
    }
}

# Dialogue Data
DIALOGUE = {
    "greeting": {
        "text": "Hello adventurer! What brings you to our town?",
        "responses": ["I'm looking for quests.", "Just passing through.", "Goodbye."]
    },
    "quest_offer": {
        "text": "We need help with a dangerous monster...",
        "responses": ["I'll help!", "Maybe later.", "Not interested."]
    },
    "quest_acceptance": {
        "text": "Thank you! Please defeat the monster and return for your reward.",
        "responses": ["Understood.", "I'm on it."]
    },
    "quest_completion": {
        "text": "You did it! Here is your reward.",
        "rewards": ["gold", "experience", "item"]
    }
}

# Crafting Materials Data
CRAFTING_MATERIALS = {
    "iron_ore": {
        "name": "Iron Ore",
        "description": "A raw material used to craft iron weapons and armor.",
        "rarity": "common",
        "value": 10
    },
    "wood": {
        "name": "Wood",
        "description": "A basic building material used in many crafts.",
        "rarity": "common",
        "value": 5
    },
    "steel_ingot": {
        "name": "Steel Ingot",
        "description": "A refined material used to craft steel weapons and armor.",
        "rarity": "uncommon",
        "value": 25
    },
    "leather": {
        "name": "Leather",
        "description": "Animal hide used to craft armor and clothing.",
        "rarity": "common",
        "value": 15
    },
    "healing_herbs": {
        "name": "Healing Herbs",
        "description": "Plants with medicinal properties used to craft potions.",
        "rarity": "common",
        "value": 20
    },
    "water": {
        "name": "Water",
        "description": "A basic ingredient used in many recipes.",
        "rarity": "common",
        "value": 1
    },
    "mana_crystal": {
        "name": "Mana Crystal",
        "description": "Crystals that contain magical energy used to craft potions.",
        "rarity": "uncommon",
        "value": 30
    }
}

# Shop Data
SHOPS = {
    "weapon_shop": {
        "name": "The Armory",
        "description": "A shop specializing in weapons and armor.",
        "items": ["iron_sword", "steel_blade", "mithril_sword", "rusty_dagger"],
        "location": "paris"
    },
    "armor_shop": {
        "name": "The Shield Wall",
        "description": "A shop specializing in armor and shields.",
        "items": ["leather_vest", "chainmail_armor", "plate_armor", "dragon_scale_mail"],
        "location": "paris"
    },
    "potion_shop": {
        "name": "The Alchemist's Cauldron",
        "description": "A shop specializing in potions and elixirs.",
        "items": ["health_potion", "mana_potion", "greater_health_potion", "elixir_of_power"],
        "location": "paris"
    }
}

# Game Settings
GAME_SETTINGS = {
    "xp_multiplier": 1.0,
    "gold_multiplier": 1.0,
    "drop_rate": 0.5,
    "critical_hit_chance": 0.1,
    "dodge_chance": 0.05
}

# Debug Settings
DEBUG_SETTINGS = {
    "debug_mode": False,
    "log_level": "info",
    "show_hitboxes": False
}

# Function to determine the rarity color for embeds
def get_rarity_color(rarity):
    """Returns the corresponding color for a given rarity."""
    return RARITY_COLORS.get(rarity.lower(), 0x95a5a6)

# Function to calculate item stats based on rarity
def calculate_item_stats(item):
    """Calculates item stats based on rarity."""
    rarity = item.get("rarity", "common").lower()
    multiplier = RARITY_MULTIPLIERS.get(rarity, 1.0)
    attack = item.get("attack", 0) * multiplier
    defense = item.get("defense", 0) * multiplier
    return attack, defense

# Function to generate random loot
def generate_loot(loot_table):
    """Generates random loot based on a loot table."""
    items = loot_table.get("items", [])
    chance = loot_table.get("chance", [])
    if not items or not chance or len(items) != len(chance):
        return None
    return random.choices(items, weights=chance, k=1)[0]

# Function to calculate damage
def calculate_damage(attacker, defender, skill):
    """Calculates the damage dealt in combat."""
    attack = attacker.get("attack", 10)
    defense = defender.get("defense", 5)
    damage = (attack - defense) * skill.get("damage", 1.0)
    return max(damage, 1)

# Function to apply status effects
def apply_status_effect(target, effect):
    """Applies a status effect to a target."""
    # Implementation to apply status effects
    pass

# Function to handle combat
def handle_combat(player, monster):
    """Handles combat between a player and a monster."""
    # Implementation of combat logic
    pass

# Function to run a dungeon
def run_dungeon(player, dungeon):
    """Runs a dungeon for a player."""
    # Implementation of dungeon logic
    pass

# Function to handle shops
def handle_shop(player, shop):
    """Handles shop interactions for a player."""
    # Implementation of shop logic
    pass

# Function to handle quests
import random

def handle_quest(player, quest):
    """Handles quest interactions for a player."""
    # Implementation of quest logic
    pass

#Function to check owner permissions
def check_owner_permissions(owner_id):
    return OWNER_PRIVILEGES if owner_id == OWNER_ID else None

# Function to calculate XP for next level
def calculate_xp_for_next_level(level):
    return int(100 * (1.5 ** (level - 1)))

# Function to get rarity color
def get_rarity_color(rarity):
    return RARITY_COLORS.get(rarity.lower(), 0x95a5a6)

# Function to calculate item stats
def calculate_item_stats(item):
    rarity = item.get("rarity", "common").lower()
    multiplier = RARITY_MULTIPLIERS.get(rarity, 1.0)
    attack = item.get("attack", 0) * multiplier
    defense = item.get("defense", 0) * multiplier
    return attack, defense

# Function to generate loot
def generate_loot(loot_table):
    items = loot_table.get("items", [])
    chance = loot_table.get("chance", [])
    if not items or not chance or len(items) != len(chance):
        return None
    return random.choices(items, weights=chance, k=1)[0]

# Function to calculate damage
def calculate_damage(attacker, defender, skill):
    attack = attacker.get("attack", 10)
    defense = defender.get("defense", 5)
    damage = (attack - defense) * skill.get("damage", 1.0)
    return max(damage, 1)

# Function to apply status effects
def apply_status_effect(target, effect):
    pass

# Function to handle combat
def handle_combat(player, monster):
    pass

# Function to run a dungeon
def run_dungeon(player, dungeon):
    pass

# Function to handle shops
def handle_shop(player, shop):
    pass

# Function to handle quests
def handle_quest(player, quest):
    pass