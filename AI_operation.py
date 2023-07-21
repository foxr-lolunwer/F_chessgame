import code
import operation
import screen
import random

GAMING = screen.Gaming()

def occ_leave():
    occ_dict = code.Config["MAP"]["map 1"]["win dot occ list"]
    count = 0
    occ_list_leave = []
    for i in occ_dict.keys():
        if occ_dict[i] == "p2":
            count += 1
        else:
            occ_list_leave.append(int(i))
    return occ_list_leave


def AI_move(ai, player, statue):
    difficulty = code.Config["SETTING"]["AI Difficulty"]["setting"]
    if statue == "m":
        dice_list = code.Config["SETTING"]["AI Difficulty"][difficulty]["M_dice"]
    elif statue == "f":
        dice_list = code.Config["SETTING"]["AI Difficulty"][difficulty]["M_dice"]
    else:
        return  # error
    distance = operation.calculate_distance(ai.pos[0], player.pos[0])
    occ_leave_pos = occ_leave()
    if distance[0] in (1, 2) or distance[1] in (1, 2):
        if ai.HP <= 3 and ai.DEF_prop + ai.DEF_dice + ai.DEF_ai < 1:
            pos_list = operation.move_person_pos(ai.pos[0], player.pos[0], random.choice(dice_list),
                                                 code.Config["MAP"]["map 1"]["list pos"])
            GAMING.display_move_red_dot(pos_list)
            return_pos_list = []
            if player.HP <= 3 and code.Config["MAP"]["map1"]["cannon dot"][0] in pos_list:
                return_pos_list.append(code.Config["MAP"]["map1"]["cannon dot"][0])
                return_pos_list.append(code.Config["MAP"]["map1"]["cannon dot"][0])
            if code.Config["MAP"]["map1"]["recovery dot"][0] in pos_list:
                return_pos_list.append(code.Config["MAP"]["map1"]["recovery dot"][0])
            if code.Config["MAP"]["map1"]["recovery dot"][1] in pos_list:
                return_pos_list.append(code.Config["MAP"]["map1"]["recovery dot"][1])

            if len(occ_leave_pos) == 1 and occ_leave_pos[0] in pos_list:
                return occ_leave_pos[0]
            for i in pos_list:
                distance = operation.calculate_distance(i, player.pos[0])
                if distance not in (1, 2) and distance not in (1, 2):
                    return_pos_list.append(distance)
            if distance:
                return random.choice(return_pos_list)
            else:
                return random.choice(return_pos_list)


