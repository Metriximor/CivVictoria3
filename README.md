# CivVictoria3
Victoria 3 Total Conversion Mod into CivMC

## Planned Buildings Roadmap

# Dirt tier
All buildings are built by the **Construction Site**
```mermaid
flowchart
    treeFarm(Tree Farm)
    building(Construction Site)
    
    wood{{Oak Log}}
    
    wood-.Wood based builds.->building
    
    treeFarm--Punch Wood-->wood
```
# Wood tier
```mermaid
flowchart
    treeFarm(Tree Farm)
    toolFactory(Tool Factory)
    mine(Mine)
    building(Construction Site)
    
    wood{{Oak Log}}
    woodTools{{Wood Tools}}
    stone{{Stone}}
    
    woodTools-.Wood Axes.->treeFarm
    woodTools-.Wood Pickaxes.->mine
    
    wood-.Make Wooden Tools.->toolFactory
    wood-.Wood based builds.->building
    
    stone-."Stone reinforcing (Modifier)".->building
    
    treeFarm--Wood Axes-->wood
        
    toolFactory--Make Wooden Tools-->woodTools    
    
    mine--Wood Pickaxes-->stone
```
# Stone tier
```mermaid
flowchart
    %% Buildings
    treeFarm(Tree Farm)
    toolFactory(Tool Factory)
    charcoalSmelter(Charcoal Smelter)
    oreSmelter(Ore Smelter)
    mine(Mine)
    building(Construction Site)
        
    %% Resources
    wood{{Oak Log}}
    stone{{Stone}}
    charcoal{{Charcoal}}
    ironOre{{Iron Ore}}
    ironIngot{{Iron Ingot}}
    stoneTools{{Stone Tools}}
    
    %% Tree farm
    stoneTools-.Stone Axes.->treeFarm
    treeFarm--Stone Axes-->wood
    
    %% Tool factory
    wood-.Make Stone Tools.->toolFactory
    stone-.Make Stone Tools.->toolFactory
    toolFactory--Make Stone Tools-->stoneTools
    
    %% Mine
    stoneTools-.Stone Pickaxes.->mine
    mine--Stone Pickaxes-->stone
    mine--Stone Pickaxes-->ironOre
    
    %% Charcoal Smelter
    wood-.Convert Logs.->charcoalSmelter
    charcoalSmelter--Convert Logs-->charcoal
    
    %% Ore Smelter
    charcoal-.Basic Smelting.->oreSmelter
    ironOre-.Basic Smelting.->oreSmelter
    oreSmelter--Basic Smelting-->ironIngot
    
    %% Building site
    ironIngot-."Iron Reinforcing (Modifier)".->building
```
# Iron Tier
```mermaid
flowchart
    %% Buildings
    treeFarm(Tree Farm)
    toolFactory(Tool Factory)
    charcoalSmelter(Charcoal Smelter)
    oreSmelter(Ore Smelter)
    mine(Mine)
    building(Construction Site)
    rails(Rails)
    sandPit(Sand Pit)
    glassSmelter(Glass Smelter)
        
    %% Resources
    wood{{Oak Log}}
    stone{{Stone}}
    charcoal{{Charcoal}}
    ironOre{{Iron Ore}}
    ironIngot{{Iron Ingot}}
    ironTools{{Iron Tools}}
    redstone{{Redstone}}
    diamonds{{Diamonds}}
    goldOre{{Gold Ore}}
    goldIngot{{Gold Ingot}}
    goldTools{{Enchanted Gold Tools}}
    sand{{Sand}}
    glass{{Glass}}
    glassBottle{{Glass Bottle}}
    
    %% Tree farm
    ironTools-.Iron Axes.->treeFarm
    treeFarm--Iron Axes-->wood
    
    %% Tool factory
    charcoal-.Make Iron Tools.->toolFactory
    ironIngot-.Make Iron Tools.->toolFactory
    toolFactory--Make Iron Tools-->ironTools
    
    charcoal-.Make Iron Tools.->toolFactory
    goldIngot-.Make enchanted Gold Tools.->toolFactory
    toolFactory--Make enchanted Gold Tools-->goldTools
    
    %% Mine
    ironTools-.Iron Pickaxes.->mine
    goldTools-.Enchanted Gold Pickaxes.->mine
    mine--Iron/Gold Pickaxes-->stone
    mine--Iron/Gold Pickaxes-->ironOre
    mine--Iron/Gold Pickaxes-->redstone
    mine--Iron/Gold Pickaxes-->goldOre
    mine--Iron/Gold Pickaxes-->diamonds
    
    %% Charcoal Smelter
    wood-.Convert Logs.->charcoalSmelter
    charcoalSmelter--Convert Logs-->charcoal
    
    %% Sand Pit
    ironTools-.Iron Shovels.->sandPit 
    sandPit--Dig Sand-->sand
    
    %% Glass Smelter
    sand-.Refine Sand.->glassSmelter
    charcoal-.Refine Sand.->glassSmelter
    glassSmelter--Refine Sand-->glass
    
    glass-.Make Bottles.->glassSmelter
    charcoal-.Make Bottles.->glassSmelter
    glassSmelter--Make Bottles-->glassBottle
    
    %% Ore Smelter
    charcoal-.Basic Smelting.->oreSmelter
    ironOre-.Basic Smelting.->oreSmelter
    oreSmelter--Basic Smelting-->ironIngot
    
    charcoal-.Gold Smelting.->oreSmelter
    goldOre-.Gold Smelting.->oreSmelter
    oreSmelter--Gold Smelting-->goldIngot
    
    %% Building site
    diamonds-."Diamond Reinforcing (Modifier)".->building
    
    %% Rails
    goldIngot-.Powered Rails.->rails
    redstone-.Powered Rails.->rails
    ironIngot-.Powered Rails.->rails
```
