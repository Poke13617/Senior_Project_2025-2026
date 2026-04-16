import random

DIFFICULTY_SETTINGS = {
    1: {"name": "Easy", "survival_time": 90},
    2: {"name": "Normal", "survival_time": 120},
    3: {"name": "Hard", "survival_time": 180},
}


class KitSelector:
    """Select a player kit and difficulty by number and return their names and timing settings."""

    KIT_MAP = {
        1: "Offense",
        2: "Support",
        3: "Defense",
    }

    @classmethod
    def select_kit(cls, kit_number: int) -> str:
        """Return the name of the kit for the given selector number."""
        if kit_number not in cls.KIT_MAP:
            raise ValueError("Invalid kit selector. Use 1 for offense, 2 for support, 3 for defense.")
        return cls.KIT_MAP[kit_number]

    @classmethod
    def select_difficulty(cls, difficulty_number: int) -> str:
        """Return the difficulty name for the given selector number."""
        if difficulty_number not in DIFFICULTY_SETTINGS:
            raise ValueError("Invalid difficulty selector. Use 1 for easy, 2 for normal, 3 for hard.")
        return DIFFICULTY_SETTINGS[difficulty_number]["name"]

    @classmethod
    def difficulty_settings(cls, difficulty_number: int) -> dict:
        """Return the difficulty timing settings for the given selector number."""
        if difficulty_number not in DIFFICULTY_SETTINGS:
            raise ValueError("Invalid difficulty selector. Use 1 for easy, 2 for normal, 3 for hard.")
        return DIFFICULTY_SETTINGS[difficulty_number].copy()

    @classmethod
    def select(cls, kit_number: int, difficulty_number: int) -> dict:
        """Return both kit and difficulty selection in one call."""
        settings = cls.difficulty_settings(difficulty_number)
        return {
            "kit": cls.select_kit(kit_number),
            "difficulty": settings["name"],
            "survival_time": settings["survival_time"],
        }


def offense_kit() -> dict:
    """Return the offense kit abilities and their cooldowns."""
    return {
        "kit": KitSelector.select_kit(1),
        "health": 90,
        "abilities": {
            "Lunge": {
                "cooldown": 8,
                "description": "Lunge forward with a powerful strike that stuns the enemy for 2 turns.",
                "distance": 2,
                "stun_time": 3,
                "distance_change": 1,
            },
            "Sprint": {
                "cooldown": 12,
                "description": "Sprint away to create distance and reposition.",
                "distance_change": 3,
            },
            "Jump": {
                "cooldown": 4,
                "description": "Jump to gain 1-turn invincibility.",
                "invincibility": 1,
            },
        },
    }


def support_kit() -> dict:
    """Return the support kit abilities and their cooldowns."""
    return {
        "kit": KitSelector.select_kit(2),
        "health": 100,
        "abilities": {
            "Quick Heal": {
                "cooldown": 4,
                "description": "Quick self-heal that can overheal by 20 without affecting movement.",
                "heal": 25,
                "overheal": 20,
                "distance_change": 0,
            },
            "Dash Forward": {
                "cooldown": 6,
                "description": "Dash forward to push back out of range.",
                "distance_change": 2.75,
            },
            "Jump": {
                "cooldown": 4,
                "description": "Jump to gain 1-turn invincibility.",
                "invincibility": 1,
            },
        },
    }


def defense_kit() -> dict:
    """Return the defense kit abilities and their cooldowns."""
    return {
        "kit": KitSelector.select_kit(3),
        "health": 165,
        "abilities": {
            "Fortify Guard": {
                "cooldown": 3,
                "description": "Raise defenses and resist the next attack.",
                "distance": 0,
                "stun_time": 0,
            },
            "Ground Slam": {
                "cooldown": 5,
                "description": "Stunning strike that slows nearby enemies.",
                "distance": 1,
                "stun_time": 3,
                "distance_change": 0.5,  # move away
            },
            "Jump": {
                "cooldown": 4,
                "description": "Jump to gain 1-turn invincibility.",
                "invincibility": 1,
            },
        },
    }


def enemy_kit() -> dict:
    """Return the enemy executioner-style kit with its abilities."""
    return {
        "kit": "Executioner",
        "stun_timer": 0,
        "abilities": {
            "Slash": {
                "cooldown": 5,
                "description": "Quick slash that deals damage and can interrupt enemy actions.",
                "damage": 20,
                "range": 1,
            },
            "Invisibility": {
                "cooldown": 7,
                "description": "Vanish briefly and instantly close distance, damaging the target, but hinders yourself for one turn.",
                "damage": 30,
                "range": 4.5,
            },
            "Charge": {
                "cooldown": 8,
                "description": "Charge forward to pin the enemy in place and deal damage based on a portion of the target's current health.",
                "base_damage": 10,
                "percent_health": 0.25,
                "range": 5,
                "distance_change": -3,
            },
        },
    }



def advance_tick(counter: int, stun_time: int = 0) -> tuple[int, int]:
    """Advance the game timer and decrease remaining stun duration."""
    return counter + 1, max(0, stun_time - 1)


def get_player_kit(kit_number: int) -> dict:
    """Return the selected player kit data."""
    if kit_number == 1:
        return offense_kit()
    if kit_number == 2:
        return support_kit()
    if kit_number == 3:
        return defense_kit()
    raise ValueError("Invalid kit selector. Use 1 for offense, 2 for support, 3 for defense.")


def choose_int(prompt: str, valid_options: list[int]) -> int:
    """Prompt the user until a valid integer choice is entered."""
    while True:
        choice = input(prompt).strip()
        if choice.isdigit() and int(choice) in valid_options:
            return int(choice)
        print(f"Please enter one of {valid_options}.")


def choose_player_ability(player_kit: dict, cooldowns: dict[str, int]) -> tuple[str, dict]:
    """Prompt the player to choose an available ability."""
    abilities = list(player_kit["abilities"].items())
    print("\nAvailable abilities:")
    for index, (name, info) in enumerate(abilities, start=1):
        remaining = int(max(0, cooldowns.get(name, 0)))
        print(f"  {index}. {name} ({info['description']}) - cooldown {remaining}")
    print(f"  {len(abilities) + 1}. Skip turn (do nothing this turn)")

    while True:
        selection = input("Select ability number: ").strip()
        if not selection.isdigit():
            print("Enter a number for your ability choice.")
            continue
        index = int(selection) - 1
        if index == len(abilities):
            return "Skip", {}
        if index < 0 or index >= len(abilities):
            print("Choice out of range.")
            continue
        name, info = abilities[index]
        if cooldowns.get(name, 0) > 0:
            print(f"{name} is still on cooldown.")
            continue
        return name, info


def select_enemy_attack(enemy: dict, enemy_cooldowns: dict[str, int]) -> tuple[str | None, dict | None]:
    """Pick a random enemy attack that is off cooldown.

    If no abilities are ready, the Executioner must recover this turn instead of attacking.
    """
    available = [name for name in enemy["abilities"] if enemy_cooldowns.get(name, 0) == 0]
    if not available:
        return None, None
    ability_name = random.choice(available)
    ability_data = enemy["abilities"][ability_name]
    return ability_name, ability_data


def apply_player_ability(
    ability_name: str,
    ability_data: dict,
    player_health: int,
    shield: int,
    player_distance: float,
    player_invincible: bool,
    player_max_health: int,
) -> tuple[int, int, float, int, bool]:
    """Apply the selected player ability and return updated health, shield, distance, enemy stun, and invincibility."""
    if ability_name == "Skip":
        print("You skip your turn.")
        return player_health, shield, player_distance, 0, player_invincible
    enemy_stun = ability_data.get("stun_time", 0)
    distance_change = ability_data.get("distance_change", 0)
    if ability_name == "Quick Heal":
        heal_amount = ability_data["heal"]
        overheal_amount = ability_data.get("overheal", 0)
        if player_health >= player_max_health:
            shield += overheal_amount
            print(f"You are already at full health and gain {overheal_amount} overheal.")
        else:
            healed = min(player_max_health - player_health, heal_amount)
            player_health += healed
            print(f"You heal yourself for {healed} health.")
    elif ability_name == "Dash Forward":
        print(f"You dash forward, increasing distance.")
    elif ability_name == "Protective Barrier":
        shield += 10
        print("You raise a protective barrier for 10 incoming damage.")
    elif ability_name == "Fortify Guard":
        shield += 25
        print("You brace yourself and reduce the next incoming damage.")
    elif ability_name == "Sprint":
        print("You sprint away to create distance.")
    elif ability_name == "Jump":
        print("You jump and become invincible for 1 turn.")
        player_invincible = True
    else:
        print(f"You use {ability_name} and move {ability_data['distance']} units.")
        if enemy_stun:
            print("The enemy is staggered by your attack.")
    player_distance += distance_change
    player_distance = max(0, player_distance)  # can't go negative
    if distance_change != 0:
        print(f"Distance changed by {distance_change}. Current distance: {player_distance:.2f}")
    return player_health, shield, player_distance, enemy_stun, player_invincible


def apply_enemy_attack(
    enemy_name: str,
    enemy_data: dict,
    player_health: int,
    shield: int,
    player_distance: float,
    player_invincible: bool,
) -> tuple[int, int, float, int]:
    """Apply the enemy attack against the player and return updated health, shield, distance, and enemy self-stun."""
    enemy_self_stun = 0
    if player_distance > enemy_data.get("range", 0):
        print(f"Executioner uses {enemy_name} but you are out of range (distance: {player_distance:.2f}).")
        return player_health, shield, player_distance, enemy_self_stun
    if player_invincible:
        print(f"Executioner uses {enemy_name} but you are invincible and take no damage.")
        return player_health, shield, player_distance, enemy_self_stun
    if enemy_name == "Charge":
        damage = enemy_data["base_damage"] + int(player_health * enemy_data["percent_health"])
    else:
        damage = enemy_data["damage"]

    mitigated = min(shield, damage)
    damage -= mitigated
    shield -= mitigated
    player_health -= damage
    print(f"Executioner uses {enemy_name} and deals {damage} damage.")
    if mitigated:
        print(f"Your shield absorbs {mitigated} damage.")

    if enemy_name == "Invisibility":
        enemy_self_stun = 1  # hinders the Executioner for 1 turn
        print("The Executioner is hindered by their own invisibility and loses a turn.")
        player_distance = 0  # sends them right to you
        print("The Executioner closes the distance instantly!")

    distance_change = enemy_data.get("distance_change", 0)
    player_distance += distance_change
    player_distance = max(0, player_distance)
    if distance_change != 0:
        print(f"Distance changed by {distance_change}. Current distance: {player_distance:.2f}")

    return player_health, shield, player_distance, enemy_self_stun


def play_survival_game() -> None:
    """Run the main survival game loop."""
    print("Welcome to Survivor vs Executioner!")
    print("Choose your survivor kit:")
    print("  1. Offense\n  2. Support\n  3. Defense")
    kit_choice = choose_int("Kit number: ", [1, 2, 3])
    difficulty_choice = choose_int("Difficulty (1=Easy, 2=Normal, 3=Hard): ", [1, 2, 3])

    settings = KitSelector.select(kit_choice, difficulty_choice)
    player_kit = get_player_kit(kit_choice)
    enemy = enemy_kit()

    player_health = player_kit["health"]
    player_max_health = player_kit["health"]
    shield = 0
    player_stun = 0
    enemy_stun = 0
    counter = 0
    player_distance = 5.0  # starting distance
    player_invincible = False
    player_cooldowns = {name: 0 for name in player_kit["abilities"]}
    enemy_cooldowns = {name: 0 for name in enemy["abilities"]}

    print(f"\nStarting as {player_kit['kit']} on {settings['difficulty']} difficulty.")
    print(f"Survive for {settings['survival_time']} turns.\n")

    while counter < settings["survival_time"] and player_health > 0:
        turns_left = settings["survival_time"] - counter
        print(f"Turn {counter + 1} - Time left: {turns_left} | Health: {player_health} | Shield: {shield} | Distance: {player_distance}")

        if enemy_stun > 0:
            print("The Executioner is stunned and cannot act this turn.")
            enemy_stun -= 1
        else:
            enemy_name, enemy_data = select_enemy_attack(enemy, enemy_cooldowns)
            if enemy_name is None:
                print("The Executioner has no abilities ready and is forced to recover this turn.")
            else:
                player_health, shield, player_distance, enemy_self_stun = apply_enemy_attack(
                    enemy_name, enemy_data, player_health, shield, player_distance, player_invincible
                )
                enemy_stun += enemy_self_stun
                enemy_cooldowns[enemy_name] = enemy_data["cooldown"]
                player_invincible = False  # invincibility lasts for this enemy attack
            # Executioner still closes in while recharging.
            if player_distance > 1:
                player_distance = max(0, player_distance - 0.15)
                print(f"The Executioner advances closer. Distance: {player_distance:.2f}")

        if player_stun > 0:
            print("You are stunned and lose this turn.")
        else:
            ability_name, ability_data = choose_player_ability(player_kit, player_cooldowns)
            player_health, shield, player_distance, enemy_stun, player_invincible = apply_player_ability(
                ability_name,
                ability_data,
                player_health,
                shield,
                player_distance,
                player_invincible,
                player_max_health,
            )
            if ability_name != "Skip":
                player_cooldowns[ability_name] = ability_data["cooldown"]

        player_cooldowns = {
            name: max(0, cooldown - 1)
            for name, cooldown in player_cooldowns.items()
        }
        enemy_cooldowns = {
            name: max(0, cooldown - 1)
            for name, cooldown in enemy_cooldowns.items()
        }
        counter, player_stun = advance_tick(counter, player_stun)
        print()

    if player_health <= 0:
        print("You were defeated by the Executioner.")
    else:
        print("You survived the timer and escaped! Congratulations.")


if __name__ == "__main__":
    play_survival_game()
