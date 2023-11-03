import sys

import pygame

import init
import code


def change_pos(pos, center_pos=False):
    if type(pos) is int:
        x_init = -48 + 53 * (pos % 100)
        y_init = -48 + 53 * (pos // 100)
        pos = (x_init, y_init)
        return pos
    elif type(pos) is tuple:
        x_init = (pos[0] + 52) // 53
        y_init = (pos[1] + 52) // 53
        pos = x_init + 100 * y_init
        if center_pos:
            return change_pos(pos)
        return pos
    else:
        return "error!"


def get_mouse_pos(g_pos=True):
    pygame.event.clear()
    while True:
        for event_move in pygame.event.get():
            if event_move.type == pygame.MOUSEBUTTONDOWN:
                event_move.pos = (event_move.pos[0], event_move.pos[1])
                if g_pos:
                    return change_pos(event_move.pos)
                else:
                    return event_move.pos
            if event_move.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class Operation:
    def __init__(self):
        return

    # 文本显示函数（文本内容，显示位置，字体大小，是否抗锯齿，传入坐标意义-默认为中心点坐标，按钮颜色，字体颜色）
    def text_display(
            self, text, p_pos, size=init.FONT_MID, anti=True, center=True, button_color=None, color=init.BLACK, get_rect=False):
        if button_color:
            text_show = size.render(text, anti, color, button_color)
        else:
            text_show = size.render(text, anti, color)
        text_rect = text_show.get_rect()
        if center:
            text_rect.center = p_pos
        else:
            text_rect.topleft = p_pos
        if not button_color and color != init.WHITE:
            text_show.set_colorkey(init.WHITE)
        init.screen.blit(text_show, text_rect)
        if button_color or get_rect:
            button = ButtonText((change_pos(p_pos), p_pos), text_rect, button_color)
            return button
        return text_rect


O_OPERATE = Operation()


# 进度条
class ProgressBar:
    def __init__(
            self, pos=None, val=None, length=100, width=20, color1=init.RED, color2=init.GRAY, num_display=None,
            background_color=init.WHITE, val_display_multiplier=1):
        self.length = length
        self.color1 = color1
        self.color2 = color2
        self.bg_color = background_color
        self.width = width
        self.pos = pos
        self.val = val
        self.val_display_mul = val_display_multiplier
        self.num_statue = num_display
        self.text_rect = None
        self.operate = Operation()

    def display(self, screen=None, val=None):
        if screen:
            display_screen = screen
        else:
            display_screen = init.screen
        for i in range(0, self.length):
            pygame.draw.rect(display_screen, color=self.color2, rect=(self.pos[0] + i, self.pos[1], 1, self.width))
        if val:
            self.val = val
        for i in range(0, self.val):
            pygame.draw.rect(display_screen, color=self.color1, rect=(self.pos[0] + i, self.pos[1], 1, self.width))
        if self.num_statue[0]:
            if self.text_rect:
                pygame.draw.rect(display_screen, rect=self.text_rect, color=self.bg_color)
            if self.num_statue[0] == "r":
                self.text_rect = self.operate.text_display("%03s" % str(round(self.val * self.val_display_mul, 1)), (
                    self.pos[0] + self.length + 10, self.pos[1] + self.width // 2), color=self.num_statue[1],
                                                           size=init.FONT_SMALL)
            if self.num_statue[0] == "c":
                self.text_rect = screen.operate.text_display("%03s" % str(round(self.val * self.val_display_mul, 1)), (
                    self.pos[0] + self.length // 2, self.pos[1] + self.width // 2), color=self.num_statue[1],
                                                             size=init.FONT_SMALL)
        pygame.display.flip()

    def mouse_get_val(self, mouse_pos):
        if mouse_pos[1] in range(self.pos[1], self.pos[1] + self.width + 1):
            if mouse_pos[0] in range(self.pos[0], self.pos[0] + self.length + 1):
                self.val = mouse_pos[0] - self.pos[0]
                if self.val <= 5:
                    self.val = 0
                elif self.length - self.val <= 5:
                    self.val = self.length
                return True
        return False


class ButtonText:
    def __init__(self, pos=((0, 0), 0), rect=None, tip_color=None):
        self.pos = pos
        self.rect = rect
        self.color = tip_color
        self.tip_color = tip_color

    def change_pos(self, p_pos):
        self.pos = (change_pos(p_pos), p_pos)
        self.rect = (p_pos[0], p_pos[1], self.rect[2], self.rect[3])

    def is_click(self, mouse_p_pos):
        if mouse_p_pos[0] in range(self.rect[0], self.rect[0] + self.rect[2] + 1) and mouse_p_pos[1] in range(
                self.rect[1], self.rect[1] + self.rect[3] + 1):
            self._tip_color()
            return True
        else:
            return False

    def _tip_color(self):
        return


button_box = ButtonText(rect=init.IMG[0].get_rect())


class MessageList:
    def __init__(self):
        self.list_message = []
        self.list_len = 16
        self.list_message_rect = []
        for i in range(self.list_len):
            self.list_message.append("")

    def append_list(self, text):
        self.list_message.append(text)
        code.date_write(text, code.DATE_FILE)
        del self.list_message[0]


MESSAGE_LIST = MessageList()
