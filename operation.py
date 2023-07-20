import random

import code

LIST_M_DICE = code.Config["SETTING"]["M_dice"]
LIST_F_DICE = code.Config["SETTING"]["F_dice"]


def dice(dice_type):
    if dice_type == "m":
        return random.choice(LIST_M_DICE)
    elif dice_type == "f":
        return random.choice(LIST_F_DICE)
    else:
        print("dice error")


def move_person_pos(per_g_pos, other_per_g_pos, dice_val, dict_map_pos):
    player_g_pos_list = (per_g_pos, other_per_g_pos)
    move_available_pos = []
    while True:
        # 十字移动
        if dice_val == "cross":
            move_available_pos_l = [per_g_pos + 1, per_g_pos - 1, per_g_pos + 100, per_g_pos - 100]
            move_available_pos = []
            for i in move_available_pos_l:
                if i in dict_map_pos["game available"] and i not in player_g_pos_list:
                    move_available_pos.append(i)
        # 斜线移动
        elif dice_val == "diagonal":
            move_available_pos_l = [per_g_pos + 99, per_g_pos - 99, per_g_pos + 101, per_g_pos - 101]
            move_available_pos = []
            for i in move_available_pos_l:
                if i in dict_map_pos["game available"] and i not in player_g_pos_list:
                    move_available_pos.append(i)
        # 传送 ！未完成预定功能
        elif dice_val == "tp":
            move_available_pos_l = dict_map_pos["tp available"]
            move_available_pos = [0]
            for i in move_available_pos_l:
                if i not in player_g_pos_list:
                    move_available_pos.append(i)
        # 自由移动（十字移动两次）
        elif dice_val == "free":
            move_available_pos_l = [per_g_pos, per_g_pos + 1, per_g_pos - 1, per_g_pos + 100, per_g_pos - 100,
                                    per_g_pos + 2, per_g_pos - 2, per_g_pos + 200, per_g_pos - 200,
                                    per_g_pos + 99, per_g_pos - 99, per_g_pos + 101, per_g_pos - 101]
            move_available_pos = [0]
            for i in move_available_pos_l:
                if i in dict_map_pos["game available"] and i != other_per_g_pos:
                    move_available_pos.append(i)
        if move_available_pos:
            return move_available_pos
        else:
            return None


def fight_kill_val(per_g_pos, other_per_g_pos, dice_val, dict_map_pos):
    if dice_val == "single shot":
        if other_per_g_pos in [per_g_pos, per_g_pos + 1, per_g_pos - 1, per_g_pos + 100, per_g_pos - 100, per_g_pos + 2,
                               per_g_pos - 2, per_g_pos + 200, per_g_pos - 200, per_g_pos + 99, per_g_pos - 99,
                               per_g_pos + 101, per_g_pos - 101]:
            return 1
    elif dice_val == "multiple shots":
        if other_per_g_pos in [per_g_pos, per_g_pos + 1, per_g_pos - 1, per_g_pos + 100, per_g_pos - 100, per_g_pos + 2,
                               per_g_pos - 2, per_g_pos + 200, per_g_pos - 200, per_g_pos + 99, per_g_pos - 99,
                               per_g_pos + 101, per_g_pos - 101]:
            return 2
    elif dice_val == "X explosion":
        fight_pos_l = []
        for i in range(1, 10):
            if per_g_pos - 101 * i in dict_map_pos["game available"]:
                fight_pos_l.append(per_g_pos - 101 * i)
            if per_g_pos - 99 * i in dict_map_pos["game available"]:
                fight_pos_l.append(per_g_pos - 99 * i)
            if per_g_pos + 99 * i in dict_map_pos["game available"]:
                fight_pos_l.append(per_g_pos + 99 * i)
            if per_g_pos + 101 * i in dict_map_pos["game available"]:
                fight_pos_l.append(per_g_pos + 101 * i)
        if other_per_g_pos in fight_pos_l:
            return 2
    elif dice_val == "bomb":
        return 1
    elif dice_val == "life recovery":
        return -1
    elif dice_val == "shield":
        return -2
    else:
        "fight_kill_val error"
    return 0


def move_click(list_pos, AI=None):
    if not list_pos:
        return None
    if AI:
        pos = random.choice(list_pos)
        pos = (pos, code.change_pos(pos))
        return pos
    while True:
        down_mouse_move_g_pos = code.get_mouse_pos()
        if down_mouse_move_g_pos in list_pos:
            pos = (down_mouse_move_g_pos, code.change_pos(down_mouse_move_g_pos))  # 新位置坐标
            return pos


def find_winner(player1_hp=True, player2_hp=True, occ_dict=None):
    # 如果player1生命为零
    if player1_hp <= 0:
        return "p2"
    # 如果player2生命为零
    if player2_hp <= 0:
        return "p1"
    if occ_dict:
        occ_list = []
        for k in occ_dict.keys():
            occ_list.append(occ_dict[k])
        if len(set(occ_list)) == 1 and occ_list[0] != "":
            return occ_list[0]
    return None


def calculate_distance(per1_g_pos0, per2_g_pos0):
    x = abs(per1_g_pos0 // 100 - per2_g_pos0 // 100)
    y = abs(per1_g_pos0 % 100 - per2_g_pos0 % 100)
    return x, y
