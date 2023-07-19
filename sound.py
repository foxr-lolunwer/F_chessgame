import code
import pygame
import time
import datetime
import random
import sys


class Sound:
    def __init__(self):
        self.shot = pygame.mixer.Sound("resource/sound/effect/shot.wav")
        self.bomb = pygame.mixer.Sound("")
