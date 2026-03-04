import random





def classes(): # This will be used to get the classes to use in-game (1998 is a dev character)
    class_num = int(input("Enter a number, 1 for offensive, 2 for support, 3 for defensive/survivalist:"))
    if class_num != 1 and class_num != 2 and class_num != 3 and != 1998:
        print("Not a valid class:")
        class_num = int(input("Enter a number, 1 for offensive, 2 for support, 3 for defensive/survivalist:"))
    if class_num == 1:
        class_name = "Offense"
        class_hp = 100
        defense_offense = 1
        list_classes = [1, class_name, class_hp, defense_offense]

        teammate_name = "Support"
        teammate_hp = 100
        defense_teammate = 1
        list_teammate = [2, teammate_name, teammate_hp, defense_teammate]

    elif class_num == 2:
        class_name = "Support"
        class_hp = 100
        defense_support = 1
        list_classes = [2, class_name, class_hp, defense_support,]

        teammate_name = "Defense"
        teammate_hp = 150
        defense_teammate = .5
        list_teammate = [3, teammate_name, teammate_hp, defense_teammate]

    elif class_num == 3:
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
for turns_passed in num_turns:
    pass