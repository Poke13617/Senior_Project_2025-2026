import random
from collections import deque

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
    return cell <= current_height + 1


def display_mini_map(player_pos: list[int], enemy_pos: list[int], teammates: list[dict]) -> None:
    """Display a 6x12 mini-map centered around the player position."""
    def colorize(char: str, kit: str | None = None) -> str:
        terrain_colors = {
            '1': '\033[38;5;130m',  # darker brown ground
            '2': '\033[38;5;136m',  # medium brown mid elevation
            '3': '\033[38;5;180m',  # lighter high ground
            'W': '\033[90m',        # walls
            '|': '\033[90m',
            '_': '\033[90m',
        }
        kit_colors = {
            'Offense': '\033[94m',       # blue
            'Support': '\033[38;5;229m', # cream
            'Defense': '\033[91m',       # red
        }
        marker_colors = {
            'P': '\033[92m',  # bright green player
            'E': '\033[34m',  # navy/dark blue executioner
        }
        color = marker_colors.get(char)
        if not color and kit:
            color = kit_colors.get(kit)
        if not color:
            color = terrain_colors.get(char, '')
        reset = '\033[0m'
        return f"{color}{char}{reset}" if color else char

    center_x, center_y = player_pos
    mini_height = 6
    mini_width = 12
    start_x = max(0, center_x - mini_width // 2)
    start_y = max(0, center_y - mini_height // 2)

    print("Mini-Map:")
    print("____________________________")

    for dy in range(mini_height):
        row_str = "| "
        map_y = start_y + dy

        if map_y >= MAP_HEIGHT:
            row_str += " " * (mini_width * 2 - 1)
        else:
            for dx in range(mini_width):
                map_x = start_x + dx
                if map_x >= MAP_WIDTH:
                    row_str += " "
                else:
                    cell = TERRAIN_MAP[map_y][map_x]
                    entity_here = None
                    if [map_x, map_y] == player_pos:
                        entity_here = "P"
                    elif [map_x, map_y] == enemy_pos:
                        entity_here = "E"
                    else:
                        teammate_kit = None
                        for index, teammate in enumerate(teammates):
                            if teammate["alive"] and teammate["pos"] == [map_x, map_y]:
                                entity_here = chr(ord("A") + index)
                                teammate_kit = teammate["kit"]
                                break
                    if entity_here:
                        row_str += colorize(entity_here, teammate_kit)
                    elif cell == 'W':
                        wall_char = "|" if dx == 0 or dx == mini_width - 1 else "_"
                        row_str += colorize(wall_char)
                    elif isinstance(cell, int):
                        row_str += colorize(str(cell))
                    else:
                        row_str += " "
                if dx < mini_width - 1:
                    row_str += " "
        row_str += " |"
        print(row_str)

    print("|__________________________|")


def display_hud(player_kit: dict, player_health: int, player_pos: list[int], 
                player_cooldowns: dict[str, int], counter: int, survival_time: int, teammates: list[dict]) -> None:
    print("┌─────────────────────────────────────────────┐")
    print(f"│ {player_kit['kit']:<8} │ Time: {survival_time - counter:<3} │ HP: {player_health:<3} │ Pos: ({player_pos[0]},{player_pos[1]}) │")
    print("├─────────────────────────────────────────────┤")
    for ability, cooldown in player_cooldowns.items():
        print(f"│ {ability:<20} │ CD: {cooldown:<2} │")
    print("├─────────────────────────────────────────────┤")
    for teammate in teammates:
        state = "DOWN" if not teammate["alive"] else f"HP:{teammate['health']:<3} Pos:{teammate['pos'][0]},{teammate['pos'][1]}"
        print(f"│ {teammate['name']:<10} {teammate['kit']:<8} {state:<18}│")
    print("└─────────────────────────────────────────────┘")


class KitSelector:
    """Select a player kit and difficulty by number and return their names and timing settings."""

    KIT_MAP = {
        1: "Offense",
        2: "Support",
        3: "Defense",
    }

    @classmethod
    def select_kit(cls, kit_number: int) -> str:
        if kit_number not in cls.KIT_MAP:
            raise ValueError("Invalid kit selector. Use 1 for offense, 2 for support, 3 for defense.")
        return cls.KIT_MAP[kit_number]

    @classmethod
    def select_difficulty(cls, difficulty_number: int) -> str:
        if difficulty_number not in DIFFICULTY_SETTINGS:
            raise ValueError("Invalid difficulty selector. Use 1 for easy, 2 for normal, 3 for hard.")
        return DIFFICULTY_SETTINGS[difficulty_number]["name"]

    @classmethod
    def difficulty_settings(cls, difficulty_number: int) -> dict:
        if difficulty_number not in DIFFICULTY_SETTINGS:
            raise ValueError("Invalid difficulty selector. Use 1 for easy, 2 for normal, 3 for hard.")
        return DIFFICULTY_SETTINGS[difficulty_number].copy()

    @classmethod
    def select(cls, kit_number: int, difficulty_number: int) -> dict:
        settings = cls.difficulty_settings(difficulty_number)
        return {
            "kit": cls.select_kit(kit_number),
            "difficulty": settings["name"],
            "survival_time": settings["survival_time"],
        }


def offense_kit() -> dict:
    return {
        "kit": KitSelector.select_kit(1),
        "health": 90,
        "abilities": {
            "Lunge": {
                "cooldown": 8,
                "description": "Lunge forward with a powerful strike that stuns the enemy for 2 turns.",
                "distance": 2,
                "stun_time": 3,
                "distance_change": 2,
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
                "distance_change": 3,
            },
            "Jump": {
                "cooldown": 4,
                "description": "Jump to gain 1-turn invincibility.",
                "invincibility": 1,
            },
        },
    }


def defense_kit() -> dict:
    return {
        "kit": KitSelector.select_kit(3),
        "health": 165,
        "abilities": {
            "Repair Field": {
                "cooldown": 5,
                "description": "Heal yourself and gain a small shield.",
                "heal": 30,
                "overheal": 15,
            },
            "Shield Bash": {
                "cooldown": 6,
                "description": "Strike with a shield to stun and reduce incoming damage.",
                "distance": 1,
                "stun_time": 2,
                "shield": 15,
            },
            "Self-Destruct": {
                "cooldown": 10,
                "description": "Sacrifice health to stun the enemy and force them back.",
                "damage": 35,
                "self_damage": 20,
                "stun_time": 2,
                "range": 2,
            },
        },
    }


def enemy_kit() -> dict:
    return {
        "kit": "Executioner",
        "health": 220,
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
                "description": "Vanish briefly and close distance to the nearest target.",
                "damage": 30,
                "range": 4,
            },
            "Charge": {
                "cooldown": 8,
                "description": "Charge forward to pin the target and deal damage based on current health.",
                "base_damage": 10,
                "percent_health": 0.25,
                "range": 5,
                "distance_change": -3,
            },
        },
    }


def calculate_distance(a: list[int], b: list[int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def has_line_of_sight(start: list[int], end: list[int]) -> bool:
    if start == end:
        return True
    if start[0] == end[0]:
        step = 1 if end[1] > start[1] else -1
        for y in range(start[1] + step, end[1], step):
            if TERRAIN_MAP[y][start[0]] == 'W':
                return False
        return True
    if start[1] == end[1]:
        step = 1 if end[0] > start[0] else -1
        for x in range(start[0] + step, end[0], step):
            if TERRAIN_MAP[start[1]][x] == 'W':
                return False
        return True
    return False


def can_attack(attacker_pos: list[int], target_pos: list[int]) -> bool:
    return (
        has_line_of_sight(attacker_pos, target_pos)
        and abs(get_terrain_height(attacker_pos[0], attacker_pos[1]) - get_terrain_height(target_pos[0], target_pos[1])) <= 1
    )


def get_neighbors(position: list[int]) -> list[list[int]]:
    x, y = position
    current_height = get_terrain_height(x, y)
    results = []
    for dx, dy in [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]:
        nx, ny = x + dx, y + dy
        if is_valid_position(nx, ny, current_height):
            results.append([nx, ny])
    return results


def find_next_step(start: list[int], goal: list[int]) -> list[int] | None:
    if start == goal:
        return start
    queue = deque()
    queue.append((start, None))
    visited = {tuple(start)}

    while queue:
        current, first_step = queue.popleft()
        for neighbor in get_neighbors(current):
            neighbor_tuple = tuple(neighbor)
            if neighbor_tuple in visited:
                continue
            visited.add(neighbor_tuple)
            next_step = neighbor if first_step is None else first_step
            if neighbor == goal:
                return neighbor if first_step is None else first_step
            queue.append((neighbor, next_step))

    return None


def get_straight_direction(origin: list[int], target: list[int], away: bool = False) -> list[int]:
    dx = target[0] - origin[0]
    dy = target[1] - origin[1]
    if abs(dx) >= abs(dy):
        step = [1 if dx > 0 else -1 if dx < 0 else 0, 0]
    else:
        step = [0, 1 if dy > 0 else -1 if dy < 0 else 0]
    if away:
        step[0] *= -1
        step[1] *= -1
    return step


def move_straight_line(position: list[int], direction: list[int], distance: int) -> list[int]:
    current = position.copy()
    for _ in range(distance):
        next_pos = [current[0] + direction[0], current[1] + direction[1]]
        current_height = get_terrain_height(current[0], current[1])
        if not is_valid_position(next_pos[0], next_pos[1], current_height):
            break
        current = next_pos
    return current


def get_player_kit(kit_number: int) -> dict:
    if kit_number == 1:
        return offense_kit()
    if kit_number == 2:
        return support_kit()
    if kit_number == 3:
        return defense_kit()
    raise ValueError("Invalid kit selector. Use 1 for offense, 2 for support, 3 for defense.")


def create_teammate(name: str, kit_number: int, position: list[int]) -> dict:
    kit = get_player_kit(kit_number)
    return {
        "name": name,
        "kit": kit["kit"],
        "health": kit["health"],
        "max_health": kit["health"],
        "pos": position,
        "cooldowns": {ability_name: 0 for ability_name in kit["abilities"]},
        "abilities": kit["abilities"],
        "alive": True,
    }


def select_enemy_attack(enemy: dict, enemy_cooldowns: dict[str, int], enemy_pos: list[int], target_pos: list[int]) -> tuple[str | None, dict | None]:
    available = [name for name in enemy["abilities"] if enemy_cooldowns.get(name, 0) == 0]
    if not available:
        return None, None

    distance = calculate_distance(enemy_pos, target_pos)
    attackable = []
    for name in available:
        info = enemy["abilities"][name]
        if distance <= info.get("range", 1) and can_attack(enemy_pos, target_pos):
            attackable.append((name, info))

    if attackable:
        # Prefer the strongest ready attack in range.
        return max(attackable, key=lambda item: item[1].get("damage", 0))

    ability_name = random.choice(available)
    return ability_name, enemy["abilities"][ability_name]


def choose_int(prompt: str, valid_options: list[int]) -> int:
    while True:
        choice = input(prompt).strip()
        if choice.isdigit() and int(choice) in valid_options:
            return int(choice)
        print(f"Please enter one of {valid_options}.")


def choose_player_ability(player_kit: dict, cooldowns: dict[str, int]) -> tuple[str, dict]:
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


def apply_player_ability(
    ability_name: str,
    ability_data: dict,
    player_health: int,
    shield: int,
    player_pos: list[int],
    player_invincible: bool,
    player_max_health: int,
    enemy_pos: list[int],
    move_direction: list[int],
) -> tuple[int, int, list[int], int, bool]:
    enemy_stun = ability_data.get("stun_time", 0)

    if ability_name == "Skip":
        print("You skip your turn.")
        return player_health, shield, player_pos, 0, player_invincible

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
        steps = int(round(ability_data.get("distance_change", 3)))
        direction = move_direction if move_direction != [0, 0] else get_straight_direction(player_pos, enemy_pos)
        new_pos = move_straight_line(player_pos, direction, steps)
        if new_pos != player_pos:
            player_pos = new_pos
            print(f"You dash forward to position ({player_pos[0]}, {player_pos[1]}).")
        else:
            print("Dash blocked by terrain.")
    elif ability_name == "Fortify Guard":
        shield += 25
        print("You brace yourself and reduce the next incoming damage.")
    elif ability_name == "Sprint":
        steps = int(round(ability_data.get("distance_change", 3)))
        direction = get_straight_direction(player_pos, enemy_pos, away=True)
        new_pos = move_straight_line(player_pos, direction, steps)
        if new_pos != player_pos:
            player_pos = new_pos
            print(f"You sprint backward to position ({player_pos[0]}, {player_pos[1]}).")
        else:
            print("Sprint blocked by terrain.")
    elif ability_name == "Jump":
        print("You jump and become invincible for 1 turn.")
        player_invincible = True
    elif ability_name == "Lunge":
        steps = int(round(ability_data.get("distance_change", 2)))
        direction = get_straight_direction(player_pos, enemy_pos)
        new_pos = move_straight_line(player_pos, direction, steps)
        if new_pos != player_pos:
            player_pos = new_pos
            print(f"You lunge forward to position ({player_pos[0]}, {player_pos[1]}) and stun the enemy.")
        else:
            print("Lunge blocked by terrain.")
    elif ability_name == "Repair Field":
        heal_amount = ability_data["heal"]
        overheal_amount = ability_data.get("overheal", 0)
        healed = min(player_max_health - player_health, heal_amount)
        player_health += healed
        if healed < heal_amount and overheal_amount > 0:
            shield += overheal_amount
            print(f"You heal for {healed} and gain {overheal_amount} shield.")
        else:
            print(f"You heal for {healed}.")
    elif ability_name == "Shield Bash":
        shield += ability_data.get("shield", 0)
        print("You shield bash the enemy and prepare for the next hit.")
    elif ability_name == "Self-Destruct":
        self_damage = ability_data.get("self_damage", 0)
        player_health -= self_damage
        print(f"You detonate a self-destruct and take {self_damage} recoil damage.")
    else:
        print(f"You use {ability_name}.")
        if enemy_stun:
            print("The enemy is staggered by your attack.")

    return player_health, shield, player_pos, enemy_stun, player_invincible


def apply_enemy_attack(
    enemy_name: str,
    enemy_data: dict,
    target: dict,
    player_shield: int,
    is_player: bool,
    player_invincible: bool,
    enemy_pos: list[int],
    target_pos: list[int],
) -> tuple[int, int, bool, int, list[int]]:
    enemy_self_stun = 0
    if is_player and player_invincible:
        print(f"Executioner uses {enemy_name} but you are invincible and take no damage.")
        return target["health"], player_shield, player_invincible, enemy_self_stun, enemy_pos

    if enemy_name == "Charge":
        damage = enemy_data["base_damage"] + int(target["health"] * enemy_data["percent_health"])
    else:
        damage = enemy_data.get("damage", 0)

    if is_player:
        mitigated = min(player_shield, damage)
        damage -= mitigated
        player_shield -= mitigated
        target["health"] -= damage
        if mitigated:
            print(f"Your shield absorbs {mitigated} damage.")
    else:
        target["health"] -= damage

    if enemy_name == "Charge":
        steps = abs(int(round(enemy_data.get("distance_change", -3))))
        direction = get_straight_direction(enemy_pos, target_pos)
        new_enemy_pos = move_straight_line(enemy_pos, direction, steps)
        if new_enemy_pos != enemy_pos:
            enemy_pos = new_enemy_pos
            print(f"Executioner charges forward to {enemy_pos}.")
        else:
            print("Executioner charges but is blocked by terrain.")

    print(f"Executioner uses {enemy_name} and deals {damage} damage to {target['name']}.")
    return target["health"], player_shield, player_invincible, enemy_self_stun, enemy_pos


def choose_teammate_action(teammate: dict, enemy_pos: list[int]) -> tuple[str | None, dict | None]:
    if not teammate["alive"]:
        return None, None
    distance_to_enemy = calculate_distance(teammate["pos"], enemy_pos)
    available = [name for name, info in teammate["abilities"].items() if teammate["cooldowns"].get(name, 0) == 0]
    if teammate["health"] <= teammate["max_health"] * 0.5:
        for ability_name in available:
            info = teammate["abilities"][ability_name]
            if "heal" in info:
                return ability_name, info
    if distance_to_enemy <= 2:
        for ability_name in available:
            info = teammate["abilities"][ability_name]
            if info.get("stun_time", 0) > 0 or info.get("damage", 0) > 0:
                return ability_name, info
    return None, None


def choose_teammate_target(teammate: dict, enemy_pos: list[int], player_pos: list[int]) -> list[int]:
    distance_to_enemy = calculate_distance(teammate["pos"], enemy_pos)

    if teammate["health"] <= teammate["max_health"] * 0.5:
        return player_pos

    best_pos = teammate["pos"]
    best_distance = distance_to_enemy
    for neighbor in get_neighbors(teammate["pos"]):
        neighbor_distance = calculate_distance(neighbor, enemy_pos)
        if neighbor_distance > best_distance:
            best_distance = neighbor_distance
            best_pos = neighbor

    if best_pos != teammate["pos"]:
        return best_pos

    # If the teammate can't move further away, stay near the player if that is safer.
    if calculate_distance(player_pos, enemy_pos) > best_distance:
        return player_pos

    return teammate["pos"]


def apply_teammate_action(teammate: dict, ability_name: str, ability_data: dict, enemy: dict, enemy_pos: list[int]) -> int:
    enemy_stun = 0
    if ability_name is None:
        return 0
    print(f"{teammate['name']} uses {ability_name}.")
    if "heal" in ability_data:
        healed = min(teammate["max_health"] - teammate["health"], ability_data["heal"])
        teammate["health"] += healed
        print(f"{teammate['name']} heals for {healed}.")
    elif ability_name == "Shield Bash":
        if calculate_distance(teammate["pos"], enemy_pos) <= ability_data.get("distance", 1):
            enemy_stun = ability_data.get("stun_time", 0)
            print(f"{teammate['name']} stuns the Executioner.")
    elif ability_name == "Self-Destruct":
        if calculate_distance(teammate["pos"], enemy_pos) <= ability_data.get("range", 2):
            enemy_stun = ability_data.get("stun_time", 0)
            teammate["health"] -= ability_data.get("self_damage", 0)
            print(f"{teammate['name']} self-destructs and takes recoil damage.")
    elif ability_name == "Lunge":
        steps = int(round(ability_data.get("distance_change", 2)))
        direction = get_straight_direction(teammate["pos"], enemy_pos)
        new_pos = move_straight_line(teammate["pos"], direction, steps)
        if new_pos != teammate["pos"]:
            teammate["pos"] = new_pos
            print(f"{teammate['name']} lunges forward to {teammate['pos']}.")
    elif ability_name == "Dash Forward":
        steps = int(round(ability_data.get("distance_change", 2)))
        direction = get_straight_direction(teammate["pos"], enemy_pos)
        new_pos = move_straight_line(teammate["pos"], direction, steps)
        if new_pos != teammate["pos"]:
            teammate["pos"] = new_pos
            print(f"{teammate['name']} dashes forward to {teammate['pos']}.")
    elif ability_name == "Sprint":
        steps = int(round(ability_data.get("distance_change", 3)))
        direction = get_straight_direction(teammate["pos"], enemy_pos, away=True)
        new_pos = move_straight_line(teammate["pos"], direction, steps)
        if new_pos != teammate["pos"]:
            teammate["pos"] = new_pos
            print(f"{teammate['name']} sprints back to {teammate['pos']}.")
    return enemy_stun


def play_survival_game() -> None:
    print("Welcome to Survivor vs Executioner!")
    print("Choose your survivor kit:")
    print("  1. Offense\n  2. Support\n  3. Defense")
    kit_choice = choose_int("Kit number: ", [1, 2, 3])
    print("Choose your difficulty:")
    print("  1. Easy\n  2. Normal\n  3. Hard")
    difficulty_choice = choose_int("Difficulty (1=Easy, 2=Normal, 3=Hard): ", [1, 2, 3])

    settings = KitSelector.select(kit_choice, difficulty_choice)
    player_kit = get_player_kit(kit_choice)
    enemy = enemy_kit()
    survival_time = settings["survival_time"]

    player_pos = [10, 8]
    enemy_pos = [2, 8]
    teammate_kit_numbers = [k for k in (1, 2, 3) if k != kit_choice]
    teammates = [
        create_teammate("Ally A", teammate_kit_numbers[0], [4, 10]),
        create_teammate("Ally B", teammate_kit_numbers[1], [6, 10]),
    ]

    player_health = player_kit["health"]
    player_max_health = player_health
    shield = 0
    player_stun = 0
    enemy_stun = 0
    counter = 0
    player_invincible = False
    lms_triggered = False
    last_move_direction = [0, 0]
    player_cooldowns = {name: 0 for name in player_kit["abilities"]}
    enemy_cooldowns = {name: 0 for name in enemy["abilities"]}

    print(f"\nStarting as {player_kit['kit']} on {settings['difficulty']} difficulty.")
    print(f"Survive for {survival_time} turns.\n")

    while counter < survival_time and player_health > 0:
        display_hud(player_kit, player_health, player_pos, player_cooldowns, counter, survival_time, teammates)
        display_mini_map(player_pos, enemy_pos, teammates)

        print(f"\n=== TURN {counter + 1} ===")

        if enemy_stun > 0:
            print("=== ENEMY PHASE ===")
            print("The Executioner is stunned and cannot act this turn.")
            enemy_stun -= 1
        else:
            print("=== ENEMY PHASE ===")
            target_candidates = [
                {"type": "player", "name": "Player", "pos": player_pos, "health": player_health, "is_player": True},
            ]
            target_candidates.extend(
                {
                    "type": "teammate",
                    "name": teammate["name"],
                    "pos": teammate["pos"],
                    "health": teammate["health"],
                    "is_player": False,
                    "teammate": teammate,
                }
                for teammate in teammates if teammate["alive"]
            )
            if target_candidates:
                best_target = min(
                    target_candidates,
                    key=lambda item: calculate_distance(enemy_pos, item["pos"]) + (5 if item["is_player"] else 0),
                )
                enemy_name, enemy_data = select_enemy_attack(enemy, enemy_cooldowns, enemy_pos, best_target["pos"])
                in_range = calculate_distance(enemy_pos, best_target["pos"]) <= enemy_data.get("range", 1) if enemy_name else False
                if enemy_name and in_range and can_attack(enemy_pos, best_target["pos"]):
                    target = best_target
                    if target["is_player"]:
                        target_state = {"health": player_health, "name": "Player"}
                    else:
                        target_state = {"health": target["teammate"]["health"], "name": target["name"], "teammate": target["teammate"]}
                    target_health, shield, player_invincible, enemy_self_stun, enemy_pos = apply_enemy_attack(
                        enemy_name,
                        enemy_data,
                        target_state,
                        shield,
                        target["is_player"],
                        player_invincible,
                        enemy_pos,
                        best_target["pos"],
                    )
                    if target["is_player"]:
                        player_health = target_health
                    else:
                        target["teammate"]["health"] = target_health
                        if target["teammate"]["health"] <= 0:
                            target["teammate"]["alive"] = False
                            survival_time += 30
                            print(f"{target['name']} has been downed! Timer extended by 30 seconds.")
                            if not lms_triggered and all(not mate["alive"] for mate in teammates):
                                lms_triggered = True
                                survival_time = counter + 140
                                player_health = 165
                                player_max_health = 165
                                print("LMS event triggered! Timer reset to 140 and your health is restored to 165.")
                    enemy_stun += enemy_self_stun
                    enemy_cooldowns[enemy_name] = enemy_data["cooldown"]
                else:
                    next_step = find_next_step(enemy_pos, best_target["pos"])
                    if next_step and next_step != enemy_pos:
                        enemy_pos = next_step
                        print(f"Executioner moves to {enemy_pos}.")
                    else:
                        if enemy_name is None:
                            print("The Executioner has no abilities ready and is forced to recover this turn.")
                        else:
                            print("Executioner cannot attack from this location and waits.")

        print("\n=== TEAMMATE PHASE ===")
        for teammate in teammates:
            if not teammate["alive"]:
                continue
            action_name, action_data = choose_teammate_action(teammate, enemy_pos)
            if action_name is None:
                target_pos = choose_teammate_target(teammate, enemy_pos, player_pos)
                next_step = find_next_step(teammate["pos"], target_pos)
                if next_step and next_step != teammate["pos"]:
                    teammate["pos"] = next_step
                    if target_pos == player_pos:
                        print(f"{teammate['name']} retreats toward the player to {teammate['pos']}.")
                    elif target_pos == enemy_pos:
                        print(f"{teammate['name']} backs away from the Executioner to {teammate['pos']}.")
                    else:
                        print(f"{teammate['name']} flees to {teammate['pos']}.")
                else:
                    print(f"{teammate['name']} holds position and keeps distance.")
                continue
            enemy_stun_from_teammate = apply_teammate_action(teammate, action_name, action_data, enemy, enemy_pos)
            teammate["cooldowns"][action_name] = action_data["cooldown"]
            if enemy_stun_from_teammate > 0:
                enemy_stun += enemy_stun_from_teammate
            if teammate["health"] <= 0:
                teammate["alive"] = False
                survival_time += 30
                print(f"{teammate['name']} was lost during the fight and the timer gains 30 seconds.")
                if not lms_triggered and all(not mate["alive"] for mate in teammates):
                    lms_triggered = True
                    survival_time = counter + 140
                    player_health = 165
                    player_max_health = 165
                    print("LMS event triggered! Timer reset to 140 and your health is restored to 165.")

        if player_stun > 0:
            print("You are stunned and lose this turn.")
            player_stun -= 1
        else:
            print("\n=== MOVEMENT PHASE ===")
            print("Use W/A/S/D keys to move, or Q/E/Z/C for diagonals, or press Enter to skip movement:")
            print("  W = North (up)")
            print("  A = West (left)")
            print("  S = South (down)")
            print("  D = East (right)")
            print("  Q = Northwest\n  E = Northeast\n  Z = Southwest\n  C = Southeast")

            move_input = input("Your move (W/A/S/D/Q/E/Z/C or Enter): ").strip().upper()
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
            elif move_input == 'Q':
                new_pos[0] -= 1
                new_pos[1] -= 1
                direction = "northwest"
            elif move_input == 'E':
                new_pos[0] += 1
                new_pos[1] -= 1
                direction = "northeast"
            elif move_input == 'Z':
                new_pos[0] -= 1
                new_pos[1] += 1
                direction = "southwest"
            elif move_input == 'C':
                new_pos[0] += 1
                new_pos[1] += 1
                direction = "southeast"
            else:
                direction = None

            if direction:
                current_height = get_terrain_height(player_pos[0], player_pos[1])
                if is_valid_position(new_pos[0], new_pos[1], current_height):
                    last_move_direction = [new_pos[0] - player_pos[0], new_pos[1] - player_pos[1]]
                    player_pos = new_pos
                    print(f"You move {direction} to position ({player_pos[0]}, {player_pos[1]})")
                else:
                    print(f"Cannot move {direction} - blocked by wall or terrain height difference!")
            else:
                print("You stay in place.")

            print("\n=== ABILITY PHASE ===")
            ability_name, ability_data = choose_player_ability(player_kit, player_cooldowns)
            if ability_name != "Skip":
                player_health, shield, player_pos, new_enemy_stun, player_invincible = apply_player_ability(
                    ability_name, ability_data, player_health, shield, player_pos, player_invincible, player_max_health, enemy_pos, last_move_direction
                )
                player_cooldowns[ability_name] = ability_data["cooldown"]
                enemy_stun += new_enemy_stun

        player_cooldowns = {name: max(0, cooldown - 1) for name, cooldown in player_cooldowns.items()}
        enemy_cooldowns = {name: max(0, cooldown - 1) for name, cooldown in enemy_cooldowns.items()}
        for teammate in teammates:
            teammate["cooldowns"] = {name: max(0, cooldown - 1) for name, cooldown in teammate["cooldowns"].items()}

        counter += 1
        print()

    if player_health <= 0:
        print("You were defeated by the Executioner.")
    else:
        print("You survived the timer and escaped! Congratulations.")


if __name__ == "__main__":
    play_survival_game()
