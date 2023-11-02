#  Pyinstaller -F -w -i icon.ico Chessgame.py
#  Pyinstaller -F -i icon.ico Chessgame.py
import random
import sys
import time

import pygame

import code
import operation
import person
import screen


class FChessGame:
    def __init__(self):
        self.game_ver = "0.10"
        self.menu = screen.menu
        self.gaming_screen = screen.gaming_screen
        self.config = code.Config
        self.screen = self.screen_init()

    def screen_init(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Game ver " + self.game_ver)  # 窗口标题显示10
        m_screen = pygame.display.set_mode((1060, 636))  # 设置游戏窗口大小：530*636（像素）
        icon = pygame.image.load(self.config["IMG"]["icon"]).convert()  # 引入窗口图标
        pygame.display.set_icon(icon)  # 显示窗口坐标
        return m_screen


def occ_leave():
    occ_dict = code.load_map["win dot occ list"]
    occ_count = 0
    occ_list_leave = []
    for i in occ_dict.keys():
        if occ_dict[i] == "p2":
            occ_count += 1
        else:
            occ_list_leave.append(i)
    return occ_list_leave


def turn_move(player, other_players):
    player.selected()
    screen.gaming_screen.display_statue(player.name + code.T["Please throw!"], code.SCREEN)
    if screen.gaming_screen.gaming_throw():
        return
    t_command_move = random.choice(code.Config["SETTING"]["M_dice"])
    screen.gaming_screen.display_statue(player.name + code.T[t_command_move], code.SCREEN)
    t_command = operation.move_person_pos(player.pos[0], other_players.pos[0], t_command_move, map_pos)
    screen.gaming_screen.display_move_red_dot(t_command)
    t_person_pos = operation.move_click(t_command)
    if t_person_pos == "return":
        return
    if t_person_pos:
        player.pos = t_person_pos
    player.action_move -= 1
    if player.occ_buff(map_pos):
        win_dot_occ[code.map_dict_key_rel(player.pos[0])] = "p" + player.number
    screen.gaming_screen.ui_gaming_data_new(player, other_players)
    screen.gaming_screen.flip_screen(player, other_players, count, win_dot_occ)
    if screen.gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
        return
    if player.action_move > 0:
        player.selected()
        t_command = operation.move_person_pos(player.pos[0], other_players.pos[0], t_command_move, map_pos)
        screen.gaming_screen.display_move_red_dot(t_command)
        t_person_pos = operation.move_click(t_command)
    if t_person_pos == "return":
        return
    if t_person_pos:
        player.pos = t_person_pos
    player.action_move -= 1
    if player.occ_buff(map_pos):
        win_dot_occ[code.map_dict_key_rel(player.pos[0])] = "p" + player.number
    screen.gaming_screen.ui_gaming_data_new(player, other_players)
    screen.gaming_screen.flip_screen(player, other_players, count, win_dot_occ)
    if screen.gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
        return


def AI_move(ai, other_players, again=None):
    other_players.selected()
    screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["Please throw!"], code.SCREEN)
    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    difficulty = code.Config["SETTING"]["AI Difficulty"]["setting"]
    dice_list = code.Config["SETTING"]["AI Difficulty"][difficulty]["M_dice"]
    distance = operation.calculate_distance(ai.pos[0], other_players.pos[0])
    occ_leave_pos = occ_leave()
    if again:
        dice = again
    else:
        dice = random.choice(dice_list)
    screen.gaming_screen.display_statue(code.T["Player 2"] + code.T[dice], code.SCREEN)
    pos_list = operation.move_person_pos(ai.pos[0], other_players.pos[0], dice, code.load_map["list pos"])
    screen.gaming_screen.display_move_red_dot(pos_list)
    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    return_pos_list = []
    print(pos_list)
    if pos_list:
        for i in range(0, len(pos_list)):
            return_pos_list.append(pos_list[i])
        print(return_pos_list)
    else:
        person_pos, again = None, None
    if len(pos_list) == 1:
        person_pos, again = pos_list[0], None
    else:
        for i in pos_list:
            # ai会优先选择特殊点位移动
            if i in code.load_map["list pos"]["special dot"]:
                return_pos_list.append(i)
            # 周围有胜利点位再加一次权重
            if i in code.load_map["list pos"]["win dot"]:
                return_pos_list.append(i)
    # 血量较少并且没有盾牌的情况下
    if ai.HP <= 3 and ai.DEF_prop + ai.DEF_dice + ai.DEF_ai < 1:
        # 如果距离较近
        if distance[0] in (1, 2) or distance[1] in (1, 2):
            # 假如可以移动到大炮的点位并且敌人血量也很少，增加选择权重
            if other_players.HP <= 3 and code.load_map["list pos"]["cannon dot"][0] in pos_list:
                return_pos_list.append(code.load_map["list pos"]["cannon dot"][0])
                return_pos_list.append(code.load_map["list pos"]["cannon dot"][0])
            # 假如周围可以回血，增加选择权重
            if code.load_map["list pos"]["recovery dot"][0] in pos_list:
                return_pos_list.append(code.load_map["list pos"]["recovery dot"][0])
            if code.load_map["list pos"]["recovery dot"][1] in pos_list:
                return_pos_list.append(code.load_map["list pos"]["recovery dot"][1])
            # 假如只剩一个点位还没有占领，立即占领赢得游戏
            if len(occ_leave_pos) == 1 and occ_leave_pos[0] in pos_list:
                person_pos, again = occ_leave_pos[0], None
            # 上述情况都不满足的话，尽可能远离对方/多权重
            for i in pos_list:
                distance = operation.calculate_distance(i, other_players.pos[0])
                if distance[0] not in (1, 2) and distance[1] not in (1, 2):
                    return_pos_list.append(distance)
        # 假如周围没有敌人，尽可能回血
        else:
            # 假如周围可以回血，增加选择权重*2
            if code.load_map["list pos"]["recovery dot"][0] in pos_list:
                return_pos_list.append(code.load_map["list pos"]["recovery dot"][0])
                return_pos_list.append(code.load_map["list pos"]["recovery dot"][0])
            if code.load_map["list pos"]["recovery dot"][1] in pos_list:
                return_pos_list.append(code.load_map["list pos"]["recovery dot"][1])
                return_pos_list.append(code.load_map["list pos"]["recovery dot"][1])
        person_pos, again = random.choice(return_pos_list), dice
    # 如果自身血量充足的情况
    elif ai.HP >= 5:
        # 如果敌人血量较少
        if other_players.HP <= 2:
            # 尽可能接近对手/固定寻找最近路线
            j = (100, 100)
            for i in pos_list:
                distance = operation.calculate_distance(i, other_players.pos[0])
                if j[0] + j[1] > distance[0] + distance[1]:
                    j = distance
                    return_pos_list = i
            person_pos, again = return_pos_list, dice
        # 如果对方有充足血量
        else:
            # 如果敌人占据大炮点位，尽可能远离对方/多权重
            if other_players.pos[0] == code.load_map["list pos"]["cannon dot"][0]:
                for i in pos_list:
                    distance = operation.calculate_distance(i, other_players.pos[0])
                    if distance[0] not in (1, 2) and distance[1] not in (1, 2):
                        return_pos_list.append(distance)
                person_pos, again = random.choice(return_pos_list), dice
            # 如果敌人没有站在大炮点位
            else:
                # 尽可能接近对手/固定寻找最近路线
                j = (100, 100)
                for i in pos_list:
                    distance = operation.calculate_distance(i, other_players.pos[0])
                    if j[0] + j[1] > distance[0] + distance[1]:
                        j = distance
                        return_pos_list = i
                person_pos, again = return_pos_list, dice
    else:
        return_pos_list = pos_list
        return random.choice(return_pos_list), dice
    ai.action_move -= 1
    if person_pos:
        ai.pos = (person_pos, code.change_pos(person_pos))
    if ai.occ_buff(map_pos):
        win_dot_occ[code.map_dict_key_rel(ai.pos[0])] = "p2"
    screen.gaming_screen.ui_gaming_data_new(other_players, ai)
    screen.gaming_screen.flip_screen(other_players, ai, count, win_dot_occ)
    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 0.5)
    if screen.gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
        return


def turn_fight(player, other_players):
    if player.DEF_dice:
        player.DEF_dice = 0
        screen.gaming_screen.ui_gaming_data_new(player, other_players)
    player.selected()
    screen.gaming_screen.display_statue(code.T["Player 1"] + code.T["Please throw!"], code.SCREEN)
    if screen.gaming_screen.gaming_throw():
        return
    t_command_fight = random.choice(code.Config["SETTING"]["F_dice"])
    screen.gaming_screen.display_statue(code.T["Player 1"] + code.T[t_command_fight], code.SCREEN)
    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    t_command = operation.fight_kill_val(player.pos[0], other_players.pos[0], t_command_fight, map_pos)
    if t_command >= 0:
        t_command = t_command - (other_players.DEF_prop + other_players.DEF_dice)
        if t_command > 0:
            other_players.HP -= t_command
            screen.gaming_screen.display_statue(code.T["Player 1"] + code.T["Kill Val is "] + str(t_command), code.SCREEN)
        else:
            screen.gaming_screen.display_statue(code.T["Player 1"] + code.T["MISS"], code.SCREEN)
    elif t_command == -1:
        player.HP += 1
        screen.gaming_screen.display_statue(code.T["Player 1"] + code.T["HP Recovery"], code.SCREEN)
    elif t_command == -2:
        player.DEF_dice += 1
        screen.gaming_screen.display_statue(code.T["Player 1"] + code.T["DEF + 1"], code.SCREEN)
    else:
        "fight error"
    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    if screen.gaming_screen.screen_win(operation.find_winner(player.HP, other_players.HP)):
        return
    screen.gaming_screen.ui_gaming_data_new(player, other_players)
    player.selected(False)


if __name__ == '__main__':
    # code.game_init()
    # map_pos = code.load_map["list pos"]
    # win_dot_occ = code.load_map["win dot occ list"]
    # count = 0
    # code.play_music()
    # code.date_write("-GAME INIT DONE-", code.DATE_FILE)
    while True:
        screen.load()
        command = screen.menu.menu_main()
        if command == "start":
            command = screen.menu.menu_start()
            person_capacity = screen.gaming_screen.map["person capacity"]
            if command == "PVP":
                player1 = person.Person("1", (
                    screen.gaming_screen.map["person init pos"][0], code.change_pos(screen.gaming_screen.map["person init pos"][0])), "player 1")
                player2 = person.Person("2", (
                    screen.gaming_screen.map["person init pos"][1], code.change_pos(screen.gaming_screen.map["person init pos"][1])), "player 2")
                screen.gaming_screen.start_init(occ_dict=win_dot_occ)
                screen.gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                screen.gaming_screen.ui_gaming_val(win_dot_occ)
                screen.gaming_screen.ui_gaming_data_new(player1, player2)
                TURN = True
                # 开始回合
                code.date_write("-GAMING INIT DONE-", code.DATE_FILE)
                while TURN:
                    player1.action_move = 1
                    player2.action_move = 1
                    count += 1
                    screen.ui_gaming_turn(count)
                    turn_move(player1, player2)
                    turn_move(player2, player1)
                    turn_fight(player1, player2)
                    turn_fight(player2, player1)
            elif command == "PVE":
                player1 = person.Person("1", (
                    screen.gaming_screen.map["person init pos"][0], code.change_pos(screen.gaming_screen.map["person init pos"][0])), "player 1")
                player2 = person.AIPerson("2", (
                    screen.gaming_screen.map["person init pos"][1], code.change_pos(screen.gaming_screen.map["person init pos"][1])), "player 2")
                screen.gaming_screen.start_init(occ_dict=win_dot_occ)
                screen.gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                screen.gaming_screen.ui_gaming_val(win_dot_occ)
                screen.gaming_screen.ui_gaming_data_new(player1, player2)
                TURN = True
                # 开始回合
                code.date_write("-GAMING INIT DONE-", code.DATE_FILE)
                while TURN:
                    player1.action_move = 1  # 移动次数
                    player2.action_move = 1
                    count += 1  # 回合数
                    screen.ui_gaming_turn(count)
                    turn_move(player1, player2)
                    AI_move(player2, player1)
                    # p1 fight
                    turn_fight(player1, player2)
                    # p2 fight
                    turn_fight(player2, player1)
                    # if player2.DEF_dice:
                    #     player2.DEF_dice = 0
                    #     screen.gaming_screen.ui_gaming_data_new(player1, player2)
                    # player2.selected()
                    # screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["Please throw!"], code.SCREEN)
                    # screen.gaming_screen.gaming_throw("AI")
                    # command_fight = random.choice(code.Config["SETTING"]["F_dice"])
                    # screen.gaming_screen.display_statue(code.T["Player 2"] + code.T[command_fight], code.SCREEN)
                    # time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    # command = operation.fight_kill_val(player2.pos[0], player1.pos[0], command_fight, map_pos)
                    # if command >= 0:
                    #     command = command - (player1.DEF_prop + player1.DEF_dice)
                    #     if command > 0:
                    #         player1.HP -= command
                    #         screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["Kill Val is "] + str(command), code.SCREEN)
                    #     else:
                    #         screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["MISS"], code.SCREEN)
                    # elif command == -1:
                    #     player2.HP += 1
                    #     screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["HP Recovery"], code.SCREEN)
                    # elif command == -2:
                    #     player2.DEF_dice += 1
                    #     screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["DEF + 1"], code.SCREEN)
                    # else:
                    #     "fight error"
                    # time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    # if screen.gaming_screen.screen_win(operation.find_winner(player1.HP, player2.HP)):
                    #     break
                    # screen.gaming_screen.ui_gaming_data_new(player1, player2)
                    # player2.selected(False)
            else:
                continue  # error
            code.date_write("-GAMING OVER-", code.DATE_FILE)
        elif command == "course":
            screen.menu.menu_course()
        elif command == "setting":
            screen.menu.menu_setting()
        elif command == "exit":
            pygame.quit()
            sys.exit()
        else:
            continue  # error
