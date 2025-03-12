### run this file please! ###
# this is the main file that runs the game

# import random, math, copy, os
import data, events, combat

# i just don't want to have to write data.player that much, i'm sorry
from data import player

# clear funky terminal directory texts
# os.system('cls' if os.name == 'nt' else 'clear')

events.doShop(player)
combat.doCombat(player, "rat")
combat.doCombat(player, "wolf")
combat.doCombat(player, "wolf")
events.restSite(player)
print("your experience with fighting beasts have taught you something")
print("you learned the spell 'bite'!")
player.spells += ["bite"]
print("")
combat.doCombat(player, "spirit")
combat.doCombat(player, "spirit")
print("your experience with fighting spirits have taught you something")
print("you learned the spell 'cleanse'!")
player.spells += ["cleanse"]
print("")
combat.doCombat(player, "imp")
combat.doCombat(player, "imp")
events.restSite(player)
events.doShop(player)
combat.doCombat(player, "demon")
events.restSite(player)
print("your experience with fighting fiends have taught you something")
print("you learned the spells 'flame' and 'fireball'!")
player.spells += ["flame", "fireball"]
print("")
combat.doCombat(player, "warg")
events.doShop(player)
events.restSite(player)
combat.doCombat(player, "reaper")
print("wowie.")