import json
import sys
import time

import pygame

import code

LOAD_IMG = pygame.image.load(code.Config["IMG"]["load"]).convert()


def load():
    code.SCREEN.fill(code.WHITE)
    code.SCREEN.blit(LOAD_IMG, (130, 100))
    code.text_display(code.T["LOADING"], (400, 600))
    pygame.display.flip()
    time.sleep(0.5)


class Menu:
    def __init__(self):
        self.__setting_list = {"game speed": (0, 0, 0), "game volume": (0, 0, 0), "AI difficulty": (0, 0, 0)}
        self.__main_bg = pygame.image.load(code.Config["IMG"]["main menu"]).convert()
        self.__toget_setting()
        self.bar_speed = code.ProgressBar(val=code.Config["SETTING"]["game speed"], num_display=("r", code.BLACK),
                                          val_display_multiplier=0.02)
        self.bar_volume = code.ProgressBar(val=code.Config["SETTING"]["game volume"], num_display=("r", code.BLACK))

    def menu_main(self):
        code.SCREEN.blit(self.__main_bg, (0, 0))
        code.text_display(code.T["Game Ver: 0.08"], (477, 26.5), size=code.FONT_SMALL, color=code.RED)
        code.text_display(code.T["Start Game"], (424, 183.5), color=code.WHITE)
        code.text_display(code.T["Course"], (424, 291.5), color=code.WHITE)
        code.text_display(code.T["Setting"], (424, 397.5), color=code.WHITE)
        code.text_display(code.T["Exit Game"], (424, 503.5), color=code.WHITE)
        pygame.display.flip()
        while True:
            code.music_continue()
            # 鼠标点击相应按钮并执行相应程序
            down_mouse_move_g_pos = code.get_mouse_pos()
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

    @staticmethod
    def menu_start():
        code.SCREEN.fill(code.WHITE)
        button_pvp = code.text_display(code.T["PVP"], code.change_pos(306), color=code.WHITE, button_color=code.RED)
        button_pve = code.text_display(code.T["PVE"], code.change_pos(506), color=code.WHITE, button_color=code.RED)
        pygame.display.flip()
        while True:
            code.music_continue()
            down_mouse_pos = code.get_mouse_pos(False)
            if button_pvp.is_click(down_mouse_pos):
                return "PVP"
            elif button_pve.is_click(down_mouse_pos):
                return "PVE"
            else:
                continue

    def menu_setting(self):
        code.SCREEN.fill(code.WHITE)
        button_set = code.text_display(code.T["Game Speed:"], code.change_pos(306), color=code.WHITE,
                                       button_color=code.RED)
        button_vol = code.text_display(code.T["Game Music Volume:"], code.change_pos(506), color=code.WHITE,
                                       button_color=code.RED)
        button_ai = code.text_display(code.T["Game AI:"], code.change_pos(706), color=code.WHITE, button_color=code.RED)
        button_se = code.text_display(code.T["SAVE&EXIT:"], code.change_pos(908), color=code.WHITE,
                                      button_color=code.RED)
        button_ex = code.text_display(code.T["EXIT"], code.change_pos(202), size=code.FONT_BIG, color=code.WHITE,
                                      button_color=code.RED)
        self.__toget_setting()
        self.__box_set_difficulty()
        self.bar_speed.pos = code.change_pos(405)
        self.bar_volume.pos = code.change_pos(605)
        self.bar_speed.display()
        self.bar_volume.display()
        button_mus = code.SCREEN.blit(code.IMG[code.Config["SETTING"]["music"]], code.change_pos(608))
        code.text_display(code.T["music"], (411, 276), size=code.FONT_SMALL)
        pygame.display.flip()

        while True:
            code.music_continue()
            down_mouse_pos = code.get_mouse_pos(g_pos=False)
            down_mouse_g_pos = code.change_pos(down_mouse_pos)
            if button_ex.is_click(down_mouse_pos):
                return
            elif self.bar_speed.mouse_get_val(down_mouse_pos):
                if self.bar_speed.val > 90:
                    self.bar_speed.val = 90
                self.bar_speed.display()
                code.Config["SETTING"]["game speed"] = self.bar_speed.val
                continue
            elif self.bar_volume.mouse_get_val(down_mouse_pos):
                self.bar_volume.display()
                code.Config["SETTING"]["game volume"] = self.bar_volume.val
                code.music_volume_change()
                continue
            elif down_mouse_g_pos == 608:
                code.Config["SETTING"]["music"] = not code.Config["SETTING"]["music"]
                print(code.Config["SETTING"]["music"])
                code.SCREEN.blit(code.IMG[code.Config["SETTING"]["music"]], code.change_pos(608))
                code.music_volume_change()
                pygame.display.flip()
                continue
            elif down_mouse_g_pos == 805:
                code.Config["SETTING"]["AI Difficulty"]["setting"] = "hard"
                self.__toget_setting()
                self.__set_difficulty("fast")
                continue
            elif down_mouse_g_pos == 806:
                code.Config["SETTING"]["AI Difficulty"]["setting"] = "normal"
                self.__toget_setting()
                self.__set_difficulty("mid")
                continue
            elif down_mouse_g_pos == 807:
                code.Config["SETTING"]["AI Difficulty"]["setting"] = "easy"
                self.__toget_setting()
                self.__set_difficulty("slow")
                continue
            elif button_se.is_click(down_mouse_pos):
                save = json.dumps(code.Config["SETTING"], indent=4)
                with open("config/set.json", "w+") as file:
                    file.write(save)
                code.text_display(code.T["Saved"], code.change_pos(1108))
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
        code.SCREEN.blit(code.IMG[self.__setting_list["AI difficulty"][0]], code.change_pos(805))
        code.SCREEN.blit(code.IMG[self.__setting_list["AI difficulty"][1]], code.change_pos(806))
        code.SCREEN.blit(code.IMG[self.__setting_list["AI difficulty"][2]], code.change_pos(807))
        pygame.display.flip()

    def __toget_setting(self):
        if code.Config["SETTING"]["AI Difficulty"]["setting"] == "normal":
            self.__setting_list["AI difficulty"] = (0, 1, 0)
        elif code.Config["SETTING"]["AI Difficulty"]["setting"] == "hard":
            self.__setting_list["AI difficulty"] = (1, 0, 0)
        elif code.Config["SETTING"]["AI Difficulty"]["setting"] == "easy":
            self.__setting_list["AI difficulty"] = (0, 0, 1)

    def ui_gaming_data_new(self, per1, per2):
        code.text_display("%02s" % str(per1.HP), (73, 537), center=False, button_color=code.GRAY_BG, color=code.RED)
        code.text_display("%02s" % str(per2.HP), (184, 537), center=False, button_color=code.GRAY_BG, color=code.RED)
        code.text_display("%02s" % str(per1.DEF_dice + per1.DEF_prop), (78, 557), center=False,
                          button_color=code.GRAY_BG, color=code.RED)
        code.text_display("%02s" % str(per2.DEF_dice + per2.DEF_prop), (189, 557), center=False,
                          button_color=code.GRAY_BG, color=code.RED)
        pygame.display.flip()


def ui_gaming_turn(count):
    code.text_display(code.T["Turn"] + "%03d" % count, (50, 30), button_color=code.WHITE)
    pygame.display.flip()


class Gaming:
    def __init__(self):
        self.__list_gaming_val = {"p1 HP": [5, (75, 546)], "p2 HP": [5, (181, 546)],
                                  "p1 DEF": [0, (82, 557)], "p2 DEF": [0, (188, 557)]}
        self.map = code.load_map
        self.__map_img = pygame.image.load(self.map["img"]).convert()
        self.red_dot_mark = pygame.image.load(code.Config["IMG"]["select mark"]).convert()
        self.red_dot_mark.set_colorkey(code.WHITE)
        self.__gaming_bottom = pygame.image.load(code.Config["IMG"]["gaming ui bottom"]).convert()
        self.button_rtm = code.ButtonText()

    def ui_gaming_val(self, occ_dict):
        code.SCREEN.blit(self.__gaming_bottom, (0, 477))
        code.text_display(code.T["Player 1"], (43, 487), code.FONT_BIG, center=False)
        code.text_display(code.T["HP:"], (43, 537), center=False)
        code.text_display(code.T["DEF:"], (43, 557), center=False)
        code.text_display(code.T["Player 2"], (149, 487), code.FONT_BIG, center=False)
        code.text_display(code.T["HP:"], (149, 537), center=False)
        code.text_display(code.T["DEF:"], (149, 557), center=False)
        code.text_display(code.T["throw!"], code.change_pos(1108), code.FONT_BIG, button_color=code.GRAY)  # 掷骰子按钮
        self.button_rtm = code.text_display(code.T["Return to menu"], code.change_pos(219), code.FONT_BIG,
                                            button_color=code.RED, color=code.WHITE)
        i = 0
        for k in occ_dict.keys():
            code.text_display("%05s : %02s" % (k, occ_dict[k]), code.change_pos(211 + i), code.FONT_MID, color=code.RED,
                              button_color=code.WHITE, center=False)
            i += 100
        pygame.display.flip()

    def ui_gaming_data_new(self, per1, per2):
        code.text_display("%02s" % str(per1.HP), (73, 537), center=False, button_color=code.GRAY_BG, color=code.RED)
        code.text_display("%02s" % str(per2.HP), (184, 537), center=False, button_color=code.GRAY_BG, color=code.RED)
        code.text_display("%02s" % str(per1.DEF_dice + per1.DEF_prop), (78, 557), center=False,
                          button_color=code.GRAY_BG, color=code.RED)
        code.text_display("%02s" % str(per2.DEF_dice + per2.DEF_prop), (189, 557), center=False,
                          button_color=code.GRAY_BG, color=code.RED)
        pygame.display.flip()

    def start_init(self, occ_dict=None):
        code.SCREEN.blit(self.__map_img, (0, 0))
        if occ_dict:
            for i in occ_dict.keys():
                occ_dict[i] = ""
        pygame.display.flip()

    def __val_check(self):
        if self.__list_gaming_val["p1 HP"][0] not in range(0, 10):
            self.__list_gaming_val["p1 HP"][0] = 9
        if self.__list_gaming_val["p2 HP"][0] not in range(0, 10):
            self.__list_gaming_val["p2 HP"][0] = 9

    def new_val(self):
        self.__val_check()
        return

    def flip_screen(self, person1, person2, count, occ_dict=None):
        code.SCREEN.blit(self.__map_img, (0, 0))
        code.SCREEN.blit(person1.img[0], person1.pos[1])
        code.SCREEN.blit(person2.img[0], person2.pos[1])
        ui_gaming_turn(count)
        if occ_dict:
            i = 0
            for k in occ_dict.keys():
                code.text_display("%05s : %02s" % (k, occ_dict[k]), code.change_pos(211 + i), code.FONT_MID,
                                  color=code.RED, button_color=code.WHITE, center=False)
                i += 100
        pygame.display.flip()

    def display_move_red_dot(self, g_pos):
        if g_pos:
            for i in g_pos:
                code.SCREEN.blit(self.red_dot_mark, code.change_pos(i))
        pygame.display.flip()

    def gaming_throw(self, AI=None):
        if AI:
            time.sleep(0.5)
            return
        button_thr = code.text_display(code.T["throw!"], code.change_pos(1108), code.FONT_BIG, button_color=code.RED,
                                       center=True)
        pygame.display.flip()
        pygame.event.clear()
        while True:
            code.music_continue()
            code.CLOCK.tick(10)
            event = pygame.event.wait()
            if event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                event.pos = (event.pos[0], event.pos[1])
                if button_thr.is_click(event.pos):
                    code.text_display(code.T["throw!"], code.change_pos(1108), code.FONT_BIG, button_color=code.GRAY,
                                      center=True)
                    pygame.display.flip()
                    break
                if self.button_rtm.is_click(event.pos):
                    return "return"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    code.text_display(code.T["throw!"], code.change_pos(1108), code.FONT_BIG, button_color=code.GRAY,
                                      center=True)
                    pygame.display.flip()
                    break
        return None

    def display_statue(self, text, screen):
        pygame.draw.rect(screen, code.WHITE, (535, 456, 530, 108))
        code.text_display(text, code.change_pos(1115), code.FONT_BIG, color=code.GRAY)
        pygame.display.flip()

    def screen_win(self, winner):
        if winner:
            code.text_display(winner + code.T["win this game!"], code.change_pos(515), code.FONT_BIG,
                              button_color=code.RED,
                              color=code.WHITE)
            pygame.display.flip()
            time.sleep(2)
            return "over"
        return None
