import random



#Define variables, in particular the following: user/teammate dmg, cd, distance. Kit hp, stun counter, and the attacks with damage on enemy.




def classes(): # This will be used to get the classes to use in-game
    class_num = int(input("Enter a number, 1 for offensive, 2 for support, 3 for defensive/survivalist:")) # Class selector
    if class_num != 1 and class_num != 2 and class_num != 3:
        print("Not a valid class:") # Confirms a class is seected
        class_num = int(input("Enter a number, 1 for offensive, 2 for support, 3 for defensive/survivalist:")) # Restarts class selector
    if class_num == 1: # Offense kit/Support ally
        class_name = "Offense"
        class_hp = 100
        defense_offense = 1
        list_classes = [1, class_name, class_hp, defense_offense]

        teammate_name = "Support"
        teammate_hp = 100
        defense_teammate = 1
        list_teammate = [2, teammate_name, teammate_hp, defense_teammate]

    elif class_num == 2: # Support kit/Defense ally
        class_name = "Support"
        class_hp = 100
        defense_support = 1
        list_classes = [2, class_name, class_hp, defense_support,]

        teammate_name = "Defense"
        teammate_hp = 150
        defense_teammate = .5
        list_teammate = [3, teammate_name, teammate_hp, defense_teammate]

    elif class_num == 3: # Defense kit/Offense ally
        class_name = "Defense"
        class_hp = 150
        defense_defense = 1.5
        list_classes = [3, class_name, class_hp, defense_defense]

        teammate_name = "Offense"
        teammate_hp = 100
        defense_teammate = 1
        list_teammate = [1, teammate_name, teammate_hp, defense_teammate]
    return list_classes
    


difficulty_num = int(input("Enter difficulty, 1 is easy, 2 is medium, 3 is hard: "))
while difficulty_num != 1 and difficulty_num != 2 and difficulty_num != 3:
    print("Invalid difficulty")
    difficulty_num = int(input("Enter difficulty, 1 is easy, 2 is medium, 3 is hard: "))
if difficulty_num == 1:
    difficulty = "Easy"
    damage_multi = 1.5
    num_turns = 30
elif difficulty_num == 2:
    difficulty = "medium"
    damage_multi = 1.25
    num_turns = 30
elif difficulty_num == 3:
    difficulty = "hard"
    damage_multi = 1.5
    num_turns = 50
difficulty_stats = [difficulty, damage_multi, num_turns]


# Little note I should add again here, damage and all damage-related information is used as stun time, which is why damage appears as lower.



if class_name == "Offense":
    attack_1 = "Dash"
    attack_1_dmg = 2
    attack_1_distance = 1
    
    attack_2 = "Roll"
    attack_2_dmg = 1
    attack_2_distance = 3
    attack_2_cd = 5

    teammate_1_1 = "Heal"
    teammate_1_1_dmg = 0
    teammate_1_1_distance = 4
    teammate_1_1_cd = 3

    teammate_1_2 = "dodge"
    teammate_1_2_dmg = 0
    teammate_1_2_distance = 2
    teammate_1_2_cd = 2

elif class_name == "Support":
    attack_1 = "Heal"
    attack_1_dmg = 0
    attack_1_distance = 4
    attack_1_cd = 3

    attack_2 = "dodge"
    attack_2_dmg = 0
    attack_2_distance = 2
    attack_2_cd = 2

    teammate_1_1 = "Charge"
    teammate_1_1_dmg = 4
    teammate_1_1_distance = 2
    teammate_1_1_cd = 2

    teammate_1_2 = "Self-heal"
    teammate_1_2_dmg = 0
    teammate_1_2_distance = 4
    teammate_1_2_cd = 3


elif class_name == "Defense":
    attack_1 = "Charge"
    attack_1_dmg = 4
    attack_1_distance = 2
    attack_1_cd = 2

    attack_2 = "Self-heal"
    attack_2_dmg = 0
    attack_2_distance = 4
    attack_2_cd = 3

    teammate_1_1 = "Dash"
    teammate_1_1_dmg = 2
    teammate_1_1_distance = 1
    teammate_1_1_cd = 4

    teammate_1_2 = "Roll"
    teammate_1_2_dmg = 1
    teammate_1_2_distance = 3
    teammate_1_2_cd = 5


for turns_passed in num_turns:
    