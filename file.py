import random





def classes(): # This will be used to get the classes to use in-game (1998 is a dev character)
    class_num = int(input("Enter a number, 1 for offensive, 2 for support, 3 for defensive/survivalist:"))
    if class_num != 1 and class_num != 2 and class_num != 3 and != 1998:
        print("Not a valid class:")
        class_num = int(input("Enter a number, 1 for offensive, 2 for support, 3 for defensive/survivalist:"))
    if class_num == 1:
        class_name = "Offense"
        class_hp = 100
        defense_fighter = 1
        list_classes = [class_num, class_name, class_hp, defense_fighter, dodge_hp,]

        teammate_name = "Support"
        teammate_hp = 100
        defense_teammate = 1
        list_teammate = [teammate_name, teammate_hp, defense_teammate]

    elif class_num == 2:
        class_name = "Support"
        class_hp = 100
        defense_support = 1
        list_classes = [class_num, class_name, class_hp, defense_support,]

        teammate_name = "Defense"
        teammate_hp = 150
        defense_teammate = .5
        list_teammate = [teammate_name, teammate_hp, defense_teammate]

    elif class_num == 3:
        class_name = "Defense"
        class_hp = 150
        defense_defense = 1.5
        list_classes = [class_num, class_name, class_hp, defense_defense]

        teammate_name = "Offense"
        teammate_hp = 100
        defense_teammate = 1
        list_teammate = [teammate_name, teammate_hp, defense_teammate]
    return list_classes
    

def difficulty(): 

    difficulty_num = int(input("Enter difficulty, 1 is easy, 2 is medium, 3 is hard: "))
    while difficulty_num != 1 and difficulty_num != 2 and difficulty_num != 3:
        print("Invalid difficulty")
        difficulty_num = int(input("Enter difficulty, 1 is easy, 2 is medium, 3 is hard: "))
    if difficulty_num == 1:
        difficulty = "easy"
        defense = .25
        damage_multi = 1.5
    
    elif difficulty_num == 2:
        difficulty = "medium"
        defense = .1
        damage_multi = 1.1
    
    elif difficulty_num == 3:
        difficulty = "hard"
        defense = 0
        damage_multi = 1

    elif difficulty_num == 1998:
        difficulty = "outcome"
        defense = .5
        damage_multi = 0
        list_difficulty = [difficulty_num, difficulty, defense, damage_multi]

def enemy1():
    pass
    

def enemy_outcome(): # dev enemy with 1998 modifier, not a killable boss, but a survival enemy
    enemy_name = "outcome"
    enemy_distance_closing = 12
    enemy_attacks = {
        # attack: cooldown (for this enemy only, others will be attack: dmg)
        "slash": 1,
        "God's trickery": 10,
        "Lunge": 6 
    }
    enemy_damages = {
        "slash": 5,
        "God's trickery": 25,
        "Lunge": 35
    }

    enemy_stats = [enemy_name, enemy_distance_closing, enemy_attacks, enemy_damages, enemy_distance]

    enemy_distance = 150 # Distance is health in this situation, it will never hit 0, but it shows how far the enemy is.
    return enemy_stats



classes()
difficulty()

if difficulty_num = 1998 and class_num = 1998:
    #This is to run the outcome gamemode, it's intended to be a "Last Man Standing" survival that lasts 20 turns, the kit will only work if both outcome modes are on.

    enemy_outcome():

    for turns_left in (1, 20):
        
        #Enemy turn (outcome)

        if cooldown1 <= 1:
            turn_attack = 3
        elif cooldown = 0:
            turn_attack.randint(0, 2)

        if turn_attack = 0:
            if enemy_distance < 10:
                attack = "slash"
                damage = 5
                cooldown_1 = 1
            else:
                attack = "miss"
                damage = 0
                cooldown_1 = 1

        elif turn_attack = 1:
            #No distance, it's a mapwide
            attack = "Minigame"
            damage = 15
            cooldown_2 = 3
            enemy_distance = 40


        elif turn_attack = 2:
            if enemy_distance <= 30:
                attack = "Choke"
                damage = 25
                cooldown_3 = 4
            else:
                attack = "nothing"
                damage = 0
                cooldown_3 -=1
        elif turn_attack = 3:
            cooldown -=1

        if dodge_hp >= damage:
            dodge_hp = dodge_hp - damage
        elif dodge_hp <= damage:
            class_hp = (class_hp + dodge_hp) - damage

        cooldown_1 -= 1
        cooldown_2 -= 1
        cooldown_3 -= 1

        #Player turn(outcome)

        player_attack = int(input("Use an ability,0 to do nothing, 1 is \"Hit and run\", 2 is \"Run\""))
        while player_attack != 1 and player_attack != 2:
            print("Invalid, please enter a valid attack: ")
            int(input("Use an ability or hit 0 to do nothing."))
        if player_attack = 0:
            enemy_distance = enemy_distance + 40
        elif player_attack = 1:
            dodge_hp += 20
            enemy_distance += 20
            cooldown_4 = 3
        elif player_attack = 2:
            enemy_distance += 50
            cooldown_5 = 3

        cooldown_4 -= 1
        cooldown_5 -= 1
        turns_left -= 1

    
elif difficulty_num = 1998 and class_num != 1998 or difficulty_num != 1998 and class_num = 1998:
    print("The character/difficulty combination must be active in order to play this mode.")
    break
