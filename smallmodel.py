import os
import random

import pygame

import init


class Music:
    def __init__(self):
        self.path = "resource/sound/music"
        root, dirs, self.music_files = list(os.walk(self.path))[0]

    def play_effect(self, music_name, count=0):
        effect = pygame.mixer.Sound(init.Config["SOUND"][music_name])
        effect.set_volume(init.Config["SETTING"]["game volume"] * 0.004)
        effect.play(loops=count)

    def play_music(self):
        pygame.mixer.music.load("resource/sound/music/" + random.choice(self.music_files))
        pygame.mixer.music.set_volume(init.Config["SETTING"]["game volume"] * 0.001)
        if not init.Config["SETTING"]["music"]:
            pygame.mixer.music.stop()
            return
        pygame.mixer.music.play()

    def music_volume_change(self):
        # 如果音乐停止，随机播放下一首
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("resource/sound/music/" + random.choice(self.music_files))
            pygame.mixer.music.play()
        pygame.mixer.music.pause()
        if init.Config["SETTING"]["game volume"] * 0.004 == 0:
            return
        if not init.Config["SETTING"]["music"]:
            pygame.mixer.music.stop()
            return
        pygame.mixer.music.set_volume(init.Config["SETTING"]["game volume"] * 0.01)
        pygame.mixer.music.unpause()

    def music_continue(self):
        # 如果音乐停止并且音量不为零，并开启了音乐，随机播放下一首
        if not pygame.mixer.music.get_busy() and init.Config["SETTING"]["game volume"] * 0.004 != 0 and init.Config["SETTING"]["music"]:
            pygame.mixer.music.load("resource/sound/music/" + random.choice(self.music_files))
            pygame.mixer.music.play()


MUSIC = Music()
