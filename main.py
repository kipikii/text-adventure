### run this file please! ###
# this is the main file that runs the game

import events, combat, os

# i just don't want to have to write data.player that much, i'm sorry
from data import player

# clear funky terminal directory texts
os.system('cls' if os.name == 'nt' else 'clear')

input("many helpful commands are available at any time by using /help (press enter to continue)\n> ")
events.doShop(player)
combat.doCombat(player, "rat")
combat.doCombat(player, "wolf")
combat.doCombat(player, "wolf")
events.restSite(player)
print("your experience with fighting beasts have taught you something")
print("you learned the spell 'bite'!\n")
player.spells += ["bite"]
events.cubTrapEvent(player)
print("")
events.shrineEvent(player)
print("")
combat.doCombat(player, "spirit")
events.spellTomeEvent(player)
combat.doCombat(player, "spirit")
print("your experience with fighting spirits have taught you something")
print("you learned the spell 'cleanse'!\n")
player.spells += ["cleanse"]
combat.doCombat(player, "imp")
events.trainingManualEvent(player)
combat.doCombat(player, "imp")
events.restSite(player)
events.doShop(player)
combat.doCombat(player, "demon")
events.restSite(player)
print("your experience with fighting fiends have taught you something")
print("you learned the spell 'fireball'!\n")
player.spells += ["fireball"]
print("")
events.shrineEvent(player)
print("")
print("")
combat.doCombat(player, "warg")
events.doShop(player)
events.restSite(player)
combat.doCombat(player, "reaper")
print("wowie.")