import code
import operation
import screen
import random
import time

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


def AI_move(ai, player, again=None):
    difficulty = code.Config["SETTING"]["AI Difficulty"]["setting"]
    dice_list = code.Config["SETTING"]["AI Difficulty"][difficulty]["M_dice"]
    distance = operation.calculate_distance(ai.pos[0], player.pos[0])
    occ_leave_pos = occ_leave()
    if again:
        dice = again
    else:
        dice = random.choice(dice_list)
    GAMING.display_statue(dice, code.SCREEN)
    pos_list = operation.move_person_pos(ai.pos[0], player.pos[0], dice, code.Config["MAP"]["map 1"]["list pos"])
    GAMING.display_move_red_dot(pos_list)
    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    if pos_list:
        return_pos_list = pos_list
    else:
        return None, None
    for i in pos_list:
        # ai会优先选择特殊点位移动
        if i in code.Config["MAP"]["map 1"]["list pos"]["special dot"]:
            return_pos_list.append(i)
        # 周围有胜利点位再加一次权重
        if i in code.Config["MAP"]["map 1"]["list pos"]["win dot"]:
            return_pos_list.append(i)
    # 血量较少并且没有盾牌的情况下
    if ai.HP <= 3 and ai.DEF_prop + ai.DEF_dice + ai.DEF_ai < 1:
        # 如果距离较近
        if distance[0] in (1, 2) or distance[1] in (1, 2):
            # 假如可以移动到大炮的点位并且敌人血量也很少，增加选择权重
            if player.HP <= 3 and code.Config["MAP"]["map1"]["cannon dot"][0] in pos_list:
                return_pos_list.append(code.Config["MAP"]["map1"]["cannon dot"][0])
                return_pos_list.append(code.Config["MAP"]["map1"]["cannon dot"][0])
            # 假如周围可以回血，增加选择权重
            if code.Config["MAP"]["map1"]["recovery dot"][0] in pos_list:
                return_pos_list.append(code.Config["MAP"]["map1"]["recovery dot"][0])
            if code.Config["MAP"]["map1"]["recovery dot"][1] in pos_list:
                return_pos_list.append(code.Config["MAP"]["map1"]["recovery dot"][1])
            # 假如只剩一个点位还没有占领，立即占领赢得游戏
            if len(occ_leave_pos) == 1 and occ_leave_pos[0] in pos_list:
                return occ_leave_pos[0], None
            # 上述情况都不满足的话，尽可能远离对方/多权重
            for i in pos_list:
                distance = operation.calculate_distance(i, player.pos[0])
                if distance[0] not in (1, 2) and distance[1] not in (1, 2):
                    return_pos_list.append(distance)
        # 假如周围没有敌人，尽可能回血
        else:
            # 假如周围可以回血，增加选择权重*2
            if code.Config["MAP"]["map1"]["recovery dot"][0] in pos_list:
                return_pos_list.append(code.Config["MAP"]["map1"]["recovery dot"][0])
                return_pos_list.append(code.Config["MAP"]["map1"]["recovery dot"][0])
            if code.Config["MAP"]["map1"]["recovery dot"][1] in pos_list:
                return_pos_list.append(code.Config["MAP"]["map1"]["recovery dot"][1])
                return_pos_list.append(code.Config["MAP"]["map1"]["recovery dot"][1])
        return random.choice(return_pos_list), dice
    # 如果自身血量充足的情况
    elif ai.HP >= 5:
        # 如果敌人血量较少
        if player.HP <= 2:
            # 尽可能接近对手/固定寻找最近路线
            j = (100, 100)
            for i in pos_list:
                distance = operation.calculate_distance(i, player.pos[0])
                if j[0] + j[1] > distance[0] + distance[1]:
                    j = distance
                    return_pos_list = i
            return return_pos_list, dice
        # 如果对方有充足血量
        else:
            # 如果敌人占据大炮点位，尽可能远离对方/多权重
            if player.pos[0] == code.Config["MAP"]["map1"]["cannon dot"][0]:
                for i in pos_list:
                    distance = operation.calculate_distance(i, player.pos[0])
                    if distance[0] not in (1, 2) and distance[1] not in (1, 2):
                        return_pos_list.append(distance)
                return random.choice(return_pos_list), dice
            # 如果敌人没有站在大炮点位
            else:
                # 尽可能接近对手/固定寻找最近路线
                j = (100, 100)
                for i in pos_list:
                    distance = operation.calculate_distance(i, player.pos[0])
                    if j[0] + j[1] > distance[0] + distance[1]:
                        j = distance
                        return_pos_list = i
                return return_pos_list, dice
    else:
        return_pos_list = pos_list
        return random.choice(return_pos_list)


