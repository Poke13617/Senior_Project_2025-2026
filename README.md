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

There are maps that the game selects from at random. These are to give you a visualizer of the terrain you will be moving around, and there is a full movement system to move from tile to tile, adding the extra depth to the game.

HOW IT'S MADE:

The character select is made with dictionaries, which takes in your kit's abilities, the teammates kits (these are the other kits you didn't choose), and the executioner's kit. These are for easy access.

Movement:
The movement is made by moving markers around different parts of the lists so it looks like the player is moving.

Map:
The map is made with lists so it's easy to access all of the terrain at once when displaying the map.

Teammates/Executioner:
These are using a pathfinding formula for different purposes. Teammates have a pathfinding formula where they run if they're in chase while Executioner follows whoever is closest (except for if a teammate is the same distance. Because the teammate isn't a player, it's focused earlier to add more strategy to how you work around the teammates.). These add the depth of other players taking these roles without other players taking these roles for simplicity.

Abilities:
ALL ABILITIES DO NOT CARRY DAMAGE. Instead, they use a stun stat. This stun stat stops the enemy in place and restricts the use of abilities. Only the executioner gets true damage (because what good is an executioner if they're being treated as the victim). And only two of these three kits carry a heal (be it self-heal, but a heal nonetheless.) These are on kits with less abilities to work around the executioner.

Feature - Jumping:
Every few turns you have a jump off cooldown. The purpose of this jump is to go invincible for a turn and to get more time while the other abilities are on cooldown, jumping over the enemy. This is so being in chase doesn't ruin the player every time without much you can do if everything is on cooldown.

Cooldowns:
All abilities, and I mean ALL abilities carry cooldowns. A game where cooldowns don't exist wouldn't work very well with how survivors can gain distance through abilities. Cooldowns are in place so you have to wait before using an ability again. The times change based on what kit is being watched. The kits all work the same without being dependent on the player's choice, so they will always have the same cooldowns.

Turns:
Every "second" is a turn, where you make a decision on where you're moving (if you want to, of course. you can choose not to move.) and what you plan to do for an ability (again, if you want to. Cooldowns exist, so there's a way to choose to do nothing). The turn ends when the executioner makes its decision.

Last Man Standing/LMS:
If somehow both of the teammates go down in chase, you are thrown into Last Man Standing (Or LMS for short). LMS is notorious in the asymmetrical horror scene, where the player is pitted one-on-one with the executioner. The timer is set to 140 turns for survival and your health is adjusted to 165. This allows for more time to survive. These perks do NOT apply to solo difficulty, where teammates aren't present.

HOW TO WIN:

To win, you survive the timer until it hits zero. When it does, you win (There isn't much else to say. Just survive the timer.)

Thank you for reading the readme and have a great day!