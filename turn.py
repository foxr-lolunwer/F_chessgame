import random
import time

import code
import init

import map_load
import person
import screen
import smallmodel
from operation import change_pos, MESSAGE_LIST


class Turn:
    def __init__(self):
        self.players = []
        self.n = map_load.MAP.person_capacity
        # 创建角色
        for i in range(1, self.n + 1):
            g_pos = map_load.MAP.person_pos_init[i - 1]
            self.players.append(person.Person(init.screen, i, (g_pos, change_pos(g_pos))))
        self.alive_players = [player for player in self.players if player.alive]
        self.turn = True
        self.count = 1
        # 开始回合
        code.date_write("-GAMING INIT DONE-", code.DATE_FILE)

    def turn_pvp(self):
        screen.GAMING.start_init(occ_dict=map_load.MAP.list_pos_win_occ)
        screen.GAMING.flip_screen(self.alive_players, self.count)
        screen.GAMING.ui_gaming_val(self.players)
        screen.GAMING.ui_gaming_data_new(self.alive_players)
        while self.turn:
            for player in self.alive_players:
                player.action_move = 1
                other_players = self.alive_players.copy()
                other_players.remove(player)
                if self.__turn_move(player, other_players):
                    return True
            for player in self.alive_players:
                other_players = self.alive_players.copy()
                other_players.remove(player)
                if self.__turn_fight(player, other_players):
                    return True
        return False

    def turn_pve(self):
        screen.GAMING.start_init(occ_dict=map_load.MAP.list_pos_win_occ)
        screen.GAMING.flip_screen(self.alive_players, self.count)
        screen.GAMING.ui_gaming_val(map_load.MAP.list_pos_win_occ)
        screen.GAMING.ui_gaming_data_new(self.alive_players)

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
            player.selected()
            s_command = self.__move_person_pos(player.pos[0], other_players_g_pos0, t_command_move)
            screen.GAMING.display_red_dot(s_command)
            t_person_pos = screen.GAMING.move_click(s_command)
            if t_person_pos == "return":
                return True
            if t_person_pos:
                player.pos = t_person_pos
            player.action_move -= 1
            player.occ_buff()
            screen.GAMING.ui_gaming_data_new(self.alive_players)
            screen.GAMING.flip_screen(self.alive_players, self.count)
            if screen.GAMING.screen_win(self.__find_winner()):
                return True
        return False

    def __turn_fight(self, player, other_players):
        if player.DEF_dice:
            player.DEF_dice = 0
            screen.GAMING.ui_gaming_data_new(player, other_players)
        player.selected()
        screen.GAMING.display_statue(player.name + init.T["Please throw!"])
        if screen.GAMING.gaming_throw():
            return True
        t_command_fight = random.choice(init.Config["SETTING"]["F_dice"])
        screen.GAMING.display_statue(player.name + init.T[t_command_fight])
        time.sleep((100 - init.Config["SETTING"]["game speed"]) * 0.02 * 1)
        t_command = self.__fight_kill_val(player, other_players, t_command_fight)
        if t_command[1]:
            self.__hit_player(player, t_command[0], t_command[1])
        screen.GAMING.ui_gaming_data_new(self.alive_players)
        if screen.GAMING.screen_win(self.__find_winner()):
            return True
        player.selected(False)
        return False

    def __hit_player(self, player, kill_val, hit_players_list):
        for hit_player in hit_players_list:
            if kill_val >= 0:
                kill_val = kill_val - (hit_player.DEF_prop + hit_player.DEF_dice)
                if kill_val > 0:
                    hit_player.HP -= kill_val
                    screen.GAMING.display_statue(init.T["Player 1"] + init.T["Kill Val is "] + str(kill_val))
                else:
                    screen.GAMING.display_statue(init.T["Player 1"] + init.T["MISS"])
            elif kill_val == -1:
                player.HP += 1
                screen.GAMING.display_statue(init.T["Player 1"] + init.T["HP Recovery"])
            elif kill_val == -2:
                player.DEF_dice += 1
                screen.GAMING.display_statue(init.T["Player 1"] + init.T["DEF + 1"])
            else:
                "fight error"
            time.sleep((100 - init.Config["SETTING"]["game speed"]) * 0.02 * 1)
        return

    # 获取可以移动的所有位置
    def __move_person_pos(self, player_g_pos, other_players_g_pos, dice_val):
        players_g_pos = other_players_g_pos.copy()
        players_g_pos.append(player_g_pos)
        move_available_pos = []
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
            move_available_pos_l = [player_g_pos, player_g_pos + 1, player_g_pos - 1, player_g_pos + 100,
                                    player_g_pos - 100,
                                    player_g_pos + 2, player_g_pos - 2, player_g_pos + 200, player_g_pos - 200,
                                    player_g_pos + 99, player_g_pos - 99, player_g_pos + 101, player_g_pos - 101]
            move_available_pos = [0]
            for i in move_available_pos_l:
                if i in map_load.MAP.pos_available and i not in other_players_g_pos:
                    move_available_pos.append(i)
        if move_available_pos:
            return move_available_pos
        else:
            return None

    def __fight_kill_val(self, fight_player, other_players, dice_val):
        hit_players_list = []
        if dice_val == "single shot":
            smallmodel.MUSIC.play_effect("shot")
            for player in other_players:
                if player.pos[0] in [fight_player.pos[0], fight_player.pos[0] + 1, fight_player.pos[0] - 1,
                                     fight_player.pos[0] + 100, fight_player.pos[0] - 100, fight_player.pos[0] + 2,
                                     fight_player.pos[0] - 2, fight_player.pos[0] + 200, fight_player.pos[0] - 200,
                                     fight_player.pos[0] + 99, fight_player.pos[0] - 99,
                                     fight_player.pos[0] + 101, fight_player.pos[0] - 101]:
                    hit_players_list.append(player)
            hit_players_g_pos_list = [player.pos[0] for player in hit_players_list]
            screen.GAMING.display_red_dot(hit_players_g_pos_list)
            hit_player_list = screen.GAMING.fight_click(hit_players_list)
            return [1, hit_player_list]
        elif dice_val == "multiple shots":
            smallmodel.MUSIC.play_effect("shot", 1)
            for player in other_players:
                if player.pos[0] in [fight_player.pos[0], fight_player.pos[0] + 1, fight_player.pos[0] - 1,
                                     fight_player.pos[0] + 100, fight_player.pos[0] - 100, fight_player.pos[0] + 2,
                                     fight_player.pos[0] - 2, fight_player.pos[0] + 200, fight_player.pos[0] - 200,
                                     fight_player.pos[0] + 99, fight_player.pos[0] - 99, fight_player.pos[0] + 101,
                                     fight_player.pos[0] - 101]:
                    hit_players_list.append(player)
            hit_players_g_pos_list = [player.pos[0] for player in hit_players_list]
            screen.GAMING.display_red_dot(hit_players_g_pos_list)
            hit_player_list = screen.GAMING.fight_click(hit_players_list)
            return [2, hit_player_list]
        elif dice_val == "X explosion":
            smallmodel.MUSIC.play_effect("X explosion")
            fight_pos_l = []
            for i in range(1, 10):
                if fight_player.pos[0] - 101 * i in map_load.MAP.pos_available:
                    fight_pos_l.append(fight_player.pos[0] - 101 * i)
                if fight_player.pos[0] - 99 * i in map_load.MAP.pos_available:
                    fight_pos_l.append(fight_player.pos[0] - 99 * i)
                if fight_player.pos[0] + 99 * i in map_load.MAP.pos_available:
                    fight_pos_l.append(fight_player.pos[0] + 99 * i)
                if fight_player.pos[0] + 101 * i in map_load.MAP.pos_available:
                    fight_pos_l.append(fight_player.pos[0] + 101 * i)
            for player in other_players:
                if player.pos[0] in fight_pos_l:
                    hit_players_list.append(player)
            return [2, hit_players_list]
        elif dice_val == "bomb":
            smallmodel.MUSIC.play_effect("bomb")
            return [1, other_players]
        elif dice_val == "life recovery":
            smallmodel.MUSIC.play_effect("life recovery")
            return [-1, None]
        elif dice_val == "shield":
            smallmodel.MUSIC.play_effect("shield")
            return [-2, None]
        else:
            return [None, None]  # error

    def __find_winner(self):
        self.alive_players = [player for player in self.players if player.alive]
        # 战斗胜利
        for alive_player in self.alive_players:
            if alive_player.HP <= 0:
                alive_player.alive = False
        alive_players = [player for player in self.players if player.alive]
        if len(alive_players) == 1:
            return alive_players[0]
        # 占点胜利
        occ_list = []
        occ_list_key = map_load.MAP.list_pos_win_occ.keys()
        for k in occ_list_key:
            occ_list.append(map_load.MAP.list_pos_win_occ[k])
        for occ in occ_list:
            if occ != occ_list[0]:
                return None
        for alive_player in self.alive_players:
            if alive_player.name == occ_list[0]:
                return alive_player
            else:
                return None  # error

    def clear(self):
        map_load.MAP.__init__()
        self.__init__()
        MESSAGE_LIST.__init__()
        screen.GAMING.__init__()

    def __calculate_distance(self, per1_g_pos0, per2_g_pos0):
        x = abs(per1_g_pos0 // 100 - per2_g_pos0 // 100)
        y = abs(per1_g_pos0 % 100 - per2_g_pos0 % 100)
        return x, y


O_TURN = Turn()
