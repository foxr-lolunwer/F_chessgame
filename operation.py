import sys

import pygame

import init
import code


def change_pos(pos, center_pos=False):
    if type(pos) is int:
        x_init = -48 + 53 * (pos % 100)
        y_init = -48 + 52 * (pos // 100)
        pos = (x_init, y_init)
        return pos
    elif type(pos) is tuple:
        x_init = (pos[0] + 52) // 53
        y_init = (pos[1] + 51) // 52
        pos = x_init + 100 * y_init
        if center_pos:
            return change_pos(pos)
        return pos
    else:
        return "error!"


def get_mouse_pos(g_pos=True, once=False):
    if once:
        pygame.event.clear()
        for event_move in pygame.event.get(eventtype=(pygame.MOUSEBUTTONDOWN, pygame.QUIT)):
            if event_move.type == pygame.MOUSEBUTTONDOWN:
                event_move.pos = (event_move.pos[0], event_move.pos[1])
                if g_pos:
                    return change_pos(event_move.pos)
                else:
                    return event_move.pos
            if event_move.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                return None
    pygame.event.clear()
    while True:
        init.CLOCK.tick(10)
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


class TextDisplay:

    # 文本显示函数（文本内容，显示位置，字体大小，是否抗锯齿，传入坐标意义-默认为中心点坐标，按钮颜色，字体颜色）
    def __init__(self, text, p_pos, size=init.FONT_MID, anti=True, center=True, bg_color=None, color=init.BLACK, get_button_rect=False, tip=False):
        self.tip = tip
        self.pos = (change_pos(p_pos), p_pos)
        self.get_button_rect = get_button_rect
        self.bg_color = bg_color
        if bg_color:
            self.text_show = size.render(text, anti, color, bg_color)
        else:
            self.text_show = size.render(text, anti, color)
        self.text_rect = self.text_show.get_rect()
        if center:
            self.text_rect.center = p_pos
        else:
            self.text_rect.topleft = p_pos
        if not bg_color and color != init.WHITE:
            self.text_show.set_colorkey(init.WHITE)
        if self.tip:
            self.button_text_rect = init.button_rect
            if center:
                self.button_text_rect.center = p_pos
            else:
                self.button_text_rect.topleft = p_pos

    def display(self):
        if self.tip:
            init.screen.blit(init.button_default[0], init.button_rect)
        init.screen.blit(self.text_show, self.text_rect)
        if self.bg_color or self.get_button_rect and not self.tip:
            button = ButtonText(self.pos, self.text_rect, self.tip)
            return button
        elif self.get_button_rect or self.tip:
            button = ButtonText(self.pos, self.button_text_rect, self.tip)
            return button
        return self.text_rect


class ButtonText:
    def __init__(self, pos=((0, 0), 0), rect=None, tip=None):
        if rect is None:
            rect = [0, 0, 0, 0]
        self.pos = pos
        self.rect = rect.copy()
        self.tip = tip

    def change_pos(self, p_pos):
        self.pos = (change_pos(p_pos), p_pos)
        self.rect = (p_pos[0], p_pos[1], self.rect[2], self.rect[3])

    def is_click(self, mouse_p_pos):
        if mouse_p_pos[0] in range(self.rect[0], self.rect[0] + self.rect[2] + 1) and mouse_p_pos[1] in range(
                self.rect[1], self.rect[1] + self.rect[3] + 1):
            self.__tip_color()
            return True
        else:
            return False

    def __tip_color(self):
        return


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
                text_bar_message = TextDisplay("%03s" % str(round(self.val * self.val_display_mul, 1)), (self.pos[0] + self.length + 10, self.pos[1] + self.width // 2), color=self.num_statue[1], size=init.FONT_SMALL)
                self.text_rect = text_bar_message.display()
            if self.num_statue[0] == "c":
                text_bar_message = TextDisplay("%03s" % str(round(self.val * self.val_display_mul, 1)), (self.pos[0] + self.length // 2, self.pos[1] + self.width // 2), color=self.num_statue[1], size=init.FONT_SMALL)
                self.text_rect = text_bar_message.display()
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
                # while True:
                #     event_bar = pygame.event.get()
                #     for event in event_bar:
                #         if event.type == pygame.MOUSEBUTTONUP:
                #             return True
                #         mouse_pos = event.pos
                #         if mouse_pos[1] in range(self.pos[1], self.pos[1] + self.width + 1):
                #             if mouse_pos[0] in range(self.pos[0], self.pos[0] + self.length + 1):
                #                 self.val = mouse_pos[0] - self.pos[0]
                #                 if self.val <= 5:
                #                     self.val = 0
                #                 elif self.length - self.val <= 5:
                #                     self.val = self.length
        return False


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
