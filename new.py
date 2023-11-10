import sys

import pygame

import init
import code
import screen
import smallmodel
import turn


def run():
    code.date_write("-DATE FILE CREATE-", code.DATE_FILE)
    init.screen.fill(init.WHITE)
    smallmodel.MUSIC.play_music()
    code.date_write("-GAME INIT DONE-", code.DATE_FILE)
    while True:
        screen.MENU.load()
        command = screen.MENU.menu_main()
        if command == "start":
            command = screen.MENU.menu_start()
            if command:
                command = turn.O_TURN.turn_pvp()
            if command:
                turn.O_TURN.clear()
                continue
            else:
                continue  # error
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


if __name__ == "__main__":
    run()
    pygame.quit()
    sys.exit()
