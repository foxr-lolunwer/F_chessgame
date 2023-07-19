import time

import pygame

import code

LOAD_IMG = pygame.image.load(code.Config["IMG"]["load"]).convert()


def load():
    code.SCREEN.fill(code.WHITE)
    code.SCREEN.blit(LOAD_IMG, (130, 100))
    code.text_display("LOADING", (400, 600))
    pygame.display.flip()
    time.sleep(0.5)


class Menu:
    def __init__(self):
        self.__setting_list = {"game speed": (0, 0, 0), "game volume": 0}
        self.__main_bg = pygame.image.load(code.Config["IMG"]["main menu"]).convert()
        self.__to_setting()

    def menu_main(self):
        code.SCREEN.blit(self.__main_bg, (0, 0))
        code.text_display("Game Ver: 0.02", (477, 26.5), color=code.RED)
        code.text_display("Start Game", (424, 183.5), color=code.WHITE)
        code.text_display("Course", (424, 291.5), color=code.WHITE)
        code.text_display("Setting", (424, 397.5), color=code.WHITE)
        code.text_display("Exit Game", (424, 503.5), color=code.WHITE)
        pygame.display.flip()
        code.date_write("-MAIN MENU INIT DONE-", code.DATE_FILE)
        while True:
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
        code.text_display("PVP", code.change_pos(306), color=code.WHITE, button_color=code.RED)
        code.text_display("PVE", code.change_pos(506), color=code.WHITE, button_color=code.RED)
        pygame.display.flip()
        while True:
            down_mouse_g_pos = code.get_mouse_pos()
            if down_mouse_g_pos == 306:
                return "PVP"
            elif down_mouse_g_pos == 506:
                return "PVE"
            else:
                continue

    def menu_setting(self):
        code.SCREEN.fill(code.WHITE)
        code.text_display("Game Speed:", code.change_pos(306), color=code.WHITE, button_color=code.RED)
        code.text_display("Game Music Volume:", code.change_pos(506), color=code.WHITE, button_color=code.RED)
        code.text_display("Game AI:", code.change_pos(706), color=code.WHITE, button_color=code.RED)
        code.text_display("EXIT", code.change_pos(202), size=code.FONT_BIG, color=code.WHITE, button_color=code.RED)
        self.__box_set_speeed()
        pygame.display.flip()

        code.date_write("-SETTING MENU DONE-", code.DATE_FILE)

        while True:
            down_mouse_g_pos = code.get_mouse_pos()
            if down_mouse_g_pos == 202:
                return
            elif down_mouse_g_pos == 405:
                code.Config["SETTING"]["game speed"] = "fast"
                self.__set_speed("fast")
                continue
            elif down_mouse_g_pos == 406:
                code.Config["SETTING"]["game speed"] = "mid"
                self.__set_speed("mid")
                continue
            elif down_mouse_g_pos == 407:
                code.Config["SETTING"]["game speed"] = "slow"
                self.__set_speed("slow")
                continue
            else:
                continue

    def menu_course(self):
        return

    def __set_speed(self, val):
        self.__to_setting()
        self.__box_set_speeed()
        code.date_write("setting: game speed " + val, code.DATE_FILE)

    def __box_set_speeed(self):
        code.SCREEN.blit(code.IMG[self.__setting_list["game speed"][0]], code.change_pos(405))
        code.SCREEN.blit(code.IMG[self.__setting_list["game speed"][1]], code.change_pos(406))
        code.SCREEN.blit(code.IMG[self.__setting_list["game speed"][2]], code.change_pos(407))
        pygame.display.flip()

    def __to_setting(self):
        if code.Config["SETTING"]["game speed"] == "mid":
            self.__setting_list["game speed"] = (0, 1, 0)
        elif code.Config["SETTING"]["game speed"] == "fast":
            self.__setting_list["game speed"] = (1, 0, 0)
        elif code.Config["SETTING"]["game speed"] == "slow":
            self.__setting_list["game speed"] = (0, 0, 1)
        else:  # error
            self.__setting_list["game speed"] = (0, 1, 0)


class UI:
    def __init__(self):
        self.__gaming_bottom = pygame.image.load(code.Config["IMG"]["gaming ui bottom"]).convert()

    def ui_gaming_bottom(self):
        code.SCREEN.blit(self.__gaming_bottom, (0, 477))
        code.text_display("Player 1", (43, 487), code.FONT_BIG, center=False)
        code.text_display("HP:", (43, 537), center=False)
        code.text_display("DEF:", (43, 557), center=False)
        code.text_display("Player 2", (149, 487), code.FONT_BIG, center=False)
        code.text_display("HP:", (149, 537), center=False)
        code.text_display("DEF:", (149, 557), center=False)
        code.text_display("throw!", code.change_pos(118), code.FONT_BIG, button_color=code.WHITE, center=False)  # 掷骰子按钮
        pygame.display.flip()


    def ui_gaming_bottom_new(self, per1, per2):
        code.text_display("%02s" % str(per1.HP), (73, 537), center=False, button_color=code.GRAY_BG, color=code.RED)
        code.text_display("%02s" % str(per2.HP), (184, 537), center=False, button_color=code.GRAY_BG, color=code.RED)
        code.text_display("%02s" % str(per1.DEF_dice + per1.DEF_prop), (78, 557), center=False, button_color=code.GRAY_BG, color=code.RED)
        code.text_display("%02s" % str(per2.DEF_dice + per2.DEF_prop), (189, 557), center=False, button_color=code.GRAY_BG, color=code.RED)
        pygame.display.flip()


def ui_gaming_turn(count):
    code.text_display("Turn %03d" % count, (50, 30), button_color=code.WHITE)
    pygame.display.flip()


class Gaming:
    def __init__(self):
        self.__list_gaming_val = {"p1 HP": [5, (75, 546)], "p2 HP": [5, (181, 546)],
                                  "p1 DEF": [0, (82, 557)], "p2 DEF": [0, (188, 557)]}
        self.map = code.Config["MAP"]["map 1"]
        self.__map_img = pygame.image.load(self.map["img"]).convert()
        self.red_dot_mark = pygame.image.load(code.Config["IMG"]["select mark"]).convert()
        self.red_dot_mark.set_colorkey(code.WHITE)

    def start_init(self):
        code.SCREEN.blit(self.__map_img, (0, 0))
        pygame.display.flip()

    def __val_check(self):
        if self.__list_gaming_val["p1 HP"][0] not in range(0, 10):
            self.__list_gaming_val["p1 HP"][0] = 9
        if self.__list_gaming_val["p2 HP"][0] not in range(0, 10):
            self.__list_gaming_val["p2 HP"][0] = 9

    def new_val(self):
        self.__val_check()
        return

    def change_val(self, num_val=None, type_val=None):
        if num_val and type_val:
            code.text_display(num_val, self.__list_gaming_val[type_val][1])
        else:
            self.new_val()

    def flip_screen(self, person1, person2, count):
        code.SCREEN.blit(self.__map_img, (0, 0))
        code.SCREEN.blit(person1.img[0], person1.pos[1])
        code.SCREEN.blit(person2.img[0], person2.pos[1])
        ui_gaming_turn(count)
        pygame.display.flip()

    def display_move_red_dot(self, g_pos):
        if g_pos:
            for i in g_pos:
                code.SCREEN.blit(self.red_dot_mark, code.change_pos(i))
        pygame.display.flip()

    def display_statue_text_new(self, this_text):
        code.text_display("")
