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
    iron_ore{{Iron Ore}}
    iron_ingot{{Iron Ingot}}
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
    mine--Stone Pickaxes-->iron_ore
    
    %% Charcoal Smelter
    wood-.Convert Logs.->charcoalSmelter
    charcoalSmelter--Convert Logs-->charcoal
    
    %% Ore Smelter
    charcoal-.Basic Smelting.->oreSmelter
    iron_ore-.Basic Smelting.->oreSmelter
    oreSmelter--Basic Smelting-->iron_ingot
    
    %% Building site
    iron_ingot-."Iron Reinforcing (Modifier)".->building
```
