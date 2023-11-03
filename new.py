import sys
import time

import pygame

import init
import code
import operation
import screen
import smallmodel
import turn


class FChessGame:
    def __init__(self):
        self.game_ver = "0.10"
        self.operate = operation.Operation()
        self.turn = turn.Turn()

    def run(self):
        code.date_write("-DATE FILE CREATE-", code.DATE_FILE)
        init.screen.fill(init.WHITE)
        smallmodel.MUSIC.play_music()
        code.date_write("-GAME INIT DONE-", code.DATE_FILE)
        while True:
            self.__load()
            command = screen.MENU.menu_main()
            if command == "start":
                command = screen.MENU.menu_start()
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
                screen.MENU.menu_course()
                continue
            elif command == "setting":
                screen.MENU.menu_setting()
                continue
            elif command == "exit":
                pygame.quit()
                sys.exit()
            else:
                continue  # error

    def __load(self):
        load_img = pygame.image.load(init.Config["IMG"]["load"]).convert()
        init.screen.fill(init.WHITE)
        init.screen.blit(load_img, (130, 100))
        self.operate.text_display(init.T["LOADING"], (400, 600))
        pygame.display.flip()
        time.sleep(0.5)


if __name__ == "__main__":
    game = FChessGame()
    game.run()
    pygame.quit()
    sys.exit()
