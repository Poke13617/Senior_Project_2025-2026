# Senior_Project_2025-2026

This is my senior project I have been working on with my knowledge of this class and where to find them.

What is it?

- This game is intended to be an asymmetrical horror, prioritizing one of three different roles (or classes), these being defense, support, and offense. Support will be the easiest to use, carrying a very good sprint tool and a self-heal. With the executioner's damage, the self-heal both this kit and defense get is greater. Every single ability has a distance you're moved, a set amount of health with a seemingly infinite overheal, and a solid stun time. All survivors carry 2 abilities while executioner carries three.



THE MECHANICS:

TEAMMATES - Small NPC models made to support the player. On death, adds 30s to the timer

EXECUTIONER - Another NPC model made to prioritize getting damage on anyone possible. Later on, the thinking path this one will have is to prioritize the person without abilities so they can't just run off.

PLAYER - the player. they are always on the move, and need to support the teammates for the best chance at survival


THE HUD:


What the hud will look like will be kind of like this (size is variable):

|______________________________________________|
| player kit | timer: time    | Current health:|
|______________________________________________|
| Ability_1_Name       |    cooldown:          |
|______________________________________________|
| Ability_2_Name       |    cooldown:          |
|______________________________________________|
|                                              |
| Teammate kit(1)      | teammate kit(2)       |
|______________________________________________|
| health:  | distance: | health:  | distance:  |
|______________________________________________|


THE MAP:


We want there to be terrain, so we intend to make a space with different terrain levels for the user and teammates to jump around for potential looping.

It'll look something like this (for the record, 1 is base level, 2 is second layer, 3 is top. W is a wall, you will not be able to go through these whatsoeverYou can only go up by one, but down can be any number. It should be a confined space you can also not go through tiles unless you're going above them. spaces between them are for ease of reading. The area outside of this should be restricted and it should show what the terrain looks like on a mini map:)


                            THE MAP
        3 3 3 3 3 3 3 3 3 W W 3 3 3 3 3 3 3 3 3 3 3 3 3
        3 3 3 W 3 3 3 3 3 W W 3 3 W 3 3 3 3 2 1 1 1 2 3
        3 W W W 3 3 3 3 3 3 W 3 3 3 3 W 3 W 2 1 1 1 2 3
        3 3 3 3 3 3 3 3 3 3 W 3 3 3 3 W 3 W 2 1 1 1 2 3
        3 3 3 3 3 W W 2 2 2 W W W 3 3 3 3 3 3 3 3 3 3 3
        3 3 3 3 3 W W 1 1 1 1 1 1 1 1 1 3 3 3 3 3 3 3 3
        3 3 3 3 3 3 3 1 1 1 1 1 1 1 1 1 W W 3 3 3 3 3 3
        3 3 3 3 3 3 3 1 1 1 1 1 1 1 1 1 W W 3 3 3 3 3 3
        3 2 3 2 3 2 3 1 1 1 1 1 1 1 1 1 2 2 3 3 3 3 3 3
        3 3 2 1 2 3 3 1 1 1 1 1 1 1 1 1 2 2 3 3 3 3 3 3
        3 3 1 1 1 3 3 3 3 3 3 3 3 3 3 3 W W 3 3 3 3 3 3
        3 3 1 1 1 3 3 3 3 W W 3 3 3 3 3 W W 3 3 3 3 3 3
        3 3 3 3 3 3 3 3 3 3 3 3 W 3 3 3 3 3 3 3 3 3 3 3
        3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3


                    Example of a Mini Map: | or _ are walls, ^ means jumpable, find a way to make the 3rd floor look different without ruining the simplistic appearance. this also means we need a way to move in one of the four directions, maybe with a W/A/S/D input reader. we only want main directions though, no diagonals. We'll have numbers where these incline increases are for now until we figure out how to remedy it. the same space between each spot is being used too for simplicity
                    we need 6 in the Y-axis and 12 in the X-axis to accomplish a size like this.
                   ____________________________
                   |  3 3 3 3 3 | 3 3 3 3 3 3 |
                   |  | | 2 2 2 | _ _ ^ ^ ^ ^ |
                   |  | |      0            ^ |
                   |  3 ^                   | |
                   |  3 ^                   |_|
                   |  3 ^                   2 |
                   |__________________________|

                   The mini map is taken from this section:

                   3 3 3 3 3 W 3 3 3 3 3 3
                   W W 2 2 2 W W W 3 3 3 3
                   W W 1 1 1 1 1 1 1 1 1 3
                   3 3 1 1 1 1 1 1 1 1 1 W
                   3 3 1 1 1 1 1 1 1 1 1 W
                   3 3 1 1 1 1 1 1 1 1 1 2




                   The mini map should change according to your movement. Teammates should still be moving around the map,this is just so we can see NPC interactions




                   Here's what still needs to be done/fixed:

                   - IMPORTANT - The enemy does not move whatsoever, we also need it coded where he can't attack from the lowest elevation to the highest elevation, or through walls.
                   - Maybe a second map
                   - Maybe some colors to show the map and characters better
                   - IMPORTANT - 2 Bots! 2 Bots that would take the kits you aren't using, would give basic communications, such as "on cooldown, I'll use <This ability> when you get back here. It would also be cool if they could take in certain prompts like asking them to use abilities. It would add the realism (And maybe a little toxicity on the side could be funny too, just basic things like "thanks a lot, <player's class name>, now I'm dead.")
                   - Maybe some cosmetics. They would change the color of the tile
                   - If time permits, a second executioner, thinking similar to tripwire from outcome memories, a trapper.
                   - Smarter NPCs that'll use their kits better. For example, executioner would wait until they're far out of range before using a rushdown ability. Also, losing tracking of the player temporarily when weaved behind a wall. Along with these, something important is so the trapper would be able to place mines that wouldn't move away.
                   - Defense kit rework: will have the same health as before, but instead, now carries a heal, a stun, and a self-destruct. This would allow for it to play more like a defensive tank.
                   - IMPORTANT - LMS: LMS (or Last Man Standing) Is big in the asymmetrical horror genre, and this game shouldn't be an acception. LMS would set the timer to 130 and set your health to 150.
                   - Timer modification, kills on teammates add 25 seconds ecah.