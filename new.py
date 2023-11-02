import sys
import time

import pygame

import code
import operation
import screen
import map


class FChessGame:
    def __init__(self):
        self.game_ver = "0.10"
        self.config = code.Config
        self.screen = self.screen_init()
        self.game_map = map.Map()
        self.menu = screen.menu(self.screen)
        self.gaming_screen = screen.gaming_screen(self.screen)
        self.turn = operation.Turn(self.screen, self.gaming_screen, self.game_map)

    def screen_init(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Game ver " + self.game_ver)  # 窗口标题显示10
        m_screen = pygame.display.set_mode((1060, 636))  # 设置游戏窗口大小：530*636（像素）
        icon = pygame.image.load(self.config["IMG"]["icon"]).convert()  # 引入窗口图标
        pygame.display.set_icon(icon)  # 显示窗口坐标
        return m_screen

    def run(self):
        code.date_write("-DATE FILE CREATE-", code.DATE_FILE)
        self.screen.fill(code.WHITE)
        code.play_music()
        code.date_write("-GAME INIT DONE-", code.DATE_FILE)
        while True:
            self.__load()
            command = screen.menu.menu_main()
            if command == "start":
                command = self.menu.menu_start()
                if command == "PVP":
                    command = self.turn.turn_pvp()
                    if command:
                        continue
                elif command == "PVE":
                    command = self.turn.turn_pve()
                    if command:
                        continue
                else:
                    continue  # error
                continue
            elif command == "course":
                self.menu.menu_course()
                continue
            elif command == "setting":
                self.menu.menu_setting()
                continue
            elif command == "exit":
                pygame.quit()
                sys.exit()
            else:
                continue  # error

    def __load(self):
        load_img = pygame.image.load(code.Config["IMG"]["load"]).convert()
        self.screen.fill(code.WHITE)
        self.screen.blit(load_img, (130, 100))
        code.text_display(code.T["LOADING"], (400, 600))
        pygame.display.flip()
        time.sleep(0.5)


if __name__ == "__main__":
    game = FChessGame()
