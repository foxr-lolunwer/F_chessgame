import os
import random
import sys

import pygame
import datetime
import json


f1 = open("config/set.json", mode="r")
f2 = open("config/img.json", mode="r")
f3 = open("config/sound.json", mode="r")
f4 = open("config/map.json", mode="r")
content1 = f1.read()
content2 = f2.read()
content3 = f3.read()
content4 = f4.read()
f1.close()
f2.close()
f3.close()
f4.close()
# f5 = open("localization/zh-cn.json", mode="r", encoding="utf-8")
# print(f5.read())
with open("localization/en.json", 'r', encoding='utf-8') as f5:
    content = f5.read()

Config = {"SETTING": json.loads(content1), "IMG": json.loads(content2), "SOUND": json.loads(content3), "MAP": json.loads(content4)}
T = json.loads(content)
# f5.close()
del content4, content3, content2, content1

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("ChessGame Ver0.05")  # 窗口标题显示10
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


# 游戏初始化
def game_init():
    date_write("-DATE FILE CREATE-", DATE_FILE)
    SCREEN.fill(WHITE)


# 字体
FONT_BIG = pygame.font.SysFont('SimHei', 30)  # 默认大号字体
FONT_MID = pygame.font.SysFont('SimHei', 16)  # 默认正常字体
FONT_SMALL = pygame.font.SysFont('SimHei', 12)  # 默认小号字体

# 通用数据集
IMG = [pygame.image.load(Config["IMG"]["select box"][0]).convert(),
       pygame.image.load(Config["IMG"]["select box"][1]).convert()]


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


def play_effect(music_name, count=0):
    effect = pygame.mixer.Sound(Config["SOUND"][music_name])
    effect.set_volume(Config["SETTING"]["game volume"] * 0.004)
    effect.play(loops=count)


path = "resource/sound/music"
root, dirs, music_files = list(os.walk(path))[0]


def play_music():
    pygame.mixer.music.load("resource/sound/music/" + random.choice(music_files))
    pygame.mixer.music.set_volume(Config["SETTING"]["game volume"] * 0.001)
    if not Config["SETTING"]["music"]:
        pygame.mixer.music.stop()
        return
    pygame.mixer.music.play()


def music_volume_change():
    # 如果音乐停止，随机播放下一首
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("resource/sound/music/" + random.choice(music_files))
        pygame.mixer.music.play()
    pygame.mixer.music.pause()
    if Config["SETTING"]["game volume"] * 0.004 == 0:
        return
    if not Config["SETTING"]["music"]:
        pygame.mixer.music.stop()
        return
    pygame.mixer.music.set_volume(Config["SETTING"]["game volume"] * 0.01)
    pygame.mixer.music.unpause()


# 加载地图
def load_map(load_map_name=Config["MAP"]["default map"]):
    map_load = Config["MAP"][load_map_name]
    return map_load


load_map = load_map()


def music_continue():
    # 如果音乐停止并且音量不为零，并开启了音乐，随机播放下一首
    if not pygame.mixer.music.get_busy() and Config["SETTING"]["game volume"] * 0.004 != 0 and Config["SETTING"]["music"]:
        pygame.mixer.music.load("resource/sound/music/" + random.choice(music_files))
        pygame.mixer.music.play()


# 进度条
class ProgressBar:
    def __init__(self, pos=None, val=None, length=100, width=20, color1=RED, color2=GRAY, num_display=None, background_color=WHITE, val_display_multiplier=1):
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

    def display(self, val=None):
        for i in range(0, self.length):
            pygame.draw.rect(SCREEN, color=self.color2, rect=(self.pos[0] + i, self.pos[1], 1, self.width))
        if val:
            self.val = val
        for i in range(0, self.val):
            pygame.draw.rect(SCREEN, color=self.color1, rect=(self.pos[0] + i, self.pos[1], 1, self.width))
        if self.num_statue[0]:
            if self.text_rect:
                pygame.draw.rect(SCREEN, rect=self.text_rect, color=self.bg_color)
            if self.num_statue[0] == "r":
                self.text_rect = text_display("%03s" % str(round(self.val * self.val_display_mul, 1)),
                                              (self.pos[0] + self.length + 10, self.pos[1] + self.width // 2),
                                              color=self.num_statue[1], size=FONT_SMALL)
            if self.num_statue[0] == "c":
                self.text_rect = text_display("%03s" % str(round(self.val * self.val_display_mul, 1)),
                                              (self.pos[0] + self.length // 2, self.pos[1] + self.width // 2),
                                              color=self.num_statue[1], size=FONT_SMALL)
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


# 字典返回键值映射，根据键值返回键
def map_dict_key_rel(val, map_dict_rel=load_map["win dot occ list rel"]):
    dict_keys = map_dict_rel.keys()
    for i in dict_keys:
        if val == map_dict_rel[i]:
            return i
    return None
