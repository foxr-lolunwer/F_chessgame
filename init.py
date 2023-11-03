import pygame
import init_ture

Config = init_ture.Config
T = init_ture.T
CLOCK = pygame.time.Clock()
pygame.init()
pygame.mixer.init()
game_ver = "0.10"
pygame.display.set_caption("Game ver " + game_ver)  # 窗口标题显示10
screen = pygame.display.set_mode((1060, 636))  # 设置游戏窗口大小：530*636（像素）
icon = pygame.image.load(Config["IMG"]["icon"]).convert()  # 引入窗口图标
pygame.display.set_icon(icon)  # 显示窗口坐标

FONT_BIG = pygame.font.SysFont('SimHei', 30)  # 默认大号字体
FONT_MID = pygame.font.SysFont('SimHei', 16)  # 默认正常字体
FONT_SMALL = pygame.font.SysFont('SimHei', 12)  # 默认小号字体
IMG = [pygame.image.load(Config["IMG"]["select box"][0]).convert(),
       pygame.image.load(Config["IMG"]["select box"][1]).convert()]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (155, 155, 155)
RED = (255, 0, 0)
GRAY_BG = (191, 191, 191)
