import sys

import pygame
import datetime
import json

f = open("config.json", mode="r")
content = f.read()
Config = json.loads(content)
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("ChessGame Ver0.05")  # 窗口标题显示
SCREEN = pygame.display.set_mode((1060, 636))  # 设置游戏窗口大小：530*636（像素）
icon = pygame.image.load(Config["IMG"]["icon"]).convert()  # 引入窗口图标
pygame.display.set_icon(icon)  # 显示窗口坐标

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (155, 155, 155)
RED = (255, 0, 0)
GRAY_BG = (191, 191, 191)

CLOCK = pygame.time.Clock()


def create_date_file(file):
    if file:
        date_file = "log/%s-%s-%s-%s.txt" % (datetime.date.today(), datetime.datetime.now().hour,
                                             datetime.datetime.now().minute, datetime.datetime.now().second)
        return date_file
    else:
        return


DATE_FILE = create_date_file(False)


def date_write(text, file):
    try:
        with open(file, mode='a') as gaming_log:
            gaming_log.write(str(pygame.time.get_ticks()) + ":" + text + "\n")
        del gaming_log
        print(str(pygame.time.get_ticks()) + ":" + text)
    except:
        return


# 坐标转换函数 方框坐标(g_pos)转像素坐标(p_pos)中心点&像素坐标转方框坐标
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


# 获取鼠标位置的方框坐标
def get_mouse_pos(key="none"):
    if key == "none":
        while True:
            event_move = pygame.event.wait()
            if event_move.type == pygame.MOUSEBUTTONDOWN:
                event_move.pos = (event_move.pos[0], event_move.pos[1])
                return change_pos(event_move.pos)
            if event_move.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    if key == "once":
        event_move = pygame.event.wait()
        if event_move.type == pygame.MOUSEBUTTONDOWN:
            event_move.pos = (event_move.pos[0], event_move.pos[1])
            return change_pos(event_move.pos)
        if event_move.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# 游戏初始化
def game_init():
    date_write("-DATE FILE CREATE-", DATE_FILE)
    SCREEN.fill(WHITE)


# 字体
FONT_BIG = pygame.font.SysFont('arial', 30)  # 默认大号字体
FONT_MID = pygame.font.SysFont('arial', 16)  # 默认正常字体
FONT_SMALL = pygame.font.SysFont('arial', 12)  # 默认小号字体

# 通用数据集
IMG = [pygame.image.load(Config["IMG"]["select box"][0]).convert(),
       pygame.image.load(Config["IMG"]["select box"][1]).convert()]

# 游戏速度
SPEED_FAST = {"time1": 0.1, "time2": 0.3, "time3": 0.5, "time4": 0.7, "time5": 3}  # 预设速度-快速
SPEED_MID = {"time1": 0.3, "time2": 0.5, "time3": 0.7, "time4": 1, "time5": 5}  # 预设速度-中速
SPEED_SLOW = {"time1": 0.5, "time2": 0.7, "time3": 1, "time4": 1.5, "time5": 8}  # 预设速度-慢速


# 文本显示函数（文本内容，显示位置，字体大小，是否抗锯齿，传入坐标意义-默认为中心点坐标，按钮颜色，字体颜色）
def text_display(text, pos, size=FONT_MID, anti=True, center=True, button_color=None, color=BLACK):
    if button_color:
        text_show = size.render(text, anti, color, button_color)
    else:
        text_show = size.render(text, anti, color)
    text_rect = text_show.get_rect()
    if center:
        text_rect.center = pos
    else:
        text_rect.topleft = pos
    if not button_color and color != WHITE:
        text_show.set_colorkey(WHITE)
    SCREEN.blit(text_show, text_rect)
    return text_rect


def game_pause():
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


def play_music(music_name):
    effect = pygame.mixer.Sound(Config["SOUND"][music_name])
    effect.set_volume(Config["SETTING"]["game volume"])
    effect.play()
