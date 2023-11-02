import random

import code
import person


class Turn:
    def __init__(self, screen, gaming_screen, game_map):
        self.players = []
        self.screen = screen
        self.gaming_screen = gaming_screen
        self.game_map = game_map
        self.n = self.game_map.person_capacity
        # 创建角色
        for i in range(self.n):
            self.players.append(person.Person(self.screen, i, self.game_map.person_pos_init[i]))
        self.turn = True
        self.count = 1
        # 开始回合
        code.date_write("-GAMING INIT DONE-", code.DATE_FILE)

    def turn_pvp(self):
        self.gaming_screen.start_init(occ_dict=self.game_map.list_pos_win_occ)
        self.gaming_screen.flip_screen(self.players, self.count, self.game_map.list_pos_win_occ)
        self.gaming_screen.ui_gaming_val(self.game_map.list_pos_win_occ)
        self.gaming_screen.ui_gaming_data_new(self.players)
        while self.turn:
            for i in range(self.n):
                other_players = self.players
                del other_players[i]
                self.__turn_move(self.players[i], other_players)
            # for i in range(self.n):
            #     other_players = self.players
            #     del other_players[i]
            #     self.__turn_fight(self.players[i], other_players)
        return False

    def turn_pve(self):
        self.gaming_screen.start_init(occ_dict=self.game_map.list_pos_win_occ)
        self.gaming_screen.flip_screen(self.players, self.count, self.game_map.list_pos_win_occ)
        self.gaming_screen.ui_gaming_val(self.game_map.list_pos_win_occ)
        self.gaming_screen.ui_gaming_data_new(self.players)

        return False

    def __turn_move(self, player, other_players):
        other_players_pos0 = [p.pos[0] for p in other_players]
        player.selected()
        self.gaming_screen.display_statue(player.name + code.T["Please throw!"], self.screen)
        if self.gaming_screen.gaming_throw():
            return
        t_command_move = random.choice(code.Config["SETTING"]["M_dice"])
        self.gaming_screen.display_statue(player.name + code.T[t_command_move], self.screen)
        t_command = move_person_pos(player.pos[0], other_players_pos0, t_command_move, self.game_map.pos)
        self.gaming_screen.display_move_red_dot(t_command)
        t_person_pos = move_click(t_command)
        if t_person_pos == "return":
            return
        if t_person_pos:
            player.pos = t_person_pos
        player.action_move -= 1
        if player.occ_buff(self.game_map.pos):
            self.game_map.list_pos_win_occ[code.map_dict_key_rel(player.pos[0])] = "p" + player.number
        self.gaming_screen.ui_gaming_data_new(player, other_players)
        self.gaming_screen.flip_screen(player, other_players, self.count, self.game_map.list_pos_win_occ)
        if self.gaming_screen.screen_win(find_winner(occ_dict=self.game_map.list_pos_win_occ)):
            return
        if player.action_move > 0:
            player.selected()
            t_command = move_person_pos(player.pos[0], other_players_pos0, t_command_move, self.game_map.pos)
            self.gaming_screen.display_move_red_dot(t_command)
            t_person_pos = move_click(t_command)
        if t_person_pos == "return":
            return
        if t_person_pos:
            player.pos = t_person_pos
        player.action_move -= 1
        if player.occ_buff(self.game_map.pos):
            self.game_map.list_pos_win_occ[code.map_dict_key_rel(player.pos[0])] = "p" + player.number
        self.gaming_screen.ui_gaming_data_new(player, other_players)
        self.gaming_screen.flip_screen(player, other_players, self.count, self.game_map.list_pos_win_occ)
        if self.gaming_screen.screen_win(find_winner(occ_dict=self.game_map.list_pos_win_occ)):
            return
        return

    # def __turn_fight(self, player, other_players):
    #     other_players_pos0 = [p.pos[0] for p in other_players]
    #     other_players_hp = [p.HP for p in other_players]
    #     if player.DEF_dice:
    #         player.DEF_dice = 0
    #         self.gaming_screen.ui_gaming_data_new(player, other_players)
    #     player.selected()
    #     self.gaming_screen.display_statue(code.T["Player 1"] + code.T["Please throw!"], self.screen)
    #     if self.gaming_screen.gaming_throw():
    #         return
    #     t_command_fight = random.choice(code.Config["SETTING"]["F_dice"])
    #     self.gaming_screen.display_statue(code.T["Player 1"] + code.T[t_command_fight], self.screen)
    #     time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    #     t_command = fight_kill_val(player.pos[0], other_players_pos0, t_command_fight, self.game_map.pos)
    #     if t_command >= 0:
    #         t_command = t_command - (other_players.DEF_prop + other_players.DEF_dice)
    #         if t_command > 0:
    #             other_players.HP -= t_command
    #             self.gaming_screen.display_statue(code.T["Player 1"] + code.T["Kill Val is "] + str(t_command),
    #                                               self.screen)
    #         else:
    #             self.gaming_screen.display_statue(code.T["Player 1"] + code.T["MISS"], self.screen)
    #     elif t_command == -1:
    #         player.HP += 1
    #         self.gaming_screen.display_statue(code.T["Player 1"] + code.T["HP Recovery"], self.screen)
    #     elif t_command == -2:
    #         player.DEF_dice += 1
    #         self.gaming_screen.display_statue(code.T["Player 1"] + code.T["DEF + 1"], self.screen)
    #     else:
    #         "fight error"
    #     time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    #     if self.gaming_screen.screen_win(find_winner(player.HP, other_players_hp)):
    #         return
    #     self.gaming_screen.ui_gaming_data_new(player, other_players)
    #     player.selected(False)
    #     return


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
        code.play_effect("shot")
        if other_per_g_pos in [per_g_pos, per_g_pos + 1, per_g_pos - 1, per_g_pos + 100, per_g_pos - 100, per_g_pos + 2,
                               per_g_pos - 2, per_g_pos + 200, per_g_pos - 200, per_g_pos + 99, per_g_pos - 99,
                               per_g_pos + 101, per_g_pos - 101]:
            return 1
    elif dice_val == "multiple shots":
        code.play_effect("shot", 1)
        if other_per_g_pos in [per_g_pos, per_g_pos + 1, per_g_pos - 1, per_g_pos + 100, per_g_pos - 100, per_g_pos + 2,
                               per_g_pos - 2, per_g_pos + 200, per_g_pos - 200, per_g_pos + 99, per_g_pos - 99,
                               per_g_pos + 101, per_g_pos - 101]:
            return 2
    elif dice_val == "X explosion":
        code.play_effect("X explosion")
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
        code.play_effect("bomb")
        return 1
    elif dice_val == "life recovery":
        code.play_effect("life recovery")
        return -1
    elif dice_val == "shield":
        code.play_effect("shield")
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
        code.music_continue()
        down_mouse_move_g_pos = code.get_mouse_pos()
        if down_mouse_move_g_pos in list_pos:
            pos = (down_mouse_move_g_pos, code.change_pos(down_mouse_move_g_pos))  # 新位置坐标
            code.play_effect("move")
            return pos
        elif down_mouse_move_g_pos in [218, 219, 220]:
            return "return"
        else:
            continue


def find_winner(player1_hp=None, other_players_hp=None, occ_dict=None, all_player=None):
    # 如果player1生命为零
    if player1_hp <= 0:
        return "p2"
    # 如果player2生命为零
    for other_player_hp in other_players_hp:
        if other_player_hp <= 0:
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
