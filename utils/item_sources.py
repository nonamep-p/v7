
"""
Item Source Database - Tells players exactly how to obtain every item.
"""

from rpg_data.game_data import ITEMS, ITEM_SOURCES

def get_item_source_guide(item_key):
    """Get detailed guide on how to obtain a specific item."""
    item_data = ITEMS.get(item_key)
    if not item_data:
        return "Item not found."
    
    sources = item_data.get('sources', [])
    guide_text = f"**{item_data['name']}** ({item_data['rarity'].title()})\n\n"
    
    guide_text += "**How to Obtain:**\n"
    
    for source in sources:
        if source == 'shop':
            price = item_data.get('price', 0)
            if price > 0:
                guide_text += f"🛒 **Shop** - Purchase for {price:,} gold\n"
        
        elif source == 'battle':
            guide_text += f"⚔️ **Combat** - Random drop from monster battles\n"
            guide_text += f"   • Use `$hunt` or `$battle` commands\n"
            guide_text += f"   • Higher level monsters = better drops\n"
        
        elif source == 'boss':
            guide_text += f"🐉 **Boss Fights** - Defeat dungeon bosses\n"
            guide_text += f"   • Complete dungeons to fight bosses\n"
            guide_text += f"   • Guaranteed rare+ drops from bosses\n"
        
        elif source == 'elite':
            guide_text += f"👑 **Elite Monsters** - Rare elite encounters\n"
            guide_text += f"   • 10% chance in battles for elite spawns\n"
            guide_text += f"   • Much better loot than normal monsters\n"
        
        elif source == 'legendary_monster':
            guide_text += f"🌟 **Legendary Creatures** - Extremely rare encounters\n"
            guide_text += f"   • 1% chance in high-level areas\n"
            guide_text += f"   • Guaranteed epic+ rewards\n"
        
        elif source == 'goblin_caves':
            guide_text += f"🕳️ **Goblin Caves Dungeon** (Levels 1-5)\n"
            guide_text += f"   • Use `$dungeons goblin_caves`\n"
            guide_text += f"   • 3 floors, increasing difficulty\n"
        
        elif source == 'shadow_fortress':
            guide_text += f"🏰 **Shadow Fortress Dungeon** (Levels 8-15)\n"
            guide_text += f"   • Use `$dungeons shadow_fortress`\n"
            guide_text += f"   • 5 floors with shadow creatures\n"
        
        elif source == 'dragon_lair':
            guide_text += f"🐉 **Dragon's Lair Dungeon** (Levels 20-30)\n"
            guide_text += f"   • Use `$dungeons dragon_lair`\n"
            guide_text += f"   • 7 floors, dragon-themed enemies\n"
        
        elif source == 'cosmic_void':
            guide_text += f"🌌 **Cosmic Void Dungeon** (Levels 35-50)\n"
            guide_text += f"   • Use `$dungeons cosmic_void`\n"
            guide_text += f"   • 10 floors, void creatures\n"
        
        elif source == 'explore':
            guide_text += f"🗺️ **World Exploration** - Random discovery\n"
            guide_text += f"   • Use `$explore` command (45min cooldown)\n"
            guide_text += f"   • Higher Charisma = better finds\n"
        
        elif source == 'miraculous_box':
            guide_text += f"✨ **Miraculous Box Expeditions**\n"
            guide_text += f"   • Use `$miraculous` command\n"
            guide_text += f"   • Costs 40 Miraculous Energy per entry\n"
            guide_text += f"   • Specialized for artifacts and rare items\n"
        
        elif source == 'crafting':
            guide_text += f"🔨 **Crafting System**\n"
            guide_text += f"   • Use `$craft` command with materials\n"
            guide_text += f"   • Requires recipe knowledge\n"
            guide_text += f"   • Higher level = better crafts\n"
        
        elif source == 'arena':
            guide_text += f"🏆 **PvP Arena Rewards**\n"
            guide_text += f"   • Use `$arena` for ranked battles\n"
            guide_text += f"   • Win battles to earn Gladiator Tokens\n"
            guide_text += f"   • Exchange tokens for rewards\n"
        
        elif source == 'achievement':
            achievement_req = item_data.get('achievement_req')
            if achievement_req:
                guide_text += f"🏆 **Achievement Reward**\n"
                guide_text += f"   • Required: {achievement_req} achievement\n"
                guide_text += f"   • Check `$achievements` for progress\n"
            else:
                guide_text += f"🏆 **Achievement Rewards** - Various achievements\n"
        
        elif source == 'event':
            guide_text += f"🎉 **Special Events** - Limited time only\n"
            guide_text += f"   • Watch for event announcements\n"
            guide_text += f"   • Participate in seasonal events\n"
        
        elif source == 'hidden':
            guide_text += f"🔍 **Hidden Methods** - Secret ways to obtain\n"
            guide_text += f"   • Explore thoroughly and experiment\n"
            guide_text += f"   • Some methods are community secrets\n"
            guide_text += f"   • Complete secret questlines\n"
        
        elif source == 'crafting':
            guide_text += f"🔨 **Crafting System**\n"
            guide_text += f"   • Use `$craft` command with materials\n"
            guide_text += f"   • Requires recipe knowledge\n"
            guide_text += f"   • Higher level = better crafts\n"
        
        elif source == 'achievement':
            guide_text += f"🏆 **Achievement Rewards**\n"
            guide_text += f"   • Complete specific achievements\n"
            guide_text += f"   • Check `$achievements` for progress\n"
            guide_text += f"   • Some require very difficult tasks\n"
        
        elif source == 'owner_only':
            guide_text += f"👑 **Bot Owner Exclusive**\n"
            guide_text += f"   • Only available to bot administrator\n"
        
        elif source == 'admin_spawn':
            guide_text += f"⚙️ **Admin Spawned**\n"
            guide_text += f"   • Server admins can spawn these items\n"
    
    # Add level requirements
    level_req = item_data.get('level_req')
    if level_req:
        guide_text += f"\n**⚠️ Level Requirement:** {level_req}+\n"
    
    # Add achievement requirements
    achievement_req = item_data.get('achievement_req')
    if achievement_req:
        guide_text += f"\n**🏆 Achievement Required:** {achievement_req}\n"
        guide_text += f"   • Use `$achievements` to check progress\n"
    
    # Add rarity information
    guide_text += f"\n**📊 Drop Information:**\n"
    rarity = item_data.get('rarity', 'common')
    rarity_chances = {
        'common': '30-50%',
        'uncommon': '15-25%', 
        'rare': '5-10%',
        'epic': '2-5%',
        'legendary': '0.5-2%',
        'mythical': '0.1-0.5%',
        'divine': '0.05-0.1%',
        'cosmic': '0.01-0.05%'
    }
    
    chance = rarity_chances.get(rarity, 'Unknown')
    guide_text += f"• **Drop Chance:** ~{chance} from appropriate sources\n"
    
    if item_data.get('hidden'):
        guide_text += "\n**🔒 This is a hidden item!** Methods may be secret or require special conditions."
    
    return guide_text

def search_items_by_source(source_type):
    """Get all items available from a specific source."""
    matching_items = {}
    
    for item_key, item_data in ITEMS.items():
        sources = item_data.get('sources', [])
        if source_type in sources:
            matching_items[item_key] = item_data
    
    return matching_items

def get_source_locations():
    """Get all available source types with descriptions."""
    return {
        'shop': 'Items purchasable with gold',
        'battle': 'Random drops from combat',
        'boss': 'Dungeon boss rewards',
        'elite': 'Elite monster drops',
        'legendary_monster': 'Legendary creature rewards',
        'goblin_caves': 'Goblin Caves dungeon (Lv1-5)',
        'shadow_fortress': 'Shadow Fortress dungeon (Lv8-15)',
        'dragon_lair': 'Dragon\'s Lair dungeon (Lv20-30)',
        'cosmic_void': 'Cosmic Void dungeon (Lv35-50)',
        'explore': 'World exploration discoveries',
        'miraculous_box': 'Miraculous Box expeditions',
        'crafting': 'Player crafting system',
        'arena': 'PvP Arena rewards',
        'achievement': 'Achievement milestone rewards',
        'event': 'Special events and seasons',
        'hidden': 'Secret or undiscovered methods'
    }

# Database command for admins
def get_complete_item_database():
    """Generate complete item database for admins."""
    db_text = "# COMPLETE ITEM DATABASE\n\n"
    
    categories = ['weapon', 'armor', 'consumable', 'accessory', 'artifact']
    
    for category in categories:
        db_text += f"\n## {category.upper()}S\n"
        category_items = {k: v for k, v in ITEMS.items() if v.get('type') == category}
        
        for item_key, item_data in sorted(category_items.items()):
            db_text += f"\n### {item_data['name']} ({item_data['rarity']})\n"
            db_text += f"- **Key:** `{item_key}`\n"
            db_text += f"- **Sources:** {', '.join(item_data.get('sources', []))}\n"
            
            if item_data.get('price', 0) > 0:
                db_text += f"- **Price:** {item_data['price']:,} gold\n"
            
            if item_data.get('level_req'):
                db_text += f"- **Level Required:** {item_data['level_req']}\n"
            
            if item_data.get('achievement_req'):
                db_text += f"- **Achievement Required:** {item_data['achievement_req']}\n"
            
            stats = []
            if item_data.get('attack'):
                stats.append(f"ATK: {item_data['attack']}")
            if item_data.get('defense'): 
                stats.append(f"DEF: {item_data['defense']}")
            if item_data.get('hp'):
                stats.append(f"HP: +{item_data['hp']}")
            if item_data.get('mana'):
                stats.append(f"MP: +{item_data['mana']}")
            if item_data.get('critical_chance'):
                stats.append(f"CRIT: {item_data['critical_chance']}%")
            
            if stats:
                db_text += f"- **Stats:** {' | '.join(stats)}\n"
            
            effects = item_data.get('effects', [])
            if effects:
                db_text += f"- **Effects:** {', '.join(effects)}\n"
            
            db_text += f"- **Description:** {item_data.get('description', 'No description')}\n"
    
    return db_text
