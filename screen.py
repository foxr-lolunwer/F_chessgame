import json
import os
import random
import sys
import time

import pygame

import code
import init
import map_load
import operation
import smallmodel


class Menu:
    def __init__(self):
        self.background = pygame.image.load(init.Config["IMG"]["background"]).convert()
        self.__setting_list = {"AI difficulty": (0, 0, 0)}
        self.__main_bg = pygame.image.load(init.Config["IMG"]["main menu"]).convert()
        self.load_img = pygame.image.load(init.Config["IMG"]["load"]).convert()
        self.__main_gif = []
        paths = os.listdir(init.Config["IMG"]["main menu gif"])
        for path in paths:
            self.__main_gif.append(pygame.image.load(init.Config["IMG"]["main menu gif"] + "/" + path).convert())
            self.__main_gif[-1].set_colorkey((252, 254, 252))
        self.__main_gif_len = len(self.__main_gif)
        self.__get_setting()
        self.bar_speed = operation.ProgressBar(val=init.Config["SETTING"]["game speed"],
                                               num_display=("r", init.BLACK), val_display_multiplier=0.02)
        self.bar_volume = operation.ProgressBar(val=init.Config["SETTING"]["game volume"],
                                                num_display=("r", init.BLACK))

    def load(self):
        init.screen.blit(self.load_img, (0, 0))
        operation.TextDisplay(init.T["LOADING"], (400, 600)).display()
        pygame.display.flip()
        time.sleep(0.5)

    def menu_main(self):
        gif_count = 0
        gif_p_pos = operation.change_pos(319)
        button_gif = operation.ButtonText(rect=[gif_p_pos[0], gif_p_pos[1], 408, 408])
        button_start, button_course, button_set, button_exit, gif_count = self.__main_menu_display(gif_count, gif_p_pos)
        while True:
            init.CLOCK.tick(10)
            # 鼠标点击相应按钮并执行相应程序
            down_mouse_move_p_pos = operation.get_mouse_pos(g_pos=False)
            if down_mouse_move_p_pos:
                # 开始游戏
                if button_start.is_click(down_mouse_move_p_pos):
                    return "start"
                # 教程
                elif button_course.is_click(down_mouse_move_p_pos):
                    return "course"
                # 设置
                elif button_set.is_click(down_mouse_move_p_pos):
                    return "setting"
                # 离开游戏
                elif button_exit.is_click(down_mouse_move_p_pos):
                    return "exit"
                elif button_gif.is_click(down_mouse_move_p_pos):
                    button_start, button_course, button_set, button_exit, gif_count = self.__main_menu_display(gif_count, gif_p_pos)
                else:
                    continue

    def __main_menu_display(self, gif_count, gif_p_pos):
        init.screen.blit(self.background, (0, 0))
        operation.TextDisplay(init.T["Game Ver"] + init.game_ver, (1277, 26.5), size=init.FONT_SMALL,
                              color=init.RED).display()
        button_start = operation.TextDisplay(init.T["Start Game"], (424, 183.5), color=init.WHITE, get_button_rect=True,
                                             tip=True).display()
        button_course = operation.TextDisplay(init.T["Course"], (424, 291.5), color=init.WHITE, get_button_rect=True,
                                              tip=True).display()
        button_set = operation.TextDisplay(init.T["Setting"], (424, 397.5), color=init.WHITE, get_button_rect=True,
                                           tip=True).display()
        button_exit = operation.TextDisplay(init.T["Exit Game"], (424, 503.5), color=init.WHITE, get_button_rect=True,
                                            tip=True).display()
        init.screen.blit(self.__main_gif[gif_count % self.__main_gif_len], gif_p_pos)
        gif_count += 1
        pygame.display.flip()
        smallmodel.MUSIC.music_continue()
        return button_start, button_course, button_set, button_exit, gif_count

    def menu_start(self):
        button_next_map, button_play, button_exit = self.__change_map()
        while True:
            smallmodel.MUSIC.music_continue()
            down_mouse_pos = operation.get_mouse_pos(False)
            if button_play.is_click(down_mouse_pos):
                init.screen.blit(self.background, (0, 0))
                return True
            elif button_exit.is_click(down_mouse_pos):
                return False
            elif button_next_map.is_click(down_mouse_pos):
                map_load.MAP.map_dict_count += 1
                map_load.MAP.loading_map(map_load.MAP.map_dict[map_load.MAP.map_dict_keys[
                    map_load.MAP.map_dict_count % map_load.MAP.map_dict_len]], map_load.MAP.map_dict_count)
                button_next_map, button_play, button_exit = self.__change_map()
            else:
                continue

    def __change_map(self):
        init.screen.blit(self.background, (0, 0))
        map_img = map_load.MAP.map_img.copy()
        for i in range(1, len(map_load.MAP.person_pos_init) + 1):
            img_person = pygame.image.load(init.Config["IMG"]["person " + str(i)][0]).convert()
            img_person.set_colorkey(init.WHITE)
            map_img.blit(img_person, operation.change_pos(map_load.MAP.person_pos_init[i - 1]))
        map_img.set_colorkey(init.WHITE)
        init.screen.blit(map_img, (50, 50))
        button_next_map = operation.TextDisplay(init.T["Next Map"], operation.change_pos(1305), get_button_rect=True, color=init.WHITE, tip=True).display()
        button_play = operation.TextDisplay(init.T["Play"], operation.change_pos(922), color=init.WHITE, get_button_rect=True, tip=True).display()
        button_exit = operation.TextDisplay(init.T["Exit"], operation.change_pos(1022), color=init.WHITE, get_button_rect=True, tip=True).display()
        operation.TextDisplay(map_load.MAP.name, operation.change_pos(322), center=True).display()
        operation.TextDisplay(init.T["capacity:"] + str(map_load.MAP.person_capacity), operation.change_pos(420), center=False).display()
        operation.TextDisplay(init.T["number of occ:"] + str(len(map_load.MAP.pos_win)), operation.change_pos(423), center=False).display()
        for i in range(len(map_load.MAP.description)):
            operation.TextDisplay(map_load.MAP.description[i], (1032, 217 + i * 30), center=False).display()
        pygame.display.flip()
        return button_next_map, button_play, button_exit

    def menu_setting(self):
        init.screen.blit(self.background, (0, 0))
        button_set = operation.TextDisplay(init.T["Game Speed"], operation.change_pos(306), color=init.WHITE, bg_color=init.RED).display()
        button_vol = operation.TextDisplay(init.T["Game Music Volume"], operation.change_pos(506), color=init.WHITE, bg_color=init.RED).display()
        button_ai = operation.TextDisplay(init.T["Game AI"], operation.change_pos(706), color=init.WHITE, bg_color=init.RED).display()
        button_en = operation.TextDisplay(init.T["Game Language"], operation.change_pos(906), color=init.WHITE, bg_color=init.RED).display()
        button_se = operation.TextDisplay(init.T["SAVE&EXIT"], operation.change_pos(1520), color=init.WHITE, tip=True).display()
        button_ex = operation.TextDisplay(init.T["EXIT"], operation.change_pos(203), size=init.FONT_BIG, color=init.WHITE, tip=True).display()
        self.__get_setting()
        self.__box_set_difficulty()
        self.bar_speed.pos = operation.change_pos(405)
        self.bar_volume.pos = operation.change_pos(605)
        self.bar_speed.display()
        self.bar_volume.display()
        button_mus = init.screen.blit(init.IMG[init.Config["SETTING"]["music"]], operation.change_pos(608))
        operation.TextDisplay(init.T["music"], (411, 276), size=init.FONT_SMALL).display()
        pygame.display.flip()

        while True:
            smallmodel.MUSIC.music_continue()
            down_mouse_pos = operation.get_mouse_pos(g_pos=False)
            down_mouse_g_pos = operation.change_pos(down_mouse_pos)
            if button_ex.is_click(down_mouse_pos):
                return
            elif self.bar_speed.mouse_get_val(down_mouse_pos):
                if self.bar_speed.val > 99:
                    self.bar_speed.val = 100
                self.bar_speed.display()
                init.Config["SETTING"]["game speed"] = self.bar_speed.val
                continue
            elif self.bar_volume.mouse_get_val(down_mouse_pos):
                self.bar_volume.display()
                init.Config["SETTING"]["game volume"] = self.bar_volume.val
                smallmodel.MUSIC.music_volume_change()
                continue
            elif down_mouse_g_pos == 608:
                init.Config["SETTING"]["music"] = not init.Config["SETTING"]["music"]
                init.screen.blit(init.IMG[init.Config["SETTING"]["music"]], operation.change_pos(608))
                smallmodel.MUSIC.music_volume_change()
                pygame.display.flip()
                continue
            elif down_mouse_g_pos == 805:
                init.Config["SETTING"]["AI Difficulty"]["setting"] = "hard"
                self.__get_setting()
                self.__set_difficulty("fast")
                continue
            elif down_mouse_g_pos == 806:
                init.Config["SETTING"]["AI Difficulty"]["setting"] = "normal"
                self.__get_setting()
                self.__set_difficulty("mid")
                continue
            elif down_mouse_g_pos == 807:
                init.Config["SETTING"]["AI Difficulty"]["setting"] = "easy"
                self.__get_setting()
                self.__set_difficulty("slow")
                continue
            elif button_se.is_click(down_mouse_pos):
                save = json.dumps(init.Config["SETTING"], indent=4)
                with open("config/set.json", "w+") as file:
                    file.write(save)
                operation.TextDisplay(init.T["Saved"], operation.change_pos(1108)).display()
                pygame.display.flip()
                time.sleep(0.5)
                return
            else:
                continue

    def menu_course(self):

        return

    def __set_difficulty(self, val):
        self.__box_set_difficulty()
        code.date_write("setting: AI difficulty " + val, code.DATE_FILE)

    def __box_set_difficulty(self):
        init.screen.blit(init.IMG[self.__setting_list["AI difficulty"][0]], operation.change_pos(805))
        init.screen.blit(init.IMG[self.__setting_list["AI difficulty"][1]], operation.change_pos(806))
        init.screen.blit(init.IMG[self.__setting_list["AI difficulty"][2]], operation.change_pos(807))
        pygame.display.flip()

    def __get_setting(self):
        if init.Config["SETTING"]["AI Difficulty"]["setting"] == "normal":
            self.__setting_list["AI difficulty"] = (0, 1, 0)
        elif init.Config["SETTING"]["AI Difficulty"]["setting"] == "hard":
            self.__setting_list["AI difficulty"] = (1, 0, 0)
        elif init.Config["SETTING"]["AI Difficulty"]["setting"] == "easy":
            self.__setting_list["AI difficulty"] = (0, 0, 1)

    def ui_gaming_data_new(self, per1, per2):
        operation.TextDisplay("%02s" % str(per1.HP), (73, 537), center=False, bg_color=init.GRAY_BG, color=init.RED).display()
        operation.TextDisplay("%02s" % str(per2.HP), (184, 537), center=False, bg_color=init.GRAY_BG, color=init.RED).display()
        operation.TextDisplay("%02s" % str(per1.DEF_dice + per1.DEF_prop), (78, 557), center=False, bg_color=init.GRAY_BG, color=init.RED).display()
        operation.TextDisplay("%02s" % str(per2.DEF_dice + per2.DEF_prop), (189, 557), center=False, bg_color=init.GRAY_BG, color=init.RED).display()
        pygame.display.flip()


MENU = Menu()


class Gaming:
    def __init__(self):
        self.message_list = pygame.image.load(init.Config["IMG"]["message list"])
        self.move_dot_mark = pygame.image.load(init.Config["IMG"]["move dot mark"]).convert()
        self.move_dot_mark.set_colorkey(init.WHITE)
        self.fight_dot_mark = pygame.image.load(init.Config["IMG"]["fight dot mark"]).convert()
        self.fight_dot_mark.set_colorkey(init.WHITE)
        self.__gaming_bottom = pygame.image.load(init.Config["IMG"]["gaming ui bottom"]).convert()
        self.button_rtm = operation.ButtonText()
        self.button_rtm_pos = operation.change_pos(219)
        self.button_thr_pos = operation.change_pos(1220)
        self.message_win_pos = (operation.change_pos(508))
        self.message_turn_pos = (operation.change_pos(223))
        self.message_message_list_start_pos_and_step = ((860, 525), 20)
        self.message_win_list_start_pos_and_step = (operation.change_pos(321), 52)
        self.message_player_name_list_start_pos_and_step = ((43, 487), 106)
        self.message_player_hp_list_start_pos_and_step = ((43, 537), 106)
        self.message_player_def_list_start_pos_and_step = ((43, 557), 106)
        self.data_player_hp_list_start_pos_and_step = ((73, 537), 111)
        self.data_player_def_list_start_pos_and_step = ((78, 557), 111)
        self.display_statue_count = 0

    def ui_gaming_val(self, players):
        init.screen.blit(self.__gaming_bottom, (0, 477))
        for player in players:
            operation.TextDisplay(player.name, (self.message_player_name_list_start_pos_and_step[0][0] + self.message_player_name_list_start_pos_and_step[1] * (player.number - 1), self.message_player_name_list_start_pos_and_step[0][1]), center=False).display()
            operation.TextDisplay(init.T["HP:"], (self.message_player_hp_list_start_pos_and_step[0][0] + self.message_player_hp_list_start_pos_and_step[1] * (player.number - 1), self.message_player_hp_list_start_pos_and_step[0][1]), center=False).display()
            operation.TextDisplay(init.T["DEF:"], (self.message_player_def_list_start_pos_and_step[0][0] + self.message_player_def_list_start_pos_and_step[1] * (player.number - 1), self.message_player_def_list_start_pos_and_step[0][1]), center=False).display()
        operation.TextDisplay(init.T["throw!"], self.button_thr_pos, init.FONT_BIG, bg_color=init.GRAY).display()  # 掷骰子按钮
        self.button_rtm = operation.TextDisplay(init.T["Return to menu"], self.button_rtm_pos, tip=True, color=init.WHITE).display()
        i = 0
        for k in map_load.MAP.list_pos_win_occ.keys():
            operation.TextDisplay("%05s : %02s" % (k, map_load.MAP.list_pos_win_occ[k]), (self.message_win_list_start_pos_and_step[0][0], self.message_win_list_start_pos_and_step[0][1] + i * self.message_win_list_start_pos_and_step[1]), color=init.RED, center=False).display()
            i += 1
        pygame.display.flip()

    def ui_gaming_data_new(self, players):
        init.screen.blit(self.__gaming_bottom, (0, 477))
        for player in players:
            operation.TextDisplay(player.name, (self.message_player_name_list_start_pos_and_step[0][0] + self.message_player_name_list_start_pos_and_step[1] * (player.number - 1), self.message_player_name_list_start_pos_and_step[0][1]), center=False).display()
            operation.TextDisplay(init.T["HP:"], (self.message_player_hp_list_start_pos_and_step[0][0] + self.message_player_hp_list_start_pos_and_step[1] * (player.number - 1), self.message_player_hp_list_start_pos_and_step[0][1]), center=False).display()
            operation.TextDisplay(init.T["DEF:"], (self.message_player_def_list_start_pos_and_step[0][0] + self.message_player_def_list_start_pos_and_step[1] * (player.number - 1), self.message_player_def_list_start_pos_and_step[0][1]), center=False).display()
        for player in players:
            operation.TextDisplay("%02s" % str(player.HP), (self.data_player_hp_list_start_pos_and_step[0][0] + self.data_player_hp_list_start_pos_and_step[1] * (player.number - 1), self.data_player_hp_list_start_pos_and_step[0][1]), center=False, color=init.RED).display()
            operation.TextDisplay("%02s" % str(player.DEF_dice + player.DEF_prop), (self.data_player_def_list_start_pos_and_step[0][0] + self.data_player_def_list_start_pos_and_step[1] * (player.number - 1), self.data_player_def_list_start_pos_and_step[0][1]), center=False, color=init.RED).display()
        pygame.display.flip()

    def start_init(self, occ_dict=None):
        init.screen.blit(map_load.MAP.map_img, (0, 0))
        if occ_dict:
            for i in occ_dict.keys():
                occ_dict[i] = ""
        pygame.display.flip()

    def flip_screen(self, players, count):
        init.screen.blit(map_load.MAP.map_img, (0, 0))
        for player in players:
            init.screen.blit(player.img[0], player.pos[1])
        operation.TextDisplay(init.T["Turn"] + "%03d" % count, self.message_turn_pos).display()
        pygame.display.flip()
        i = 0
        for k in map_load.MAP.list_pos_win_occ.keys():
            operation.TextDisplay("%05s : %08s" % (k, map_load.MAP.list_pos_win_occ[k]), (self.message_win_list_start_pos_and_step[0][0], self.message_win_list_start_pos_and_step[0][1] + i * self.message_win_list_start_pos_and_step[1]), init.FONT_MID, color=init.RED, center=False).display()
            i += 1
        pygame.display.flip()

    def display_red_dot(self, g_pos, dot_type):
        if dot_type == "m":
            image_dot = self.move_dot_mark
            correct = (5, 0)
        elif dot_type == "f":
            image_dot = self.fight_dot_mark
            correct = (0, 0)
        else:
            return  # error
        if g_pos:
            for i in g_pos:
                p_pos = operation.change_pos(i)
                init.screen.blit(image_dot, (p_pos[0] + correct[0], p_pos[1] + correct[1]))
        pygame.display.flip()

    def gaming_throw(self, AI=None):
        if AI:
            time.sleep(0.5)
            return
        button_thr = operation.TextDisplay(init.T["throw!"], self.button_thr_pos, init.FONT_BIG, bg_color=init.RED, center=True).display()
        pygame.display.flip()
        pygame.event.clear()
        while True:
            smallmodel.MUSIC.music_continue()
            init.CLOCK.tick(10)
            event = pygame.event.wait()
            if event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                event.pos = (event.pos[0], event.pos[1])
                if button_thr.is_click(event.pos):
                    operation.TextDisplay(init.T["throw!"], self.button_thr_pos, init.FONT_BIG, bg_color=init.GRAY, center=True).display()
                    pygame.display.flip()
                    break
                if self.button_rtm.is_click(event.pos):
                    return "return"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    operation.TextDisplay(init.T["throw!"], self.button_thr_pos, init.FONT_BIG, bg_color=init.GRAY, center=True).display()
                    pygame.display.flip()
                    break
        return None

    def move_click(self, list_pos, AI=None):
        if not list_pos:
            return None
        if AI:
            pos = random.choice(list_pos)
            pos = (pos, operation.change_pos(pos))
            return pos
        while True:
            smallmodel.MUSIC.music_continue()
            down_mouse_move_g_pos = operation.get_mouse_pos()
            if down_mouse_move_g_pos in list_pos:
                pos = (down_mouse_move_g_pos, operation.change_pos(down_mouse_move_g_pos))  # 新位置坐标
                smallmodel.MUSIC.play_effect("move")
                return pos
            elif self.button_rtm.is_click(operation.change_pos(down_mouse_move_g_pos)):
                return "return"
            else:
                continue

    def fight_click(self, hit_players_list, AI=None):
        if not hit_players_list:
            return None  # error
        if AI:
            hit_player = random.choice(hit_players_list)
            return [hit_player]
        smallmodel.MUSIC.music_continue()
        while True:
            down_mouse_move_g_pos = operation.get_mouse_pos()
            for player in hit_players_list:
                if down_mouse_move_g_pos == player.pos[0]:
                    return [player]
                elif self.button_rtm.is_click(operation.change_pos(down_mouse_move_g_pos)):
                    return "return"
                else:
                    continue

    def display_statue(self, text):
        self.display_statue_count += 1
        operation.MESSAGE_LIST.append_list(text)
        init.screen.blit(self.message_list, (855, 205))
        for i in range(1, operation.MESSAGE_LIST.list_len + 1):
            text_rect = operation.TextDisplay(operation.MESSAGE_LIST.list_message[-i], (self.message_message_list_start_pos_and_step[0][0], self.message_message_list_start_pos_and_step[0][1] - self.message_message_list_start_pos_and_step[1] * i), init.FONT_MID, center=False, color=init.RED).display()
            operation.MESSAGE_LIST.list_message_rect.append(text_rect)
            if self.display_statue_count > 1:
                del operation.MESSAGE_LIST.list_message_rect[0]
        pygame.display.flip()

    def screen_win(self, winner):
        if winner:
            operation.TextDisplay(winner.name + " " + init.T["win this game!"], operation.change_pos(515), init.FONT_BIG, bg_color=init.RED, color=init.WHITE).display()
            pygame.display.flip()
            time.sleep(2)
            return "over"
        return None


GAMING = Gaming()
