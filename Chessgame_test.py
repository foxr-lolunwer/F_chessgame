#  Pyinstaller -F -w -i icon.ico Chessgame_test.py
#  Pyinstaller -F -i icon.ico Chessgame_test.py

import sys
import time

import pygame

import code
import operation
import person
import screen

if __name__ == '__main__':
    code.game_init()
    menu = screen.Menu()
    ui = screen.UI()
    gaming_screen = screen.Gaming()
    map_pos = gaming_screen.map["list pos"]
    win_dot_occ = code.Config["MAP"]["map 1"]["win dot occ list"]
    count = 0
    code.play_music()
    code.date_write("-GAME INIT DONE-", code.DATE_FILE)
    while True:
        screen.load()
        command = menu.menu_main()
        if command == "start":
            command = menu.menu_start()
            person_capacity = gaming_screen.map["person capacity"]
            if command == "PVP":
                player1 = person.Person("1", (
                    gaming_screen.map["person init pos"][0], code.change_pos(gaming_screen.map["person init pos"][0])))
                player2 = person.Person("2", (
                    gaming_screen.map["person init pos"][1], code.change_pos(gaming_screen.map["person init pos"][1])))
                gaming_screen.start_init()
                gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                ui.ui_gaming_val(win_dot_occ)
                ui.ui_gaming_data_new(player1, player2)
                TURN = True
                # 开始回合
                code.date_write("-GAMING INIT DONE-", code.DATE_FILE)
                while TURN:
                    player1.action_move = 1
                    player2.action_move = 1
                    count += 1
                    screen.ui_gaming_turn(count)
                    # move p1
                    player1.selected()
                    gaming_screen.display_statue("Please throw!", code.SCREEN)
                    if gaming_screen.gaming_throw():
                        break
                    command_move = operation.dice("m")
                    gaming_screen.display_statue(command_move, code.SCREEN)
                    command = operation.move_person_pos(player1.pos[0], player2.pos[0], command_move, map_pos)
                    gaming_screen.display_move_red_dot(command)
                    person_pos = operation.move_click(command)
                    if person_pos == "return":
                        break
                    if person_pos:
                        player1.pos = person_pos
                    player1.action_move -= 1
                    if player1.occ_buff(map_pos):
                        win_dot_occ[str(player1.pos[0])] = "p1"
                    ui.ui_gaming_data_new(player1, player2)
                    gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                    if gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
                        break
                    if player1.action_move > 0:
                        player1.selected()
                        command = operation.move_person_pos(player1.pos[0], player2.pos[0], command_move, map_pos)
                        gaming_screen.display_move_red_dot(command)
                        person_pos = operation.move_click(command)
                    if person_pos == "return":
                        break
                    if person_pos:
                        player1.pos = person_pos
                    player1.action_move -= 1
                    if player1.occ_buff(map_pos):
                        win_dot_occ[str(player1.pos[0])] = "p1"
                    ui.ui_gaming_data_new(player1, player2)
                    gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                    if gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
                        break
                    # move p2
                    player2.selected()
                    gaming_screen.display_statue("Please throw!", code.SCREEN)
                    if gaming_screen.gaming_throw():
                        break
                    command_move = operation.dice("m")
                    gaming_screen.display_statue(command_move, code.SCREEN)
                    # code.text_display("")
                    command = operation.move_person_pos(player2.pos[0], player1.pos[0], command_move, map_pos)
                    gaming_screen.display_move_red_dot(command)
                    person_pos = operation.move_click(command)
                    if person_pos == "return":
                        break
                    if person_pos:
                        player2.pos = person_pos
                    player2.action_move -= 1
                    if player2.occ_buff(map_pos):
                        win_dot_occ[str(player2.pos[0])] = "p2"
                    ui.ui_gaming_data_new(player1, player2)
                    gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                    if gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
                        break
                    if player2.action_move > 0:
                        player2.selected()
                        command = operation.move_person_pos(player2.pos[0], player1.pos[0], command_move, map_pos)
                        gaming_screen.display_move_red_dot(command)
                        person_pos = operation.move_click(command)
                    if person_pos == "return":
                        break
                    if person_pos:
                        player2.pos = person_pos
                    player2.action_move -= 1
                    if player2.occ_buff(map_pos):
                        win_dot_occ[str(player2.pos[0])] = "p2"
                    ui.ui_gaming_data_new(player1, player2)
                    gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                    if gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
                        break
                    # p1 fight
                    if player1.DEF_dice:
                        player1.DEF_dice = 0
                        ui.ui_gaming_data_new(player1, player2)
                    player1.selected()
                    gaming_screen.display_statue("Please throw!", code.SCREEN)
                    if gaming_screen.gaming_throw():
                        break
                    command_fight = operation.dice("f")
                    gaming_screen.display_statue(command_fight, code.SCREEN)
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    command = operation.fight_kill_val(player1.pos[0], player2.pos[0], command_fight, map_pos)
                    if command >= 0:
                        command = command - (player2.DEF_prop + player2.DEF_dice)
                        if command > 0:
                            player2.HP -= command
                            gaming_screen.display_statue("Kill Val is " + str(command), code.SCREEN)
                        else:
                            gaming_screen.display_statue("MISS", code.SCREEN)
                    elif command == -1:
                        player1.HP += 1
                        gaming_screen.display_statue("HP Recovery", code.SCREEN)
                    elif command == -2:
                        player1.DEF_dice += 1
                        gaming_screen.display_statue("DEF + 1", code.SCREEN)
                    else:
                        "fight error"
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    if gaming_screen.screen_win(operation.find_winner(player1.HP, player2.HP)):
                        break
                    ui.ui_gaming_data_new(player1, player2)
                    player1.selected(False)
                    # p2 fight
                    if player2.DEF_dice:
                        player2.DEF_dice = 0
                        ui.ui_gaming_data_new(player1, player2)
                    player2.selected()
                    gaming_screen.display_statue("Please throw!", code.SCREEN)
                    if gaming_screen.gaming_throw():
                        break
                    command_fight = operation.dice("f")
                    gaming_screen.display_statue(command_fight, code.SCREEN)
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    command = operation.fight_kill_val(player2.pos[0], player1.pos[0], command_fight, map_pos)
                    if command >= 0:
                        command = command - (player1.DEF_prop + player1.DEF_dice)
                        if command > 0:
                            player1.HP -= command
                            gaming_screen.display_statue("Kill Val is " + str(command), code.SCREEN)
                        else:
                            gaming_screen.display_statue("MISS", code.SCREEN)
                    elif command == -1:
                        player2.HP += 1
                        gaming_screen.display_statue("HP Recovery", code.SCREEN)
                    elif command == -2:
                        player2.DEF_dice += 1
                        gaming_screen.display_statue("DEF + 1", code.SCREEN)
                    else:
                        "fight error"
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    ui.ui_gaming_data_new(player1, player2)
                    player2.selected(False)
            elif command == "PVE":
                player1 = person.Person("1", (
                    gaming_screen.map["person init pos"][0], code.change_pos(gaming_screen.map["person init pos"][0])))
                player2 = person.AIPerson("2", (
                    gaming_screen.map["person init pos"][1], code.change_pos(gaming_screen.map["person init pos"][1])))
                gaming_screen.start_init()
                gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                ui.ui_gaming_val(win_dot_occ)
                ui.ui_gaming_data_new(player1, player2)
                TURN = True
                # 开始回合
                code.date_write("-GAMING INIT DONE-", code.DATE_FILE)
                while TURN:
                    player1.action_move = 1
                    player2.action_move = 1
                    count += 1
                    screen.ui_gaming_turn(count)
                    # move p1
                    player1.selected()
                    gaming_screen.display_statue("Please throw!", code.SCREEN)
                    if gaming_screen.gaming_throw():
                        break
                    command_move = operation.dice("m")
                    gaming_screen.display_statue(command_move, code.SCREEN)
                    command = operation.move_person_pos(player1.pos[0], player2.pos[0], command_move, map_pos)
                    gaming_screen.display_move_red_dot(command)
                    person_pos = operation.move_click(command)
                    if person_pos == "return":
                        break
                    if person_pos:
                        player1.pos = person_pos
                    player1.action_move -= 1
                    if player1.occ_buff(map_pos):
                        win_dot_occ[str(player1.pos[0])] = "p1"
                    ui.ui_gaming_data_new(player1, player2)
                    gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                    if gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
                        break
                    if player1.action_move > 0:
                        player1.selected()
                        command = operation.move_person_pos(player1.pos[0], player2.pos[0], command_move, map_pos)
                        gaming_screen.display_move_red_dot(command)
                        person_pos = operation.move_click(command)
                    if person_pos == "return":
                        break
                    if person_pos:
                        player1.pos = person_pos
                    player1.action_move -= 1
                    if player1.occ_buff(map_pos):
                        win_dot_occ[str(player1.pos[0])] = "p1"
                    ui.ui_gaming_data_new(player1, player2)
                    gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                    if gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
                        break
                    # move p2
                    player2.selected()
                    gaming_screen.display_statue("Please throw!", code.SCREEN)
                    gaming_screen.gaming_throw("AI")
                    command_move = operation.dice("m")
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 0.5)
                    gaming_screen.display_statue(command_move, code.SCREEN)
                    # code.text_display("")
                    command = operation.move_person_pos(player2.pos[0], player1.pos[0], command_move, map_pos)
                    gaming_screen.display_move_red_dot(command)
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 0.5)
                    person_pos = operation.move_click(command, "AI")
                    if person_pos:
                        player2.pos = person_pos
                    player2.action_move -= 1
                    if player2.occ_buff(map_pos):
                        win_dot_occ[str(player2.pos[0])] = "p2"
                    ui.ui_gaming_data_new(player1, player2)
                    gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 0.5)
                    if gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
                        break
                    if player2.action_move > 0:
                        player2.selected()
                        command = operation.move_person_pos(player2.pos[0], player1.pos[0], command_move, map_pos)
                        gaming_screen.display_move_red_dot(command)
                        time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 0.5)
                        person_pos = operation.move_click(command, "AI")
                        if person_pos:
                            player2.pos = person_pos
                        player2.action_move -= 1
                        if player2.occ_buff(map_pos):
                            win_dot_occ[str(player2.pos[0])] = "p2"
                        ui.ui_gaming_data_new(player1, player2)
                        gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                        time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 0.5)
                        if gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
                            break
                    # p1 fight
                    if player1.DEF_dice:
                        player1.DEF_dice = 0
                        ui.ui_gaming_data_new(player1, player2)
                    player1.selected()
                    gaming_screen.display_statue("Please throw!", code.SCREEN)
                    if gaming_screen.gaming_throw():
                        break
                    command_fight = operation.dice("f")
                    gaming_screen.display_statue(command_fight, code.SCREEN)
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    command = operation.fight_kill_val(player1.pos[0], player2.pos[0], command_fight, map_pos)
                    if command >= 0:
                        command = command - (player2.DEF_prop + player2.DEF_dice)
                        if command > 0:
                            player2.HP -= command
                            gaming_screen.display_statue("Kill Val is " + str(command), code.SCREEN)
                        else:
                            gaming_screen.display_statue("MISS", code.SCREEN)
                    elif command == -1:
                        player1.HP += 1
                        gaming_screen.display_statue("HP Recovery", code.SCREEN)
                    elif command == -2:
                        player1.DEF_dice += 1
                        gaming_screen.display_statue("DEF + 1", code.SCREEN)
                    else:
                        "fight error"
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    if gaming_screen.screen_win(operation.find_winner(player1.HP, player2.HP)):
                        break
                    ui.ui_gaming_data_new(player1, player2)
                    player1.selected(False)
                    # p2 fight
                    if player2.DEF_dice:
                        player2.DEF_dice = 0
                        ui.ui_gaming_data_new(player1, player2)
                    player2.selected()
                    gaming_screen.display_statue("Please throw!", code.SCREEN)
                    gaming_screen.gaming_throw("AI")
                    command_fight = operation.dice("f")
                    gaming_screen.display_statue(command_fight, code.SCREEN)
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    command = operation.fight_kill_val(player2.pos[0], player1.pos[0], command_fight, map_pos)
                    if command >= 0:
                        command = command - (player1.DEF_prop + player1.DEF_dice)
                        if command > 0:
                            player1.HP -= command
                            gaming_screen.display_statue("Kill Val is " + str(command), code.SCREEN)
                        else:
                            gaming_screen.display_statue("MISS", code.SCREEN)
                    elif command == -1:
                        player2.HP += 1
                        gaming_screen.display_statue("HP Recovery", code.SCREEN)
                    elif command == -2:
                        player2.DEF_dice += 1
                        gaming_screen.display_statue("DEF + 1", code.SCREEN)
                    else:
                        "fight error"
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    ui.ui_gaming_data_new(player1, player2)
                    player2.selected(False)
            else:
                continue  # error
            code.date_write("-GAMING OVER-", code.DATE_FILE)
        elif command == "course":
            menu.menu_course()
        elif command == "setting":
            menu.menu_setting()
        elif command == "exit":
            pygame.quit()
            sys.exit()
        else:
            continue  # error
