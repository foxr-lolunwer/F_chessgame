import json
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
        self.__setting_list = {"AI difficulty": (0, 0, 0)}
        self.__main_bg = pygame.image.load(init.Config["IMG"]["main menu"]).convert()
        self.__toget_setting()
        self.bar_speed = operation.ProgressBar(val=init.Config["SETTING"]["game speed"],
                                               num_display=("r", init.BLACK), val_display_multiplier=0.02)
        self.bar_volume = operation.ProgressBar(val=init.Config["SETTING"]["game volume"],
                                                num_display=("r", init.BLACK))

    def menu_main(self):
        init.screen.blit(self.__main_bg, (0, 0))
        operation.O_OPERATE.text_display(init.T["Game Ver"] + init.game_ver, (477, 26.5), size=init.FONT_SMALL,
                                         color=init.RED)
        operation.O_OPERATE.text_display(init.T["Start Game"], (424, 183.5), color=init.WHITE)
        operation.O_OPERATE.text_display(init.T["Course"], (424, 291.5), color=init.WHITE)
        operation.O_OPERATE.text_display(init.T["Setting"], (424, 397.5), color=init.WHITE)
        operation.O_OPERATE.text_display(init.T["Exit Game"], (424, 503.5), color=init.WHITE)
        pygame.display.flip()
        while True:
            smallmodel.MUSIC.music_continue()
            # 鼠标点击相应按钮并执行相应程序
            down_mouse_move_g_pos = operation.get_mouse_pos()
            # 开始游戏
            if down_mouse_move_g_pos in [407, 408, 409]:
                return "start"
            # 教程
            elif down_mouse_move_g_pos in [607, 608, 609]:
                return "course"
            # 设置
            elif down_mouse_move_g_pos in [807, 808, 809]:
                return "setting"
            # 离开游戏
            elif down_mouse_move_g_pos in [1007, 1008, 1009]:
                return "exit"
            else:
                continue

    def menu_start(self):
        init.screen.fill(init.WHITE)
        map_img = map_load.MAP.map_img.copy()
        for i in range(1, len(map_load.MAP.person_pos_init) + 1):
            img_person = pygame.image.load(init.Config["IMG"]["person " + str(i % 2 + 1)][0]).convert()
            img_person.set_colorkey(init.WHITE)
            map_img.blit(img_person, operation.change_pos(map_load.MAP.person_pos_init[i - 1]))
        init.screen.blit(map_img, (50, 50))
        button_play = operation.O_OPERATE.text_display(init.T["Play"], operation.change_pos(913), color=init.WHITE,
                                                       button_color=init.RED)
        button_exit = operation.O_OPERATE.text_display(init.T["Exit"], operation.change_pos(1013), color=init.WHITE,
                                                       button_color=init.RED)
        operation.O_OPERATE.text_display(map_load.MAP.name, operation.change_pos(314), center=True)
        operation.O_OPERATE.text_display(init.T["capacity:"] + str(map_load.MAP.person_capacity),
                                         operation.change_pos(413), center=False)
        operation.O_OPERATE.text_display(init.T["number of occ:"] + str(len(map_load.MAP.pos_win)),
                                         operation.change_pos(416), center=False)
        for i in range(len(map_load.MAP.description)):
            operation.O_OPERATE.text_display(map_load.MAP.description[i], (641, 217 + i * 30), center=False)
        pygame.display.flip()
        while True:
            smallmodel.MUSIC.music_continue()
            down_mouse_pos = operation.get_mouse_pos(False)
            if button_play.is_click(down_mouse_pos):
                init.screen.fill(init.WHITE)
                return True
            elif button_exit.is_click(down_mouse_pos):
                return False
            else:
                continue

    def menu_setting(self):
        init.screen.fill(init.WHITE)
        button_set = operation.O_OPERATE.text_display(init.T["Game Speed"], operation.change_pos(306), color=init.WHITE,
                                                      button_color=init.RED)
        button_vol = operation.O_OPERATE.text_display(init.T["Game Music Volume"], operation.change_pos(506),
                                                      color=init.WHITE, button_color=init.RED)
        button_ai = operation.O_OPERATE.text_display(init.T["Game AI"], operation.change_pos(706), color=init.WHITE,
                                                     button_color=init.RED)
        button_en = operation.O_OPERATE.text_display(init.T["Game Language"], operation.change_pos(906),
                                                     color=init.WHITE,
                                                     button_color=init.RED)
        button_se = operation.O_OPERATE.text_display(init.T["SAVE&EXIT"], operation.change_pos(1108), color=init.WHITE,
                                                     button_color=init.RED)
        button_ex = operation.O_OPERATE.text_display(init.T["EXIT"], operation.change_pos(202), size=init.FONT_BIG,
                                                     color=init.WHITE, button_color=init.RED)
        self.__toget_setting()
        self.__box_set_difficulty()
        self.bar_speed.pos = operation.change_pos(405)
        self.bar_volume.pos = operation.change_pos(605)
        self.bar_speed.display()
        self.bar_volume.display()
        button_mus = init.screen.blit(init.IMG[init.Config["SETTING"]["music"]], operation.change_pos(608))
        operation.O_OPERATE.text_display(init.T["music"], (411, 276), size=init.FONT_SMALL)
        pygame.display.flip()

        while True:
            smallmodel.MUSIC.music_continue()
            down_mouse_pos = operation.get_mouse_pos(g_pos=False)
            down_mouse_g_pos = operation.change_pos(down_mouse_pos)
            if button_ex.is_click(down_mouse_pos):
                return
            elif self.bar_speed.mouse_get_val(down_mouse_pos):
                if self.bar_speed.val > 90:
                    self.bar_speed.val = 90
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
                print(init.Config["SETTING"]["music"])
                init.screen.blit(init.IMG[init.Config["SETTING"]["music"]], operation.change_pos(608))
                smallmodel.MUSIC.music_volume_change()
                pygame.display.flip()
                continue
            elif down_mouse_g_pos == 805:
                init.Config["SETTING"]["AI Difficulty"]["setting"] = "hard"
                self.__toget_setting()
                self.__set_difficulty("fast")
                continue
            elif down_mouse_g_pos == 806:
                init.Config["SETTING"]["AI Difficulty"]["setting"] = "normal"
                self.__toget_setting()
                self.__set_difficulty("mid")
                continue
            elif down_mouse_g_pos == 807:
                init.Config["SETTING"]["AI Difficulty"]["setting"] = "easy"
                self.__toget_setting()
                self.__set_difficulty("slow")
                continue
            # elif down_mouse_g_pos == 1005:
            #     init.Config["SETTING"]["AI Difficulty"]["setting"] = "hard"
            #     self.__toget_setting()
            #     self.__set_difficulty("fast")
            #     continue
            # elif down_mouse_g_pos == 1006:
            #     init.Config["SETTING"]["AI Difficulty"]["setting"] = "normal"
            #     self.__toget_setting()
            #     self.__set_difficulty("mid")
            #     continue
            # elif down_mouse_g_pos == 1007:
            #     init.Config["SETTING"]["AI Difficulty"]["setting"] = "easy"
            #     self.__toget_setting()
            #     self.__set_difficulty("slow")
            #     continue
            elif button_se.is_click(down_mouse_pos):
                save = json.dumps(init.Config["SETTING"], indent=4)
                with open("config/set.json", "w+") as file:
                    file.write(save)
                operation.O_OPERATE.text_display(init.T["Saved"], operation.change_pos(1108))
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

    def __toget_setting(self):
        if init.Config["SETTING"]["AI Difficulty"]["setting"] == "normal":
            self.__setting_list["AI difficulty"] = (0, 1, 0)
        elif init.Config["SETTING"]["AI Difficulty"]["setting"] == "hard":
            self.__setting_list["AI difficulty"] = (1, 0, 0)
        elif init.Config["SETTING"]["AI Difficulty"]["setting"] == "easy":
            self.__setting_list["AI difficulty"] = (0, 0, 1)

    def ui_gaming_data_new(self, per1, per2):
        operation.O_OPERATE.text_display("%02s" % str(per1.HP), (73, 537), center=False, button_color=init.GRAY_BG,
                                         color=init.RED)
        operation.O_OPERATE.text_display("%02s" % str(per2.HP), (184, 537), center=False,
                                         button_color=init.GRAY_BG,
                                         color=init.RED)
        operation.O_OPERATE.text_display("%02s" % str(per1.DEF_dice + per1.DEF_prop), (78, 557), center=False,
                                         button_color=init.GRAY_BG, color=init.RED)
        operation.O_OPERATE.text_display("%02s" % str(per2.DEF_dice + per2.DEF_prop), (189, 557), center=False,
                                         button_color=init.GRAY_BG, color=init.RED)
        pygame.display.flip()


MENU = Menu()


# def ui_gaming_turn(count):
#     operation.O_OPERATE.text_display(init.T["Turn"] + "%03d" % count, (50, 30), button_color=init.WHITE)
#     pygame.display.flip()


# class MessageList:
#     def __init__(self):
#         self.list_message = []
#         self.list_len = 16
#         self.list_message_rect = []
#         for i in range(self.list_len):
#             self.list_message.append("")
# 
#     def append_list(self, text):
#         self.list_message.append(text)
#         operation.date_write(text, operation.DATE_FILE)
#         del self.list_message[0]
#
class Gaming:
    def __init__(self):
        self.red_dot_mark = pygame.image.load(init.Config["IMG"]["select mark"]).convert()
        self.red_dot_mark.set_colorkey(init.WHITE)
        self.__gaming_bottom = pygame.image.load(init.Config["IMG"]["gaming ui bottom"]).convert()
        self.button_rtm = operation.ButtonText()
        self.display_statue_count = 0

    def ui_gaming_val(self, players):
        init.screen.blit(self.__gaming_bottom, (0, 477))
        for player in players:
            operation.O_OPERATE.text_display(player.name, (43 + 106 * (player.number - 1), 487), center=False)
            operation.O_OPERATE.text_display(init.T["HP:"], (43 + 106 * (player.number - 1), 537), center=False)
            operation.O_OPERATE.text_display(init.T["DEF:"], (43 + 106 * (player.number - 1), 557), center=False)
        operation.O_OPERATE.text_display(init.T["throw!"], operation.change_pos(1112), init.FONT_BIG,
                                         button_color=init.GRAY)  # 掷骰子按钮
        self.button_rtm = operation.O_OPERATE.text_display(init.T["Return to menu"], operation.change_pos(219),
                                                           init.FONT_BIG, button_color=init.RED, color=init.WHITE)
        i = 0
        for k in map_load.MAP.list_pos_win_occ.keys():
            operation.O_OPERATE.text_display("%05s : %02s" % (k, map_load.MAP.list_pos_win_occ[k]),
                                             operation.change_pos(211 + i),
                                             color=init.RED, button_color=init.WHITE, center=False)
            i += 100
        pygame.display.flip()

    def ui_gaming_data_new(self, players):
        for player in players:
            operation.O_OPERATE.text_display("%02s" % str(player.HP), (73 + 111 * (player.number - 1), 537),
                                             center=False,
                                             button_color=init.GRAY_BG,
                                             color=init.RED)
            operation.O_OPERATE.text_display("%02s" % str(player.DEF_dice + player.DEF_prop),
                                             (78 + 111 * (player.number - 1), 557), center=False,
                                             button_color=init.GRAY_BG, color=init.RED)
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
        operation.O_OPERATE.text_display(init.T["Turn"] + "%03d" % count, (50, 30), button_color=init.WHITE)
        pygame.display.flip()
        i = 0
        for k in map_load.MAP.list_pos_win_occ.keys():
            operation.O_OPERATE.text_display("%05s : %08s" % (k, map_load.MAP.list_pos_win_occ[k]),
                                             operation.change_pos(211 + i),
                                             init.FONT_MID, color=init.RED, button_color=init.WHITE, center=False)
            i += 100
        pygame.display.flip()

    def display_red_dot(self, g_pos):
        if g_pos:
            for i in g_pos:
                init.screen.blit(self.red_dot_mark, operation.change_pos(i))
        pygame.display.flip()

    def gaming_throw(self, AI=None):
        if AI:
            time.sleep(0.5)
            return
        button_thr = operation.O_OPERATE.text_display(init.T["throw!"], operation.change_pos(1112), init.FONT_BIG,
                                                      button_color=init.RED, center=True)
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
                    operation.O_OPERATE.text_display(init.T["throw!"], operation.change_pos(1112), init.FONT_BIG,
                                                     button_color=init.GRAY,
                                                     center=True)
                    pygame.display.flip()
                    break
                if self.button_rtm.is_click(event.pos):
                    return "return"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    operation.O_OPERATE.text_display(init.T["throw!"], operation.change_pos(1112), init.FONT_BIG,
                                                     button_color=init.GRAY,
                                                     center=True)
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
        for i in range(1, operation.MESSAGE_LIST.list_len + 1):
            if self.display_statue_count > 1:
                pygame.draw.rect(init.screen, init.WHITE, operation.MESSAGE_LIST.list_message_rect[i - 1])
        for i in range(1, operation.MESSAGE_LIST.list_len + 1):
            text_rect = operation.O_OPERATE.text_display(operation.MESSAGE_LIST.list_message[-i], (747, 535 - 20 * i),
                                                         init.FONT_MID,
                                                         color=init.GRAY)
            operation.MESSAGE_LIST.list_message_rect.append(text_rect)
            if self.display_statue_count > 1:
                del operation.MESSAGE_LIST.list_message_rect[0]
        pygame.display.flip()

    def screen_win(self, winner):
        if winner:
            operation.O_OPERATE.text_display(winner.name + init.T["win this game!"], operation.change_pos(515),
                                             init.FONT_BIG, button_color=init.RED, color=init.WHITE)
            pygame.display.flip()
            time.sleep(2)
            return "over"
        return None


GAMING = Gaming()
