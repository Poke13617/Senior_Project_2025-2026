import random

DIFFICULTY_SETTINGS = {
    1: {"name": "Easy", "survival_time": 90},
    2: {"name": "Normal", "survival_time": 120},
    3: {"name": "Hard", "survival_time": 180},
}


# Terrain map (height levels: 1=ground, 2=mid, 3=top, W=wall)
TERRAIN_MAP = [
    [3,3,3,3,3,3,3,3,3,'W','W',3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,'W',3,3,3,3,3,'W','W',3,3,'W',3,3,3,3,2,1,1,1,2,3],
    [3,'W','W','W',3,3,3,3,3,3,'W',3,3,3,3,'W',3,'W',2,1,1,1,2,3],
    [3,3,3,3,3,3,3,3,3,3,'W',3,3,3,3,'W',3,'W',2,1,1,1,2,3],
    [3,3,3,3,3,'W','W',2,2,2,'W','W','W',3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,'W','W',1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,'W','W',3,3,3,3,3,3],
    [3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,'W','W',3,3,3,3,3,3],
    [3,2,3,2,3,2,3,1,1,1,1,1,1,1,1,1,2,2,3,3,3,3,3,3],
    [3,3,2,1,2,3,3,1,1,1,1,1,1,1,1,1,2,2,3,3,3,3,3,3],
    [3,3,1,1,1,3,3,3,3,3,3,3,3,3,3,3,'W','W',3,3,3,3,3,3],
    [3,3,1,1,1,3,3,3,3,'W','W',3,3,3,3,3,'W','W',3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,'W',3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
]

MAP_HEIGHT = len(TERRAIN_MAP)
MAP_WIDTH = len(TERRAIN_MAP[0]) if TERRAIN_MAP else 0

def get_terrain_height(x: int, y: int) -> int:
    """Get the height level at position (x, y). Returns 0 for walls or out of bounds."""
    if 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
        cell = TERRAIN_MAP[y][x]
        return cell if isinstance(cell, int) else 0
    return 0

def is_valid_position(x: int, y: int, current_height: int) -> bool:
    """Check if a position is valid to move to from current height."""
    if not (0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH):
        return False
    cell = TERRAIN_MAP[y][x]
    if cell == 'W':
        return False
    # Can move up by at most 1 level, down by any amount
    return cell <= current_height + 1


def display_mini_map(player_pos: list[int], enemy_pos: list[int]) -> None:
    """Display a 6x12 mini-map centered around the player position."""
    center_x, center_y = player_pos
    
    # Mini-map dimensions: 6 rows, 12 columns
    mini_height = 6
    mini_width = 12
    
    # Calculate the top-left corner of the mini-map view
    start_x = max(0, center_x - mini_width // 2)
    start_y = max(0, center_y - mini_height // 2)
    
    print("Mini-Map:")
    print("____________________________")
    
    for dy in range(mini_height):
        row_str = "| "
        map_y = start_y + dy
        
        if map_y >= MAP_HEIGHT:
            # Out of bounds - show empty
            row_str += " " * (mini_width * 2 - 1)
        else:
            for dx in range(mini_width):
                map_x = start_x + dx
                
                if map_x >= MAP_WIDTH:
                    row_str += " "
                else:
                    cell = TERRAIN_MAP[map_y][map_x]
                    
                    # Check if any entity is at this position
                    entity_here = None
                    if [map_x, map_y] == player_pos:
                        entity_here = "P"
                    elif [map_x, map_y] == enemy_pos:
                        entity_here = "E"
                    
                    if entity_here:
                        row_str += entity_here
                    elif cell == 'W':
                        # Wall - use special characters based on position
                        if dx == 0 or dx == mini_width - 1:
                            row_str += "|"  # Vertical wall
                        else:
                            row_str += "_"  # Horizontal wall
                    elif isinstance(cell, int):
                        # Height level
                        if cell == 3:
                            row_str += "3"
                        elif cell == 2:
                            row_str += "2" 
                        elif cell == 1:
                            row_str += "1"
                        else:
                            row_str += "0"
                    else:
                        row_str += " "
                
                # Add space between cells
                if dx < mini_width - 1:
                    row_str += " "
        
        row_str += " |"
        print(row_str)
    
    print("|__________________________|")


def display_hud(player_kit: dict, player_health: int, player_pos: list[int], 
                player_cooldowns: dict[str, int], counter: int, survival_time: int) -> None:
    """Display a compact game HUD."""
    print("┌─────────────────────────────────────┐")
    print(f"│ {player_kit['kit']:<8} │ Time: {survival_time - counter:<3} │ HP: {player_health:<3} │ Pos: ({player_pos[0]},{player_pos[1]}) │")
    print("├─────────────────────────────────────┤")
    
    # Show player abilities
    abilities = list(player_kit["abilities"].keys())
    for ability in abilities:
        cooldown = player_cooldowns.get(ability, 0)
        print(f"│ {ability:<15} │ CD: {cooldown:<2} │")
    
    print("└─────────────────────────────────────┘")


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


def choose_int(prompt: str, valid_options: list[int]) -> int:
    """Error management - Invalid input"""
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
    player_pos: list[int],
    player_invincible: bool,
    player_max_health: int,
) -> tuple[int, int, list[int], int, bool]:
    """Apply the selected player ability and return updated health, shield, position, enemy stun, and invincibility."""
    if ability_name == "Skip":
        print("You skip your turn.")
        return player_health, shield, player_pos, 0, player_invincible
    
    enemy_stun = ability_data.get("stun_time", 0)
    
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
        # Move forward (positive X direction)
        new_pos = [player_pos[0] + 2, player_pos[1]]
        current_height = get_terrain_height(player_pos[0], player_pos[1])
        if is_valid_position(new_pos[0], new_pos[1], current_height):
            player_pos = new_pos
            print(f"You dash forward to position ({player_pos[0]}, {player_pos[1]}).")
        else:
            print("Dash blocked by terrain.")
    elif ability_name == "Protective Barrier":
        shield += 10
        print("You raise a protective barrier for 10 incoming damage.")
    elif ability_name == "Fortify Guard":
        shield += 25
        print("You brace yourself and reduce the next incoming damage.")
    elif ability_name == "Sprint":
        # Move backward (negative X direction)
        new_pos = [player_pos[0] - 3, player_pos[1]]
        current_height = get_terrain_height(player_pos[0], player_pos[1])
        if is_valid_position(new_pos[0], new_pos[1], current_height):
            player_pos = new_pos
            print(f"You sprint backward to position ({player_pos[0]}, {player_pos[1]}).")
        else:
            print("Sprint blocked by terrain.")
    elif ability_name == "Jump":
        print("You jump and become invincible for 1 turn.")
        player_invincible = True
    elif ability_name == "Lunge":
        # Move forward and attack
        new_pos = [player_pos[0] + 2, player_pos[1]]
        current_height = get_terrain_height(player_pos[0], player_pos[1])
        if is_valid_position(new_pos[0], new_pos[1], current_height):
            player_pos = new_pos
            print(f"You lunge forward to position ({player_pos[0]}, {player_pos[1]}) and stun the enemy.")
        else:
            print("Lunge blocked by terrain.")
    else:
        print(f"You use {ability_name}.")
        if enemy_stun:
            print("The enemy is staggered by your attack.")
    
    return player_health, shield, player_pos, enemy_stun, player_invincible


def apply_enemy_attack(
    enemy_name: str,
    enemy_data: dict,
    player_health: int,
    shield: int,
    distance: float,
    player_invincible: bool,
) -> tuple[int, int, list[int], int]:
    """Apply the enemy attack against the player and return updated health, shield, position, and enemy self-stun."""
    enemy_self_stun = 0
    if distance > enemy_data.get("range", 0):
        print(f"Executioner uses {enemy_name} but you are out of range (distance: {distance:.2f}).")
        return player_health, shield, [], enemy_self_stun  # Return empty list for position since no change
    if player_invincible:
        print(f"Executioner uses {enemy_name} but you are invincible and take no damage.")
        return player_health, shield, [], enemy_self_stun
    
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

    # For now, no position changes from enemy attacks
    # Invisibility could teleport enemy closer in future
    return player_health, shield, [], enemy_self_stun


def play_survival_game() -> None:
    # The game
    print("Welcome to Survivor vs Executioner!")
    print("Choose your survivor kit:")
    print("  1. Offense\n  2. Support\n  3. Defense")
    kit_choice = choose_int("Kit number: ", [1, 2, 3])
    difficulty_choice = choose_int("Difficulty (1=Easy, 2=Normal, 3=Hard): ", [1, 2, 3])

    settings = KitSelector.select(kit_choice, difficulty_choice)
    player_kit = get_player_kit(kit_choice)
    enemy = enemy_kit()

    # Initialize positions (x, y) - starting in the center area
    player_pos = [10, 8]  # Starting position
    enemy_pos = [2, 8]    # Enemy starts on the left side
    
    player_health = player_kit["health"]
    player_max_health = player_kit["health"]
    shield = 0
    player_stun = 0
    enemy_stun = 0
    counter = 0
    player_invincible = False
    player_cooldowns = {name: 0 for name in player_kit["abilities"]}
    enemy_cooldowns = {name: 0 for name in enemy["abilities"]}

    print(f"\nStarting as {player_kit['kit']} on {settings['difficulty']} difficulty.")
    print(f"Survive for {settings['survival_time']} turns.\n")

    while counter < settings["survival_time"] and player_health > 0:
        # Display HUD and mini-map
        display_hud(player_kit, player_health, player_pos, 
                   player_cooldowns, counter, settings["survival_time"])
        display_mini_map(player_pos, enemy_pos)

        print(f"\n=== TURN {counter + 1} ===")

        if enemy_stun > 0:
            print("=== ENEMY PHASE ===")
            print("The Executioner is stunned and cannot act this turn.")
            enemy_stun -= 1
        else:
            print("=== ENEMY PHASE ===")
            # Enemy AI movement and attack logic would go here
            # For now, enemy stays in place
            enemy_name, enemy_data = select_enemy_attack(enemy, enemy_cooldowns)
            if enemy_name is None:
                print("The Executioner has no abilities ready and is forced to recover this turn.")
            else:
                # Calculate distance for attack range
                distance = abs(player_pos[0] - enemy_pos[0]) + abs(player_pos[1] - enemy_pos[1])
                if distance <= enemy_data.get("range", 1):
                    player_health, shield, _, enemy_self_stun = apply_enemy_attack(
                        enemy_name, enemy_data, player_health, shield, distance, player_invincible
                    )
                    enemy_stun += enemy_self_stun
                    enemy_cooldowns[enemy_name] = enemy_data["cooldown"]
                else:
                    print(f"Executioner uses {enemy_name} but you are out of range (distance: {distance}).")
                player_invincible = False

        # Player turn: movement and ability
        if player_stun > 0:
            print("You are stunned and lose this turn.")
            player_stun -= 1
        else:
            # Player movement
            print("\n=== MOVEMENT PHASE ===")
            print("Use W/A/S/D keys to move, or press Enter to skip movement:")
            print("  W = North (up)")
            print("  A = West (left)") 
            print("  S = South (down)")
            print("  D = East (right)")
            
            move_input = input("Your move (W/A/S/D or Enter): ").strip().upper()
            
            new_pos = player_pos.copy()
            if move_input == 'W':
                new_pos[1] -= 1
                direction = "north"
            elif move_input == 'S':
                new_pos[1] += 1
                direction = "south"
            elif move_input == 'A':
                new_pos[0] -= 1
                direction = "west"
            elif move_input == 'D':
                new_pos[0] += 1
                direction = "east"
            else:
                direction = None
            
            # Check if movement is valid
            if direction:
                current_height = get_terrain_height(player_pos[0], player_pos[1])
                if is_valid_position(new_pos[0], new_pos[1], current_height):
                    player_pos = new_pos
                    print(f"You move {direction} to position ({player_pos[0]}, {player_pos[1]})")
                else:
                    print(f"Cannot move {direction} - blocked by wall or terrain height difference!")
            else:
                print("You stay in place.")
            
            # Player ability selection
            print("\n=== ABILITY PHASE ===")
            ability_name, ability_data = choose_player_ability(player_kit, player_cooldowns)
            if ability_name != "Skip":
                player_health, shield, player_pos, enemy_stun, player_invincible = apply_player_ability(
                    ability_name, ability_data, player_health, shield, player_pos, player_invincible, player_max_health
                )
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
