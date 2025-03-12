### man, my old code is very SPAGHETTI and INEFFICIENT ###
### let's streamline this hunk of junk ###

# import random, math, copy, os
import data, events, combat

# # clear funky terminal directory text
# os.system('cls' if os.name == 'nt' else 'clear')

events.doShop(data.player)
combat.doCombat(data.player, "rat")
combat.doCombat(data.player, "wolf")
combat.doCombat(data.player, "wolf")
events.restSite(data.player)
print("your experience with fighting beasts have taught you something")
print("you learned the spell 'bite'!")
data.player.spells += ["bite"]
print("")
combat.doCombat(data.player, "spirit")
combat.doCombat(data.player, "spirit")
print("your experience with fighting spirits have taught you something")
print("you learned the spell 'cleanse'!")
data.player.spells += ["cleanse"]
print("")
combat.doCombat(data.player, "imp")
combat.doCombat(data.player, "imp")
events.restSite(data.player)
events.doShop(data.player)
combat.doCombat(data.player, "demon")
events.restSite(data.player)
print("your experience with fighting fiends have taught you something")
print("you learned the spells 'flame' and 'fireball'!")
data.player.spells += ["flame", "fireball"]
print("")
combat.doCombat(data.player, "warg")
events.doShop(data.player)
events.restSite(data.player)
combat.doCombat(data.player, "reaper")
print("wowie.")