import random

import code
import init

import map_load
import person
import screen
import smallmodel
from operation import change_pos


class Turn:
    def __init__(self):
        self.players = []
        self.n = map_load.MAP.person_capacity
        # 创建角色
        for i in range(self.n):
            g_pos = map_load.MAP.person_pos_init[i]
            self.players.append(person.Person(init.screen, i, (g_pos, change_pos(g_pos))))
        self.turn = True
        self.count = 1
        # 开始回合
        code.date_write("-GAMING INIT DONE-", code.DATE_FILE)

    def turn_pvp(self):
        screen.GAMING.start_init(occ_dict=map_load.MAP.list_pos_win_occ)
        screen.GAMING.flip_screen(self.players, self.count, map_load.MAP.list_pos_win_occ)
        screen.GAMING.ui_gaming_val(map_load.MAP.list_pos_win_occ)
        screen.GAMING.ui_gaming_data_new(self.players)
        while self.turn:
            for player in self.players:
                player.action_move = 1
                other_players = self.players.copy()
                other_players.remove(player)
                if self.__turn_move(player, other_players):
                    return True
            # for i in range(self.n):
            #     other_players = self.players
            #     del other_players[i]
            #     self.__turn_fight(self.players[i], other_players)
        return False

    def turn_pve(self):
        screen.GAMING.start_init(occ_dict=map_load.MAP.list_pos_win_occ)
        screen.GAMING.flip_screen(self.players, self.count, map_load.MAP.list_pos_win_occ)
        screen.GAMING.ui_gaming_val(map_load.MAP.list_pos_win_occ)
        screen.GAMING.ui_gaming_data_new(self.players)

        return False

    # 返回值为true时返回主菜单
    def __turn_move(self, player, other_players):
        other_players_g_pos0 = [p.pos[0] for p in other_players]
        player.selected()
        screen.GAMING.display_statue(player.name + init.T["Please throw!"])
        if screen.GAMING.gaming_throw():
            return True
        t_command_move = random.choice(init.Config["SETTING"]["M_dice"])
        screen.GAMING.display_statue(player.name + init.T[t_command_move])
        while player.action_move:
            t_command = self.__move_person_pos(player.pos[0], other_players_g_pos0, t_command_move)
            screen.GAMING.display_move_red_dot(t_command)
            t_person_pos = screen.GAMING.move_click(t_command)
            if t_person_pos == "return":
                return True
            if t_person_pos:
                player.pos = t_person_pos
            player.action_move -= 1
            # if player.occ_buff():
            #     map_load.MAP.list_pos_win_occ[map_load.MAP.list_pos_win_rel(player.pos[0])] = "p" + str(player.number)
            screen.GAMING.ui_gaming_data_new(self.players)
            screen.GAMING.flip_screen(self.players, self.count)
            if screen.GAMING.screen_win(self.__find_winner()):
                return False
        return False

    # def __turn_fight(self, player, other_players):
    #     other_players_pos0 = [p.pos[0] for p in other_players]
    #     other_players_hp = [p.HP for p in other_players]
    #     if player.DEF_dice:
    #         player.DEF_dice = 0
    #         screen.GAMING.ui_gaming_data_new(player, other_players)
    #     player.selected()
    #     screen.GAMING.display_statue(code.T["Player 1"] + code.T["Please throw!"])
    #     if screen.GAMING.gaming_throw():
    #         return
    #     t_command_fight = random.choice(code.Config["SETTING"]["F_dice"])
    #     screen.GAMING.display_statue(code.T["Player 1"] + code.T[t_command_fight])
    #     time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    #     t_command = fight_kill_val(player.pos[0], other_players_pos0, t_command_fight, map_load.MAP.pos)
    #     if t_command >= 0:
    #         t_command = t_command - (other_players.DEF_prop + other_players.DEF_dice)
    #         if t_command > 0:
    #             other_players.HP -= t_command
    #             screen.GAMING.display_statue(code.T["Player 1"] + code.T["Kill Val is "] + str(t_command))
    #         else:
    #             screen.GAMING.display_statue(code.T["Player 1"] + code.T["MISS"])
    #     elif t_command == -1:
    #         player.HP += 1
    #         screen.GAMING.display_statue(code.T["Player 1"] + code.T["HP Recovery"])
    #     elif t_command == -2:
    #         player.DEF_dice += 1
    #         screen.GAMING.display_statue(code.T["Player 1"] + code.T["DEF + 1"])
    #     else:
    #         "fight error"
    #     time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    #     if screen.GAMING.screen_win(find_winner(player.HP, other_players_hp)):
    #         return
    #     screen.GAMING.ui_gaming_data_new(player, other_players)
    #     player.selected(False)
    #     return

    # 获取可以移动的所有位置
    def __move_person_pos(self, player_g_pos, other_players_g_pos, dice_val):
        players_g_pos = other_players_g_pos.copy()
        players_g_pos.append(player_g_pos)
        move_available_pos = []
        while True:
            # 十字移动
            if dice_val == "cross":
                move_available_pos_l = [player_g_pos + 1, player_g_pos - 1, player_g_pos + 100, player_g_pos - 100]
                move_available_pos = []
                for i in move_available_pos_l:
                    if i in map_load.MAP.pos_available and i not in players_g_pos:
                        move_available_pos.append(i)
            # 斜线移动
            elif dice_val == "diagonal":
                move_available_pos_l = [player_g_pos + 99, player_g_pos - 99, player_g_pos + 101, player_g_pos - 101]
                move_available_pos = []
                for i in move_available_pos_l:
                    if i in map_load.MAP.pos_available and i not in players_g_pos:
                        move_available_pos.append(i)
            # 传送 ！未完成预定功能
            elif dice_val == "tp":
                move_available_pos_l = map_load.MAP.pos_tp
                move_available_pos = [0]
                for i in move_available_pos_l:
                    if i not in other_players_g_pos:
                        move_available_pos.append(i)
            # 自由移动（十字移动两次）
            elif dice_val == "free":
                move_available_pos_l = [player_g_pos, player_g_pos + 1, player_g_pos - 1, player_g_pos + 100, player_g_pos - 100,
                                        player_g_pos + 2, player_g_pos - 2, player_g_pos + 200, player_g_pos - 200,
                                        player_g_pos + 99, player_g_pos - 99, player_g_pos + 101, player_g_pos - 101]
                move_available_pos = [0]
                for i in move_available_pos_l:
                    if i in map_load.MAP.pos_available and i != other_players_g_pos:
                        move_available_pos.append(i)
            if move_available_pos:
                return move_available_pos
            else:
                return None

    def __fight_kill_val(self, per_g_pos, other_per_g_pos, dice_val, dict_map_pos):
        if dice_val == "single shot":
            smallmodel.MUSIC.play_effect("shot")
            if other_per_g_pos in [per_g_pos, per_g_pos + 1, per_g_pos - 1, per_g_pos + 100, per_g_pos - 100,
                                   per_g_pos + 2,
                                   per_g_pos - 2, per_g_pos + 200, per_g_pos - 200, per_g_pos + 99, per_g_pos - 99,
                                   per_g_pos + 101, per_g_pos - 101]:
                return 1
        elif dice_val == "multiple shots":
            smallmodel.MUSIC.play_effect("shot", 1)
            if other_per_g_pos in [per_g_pos, per_g_pos + 1, per_g_pos - 1, per_g_pos + 100, per_g_pos - 100,
                                   per_g_pos + 2,
                                   per_g_pos - 2, per_g_pos + 200, per_g_pos - 200, per_g_pos + 99, per_g_pos - 99,
                                   per_g_pos + 101, per_g_pos - 101]:
                return 2
        elif dice_val == "X explosion":
            smallmodel.MUSIC.play_effect("X explosion")
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
            smallmodel.MUSIC.play_effect("bomb")
            return 1
        elif dice_val == "life recovery":
            smallmodel.MUSIC.play_effect("life recovery")
            return -1
        elif dice_val == "shield":
            smallmodel.MUSIC.play_effect("shield")
            return -2
        else:
            "fight_kill_val error"
        return 0

    def __find_winner(self, player1_hp=None, other_players_hp=None):
        # # 如果player1生命为零
        # if player1_hp <= 0:
        #     return "p2"
        # # 如果player2生命为零
        # for other_player_hp in other_players_hp:
        #     if other_player_hp <= 0:
        #         return "p1"
        if map_load.MAP.list_pos_win_occ:
            occ_list = []
            for k in map_load.MAP.list_pos_win_occ.keys():
                occ_list.append(map_load.MAP.list_pos_win_occ[k])
            if len(set(occ_list)) == 1 and occ_list[0] != "":
                return occ_list[0]
        return None

    def __calculate_distance(self, per1_g_pos0, per2_g_pos0):
        x = abs(per1_g_pos0 // 100 - per2_g_pos0 // 100)
        y = abs(per1_g_pos0 % 100 - per2_g_pos0 % 100)
        return x, y


O_TURN = Turn()
