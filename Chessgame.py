#  Pyinstaller -F -w -i icon.ico Chessgame.py
#  Pyinstaller -F -i icon.ico Chessgame.py

import sys
import time

import pygame

import code
import operation
import person
import screen
import AI_operation


def turn_move(player, other_players):
    player.selected()
    screen.gaming_screen.display_statue(player.name + code.T["Please throw!"], code.SCREEN)
    if screen.gaming_screen.gaming_throw():
        return
    t_command_move = operation.dice("m")
    screen.gaming_screen.display_statue(player.name + code.T[t_command_move], code.SCREEN)
    t_command = operation.move_person_pos(player.pos[0], other_players.pos[0], t_command_move, map_pos)
    screen.gaming_screen.display_move_red_dot(t_command)
    t_person_pos = operation.move_click(t_command)
    if t_person_pos == "return":
        return
    if t_person_pos:
        player.pos = t_person_pos
    player.action_move -= 1
    if player.occ_buff(map_pos):
        win_dot_occ[code.map_dict_key_rel(player.pos[0])] = "p" + player.number
    screen.gaming_screen.ui_gaming_data_new(player, other_players)
    screen.gaming_screen.flip_screen(player, other_players, count, win_dot_occ)
    if screen.gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
        return
    if player.action_move > 0:
        player.selected()
        t_command = operation.move_person_pos(player.pos[0], other_players.pos[0], t_command_move, map_pos)
        screen.gaming_screen.display_move_red_dot(t_command)
        t_person_pos = operation.move_click(t_command)
    if t_person_pos == "return":
        return
    if t_person_pos:
        player.pos = t_person_pos
    player.action_move -= 1
    if player.occ_buff(map_pos):
        win_dot_occ[code.map_dict_key_rel(player.pos[0])] = "p" + player.number
    screen.gaming_screen.ui_gaming_data_new(player, other_players)
    screen.gaming_screen.flip_screen(player, other_players, count, win_dot_occ)
    if screen.gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
        return


def turn_fight(player, other_players):
    if player.DEF_dice:
        player.DEF_dice = 0
        screen.gaming_screen.ui_gaming_data_new(player, other_players)
    player.selected()
    screen.gaming_screen.display_statue(code.T["Player 1"] + code.T["Please throw!"], code.SCREEN)
    if screen.gaming_screen.gaming_throw():
        return
    t_command_fight = operation.dice("f")
    screen.gaming_screen.display_statue(code.T["Player 1"] + code.T[t_command_fight], code.SCREEN)
    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    t_command = operation.fight_kill_val(player.pos[0], other_players.pos[0], t_command_fight, map_pos)
    if t_command >= 0:
        t_command = t_command - (other_players.DEF_prop + other_players.DEF_dice)
        if t_command > 0:
            other_players.HP -= t_command
            screen.gaming_screen.display_statue(code.T["Player 1"] + code.T["Kill Val is "] + str(t_command), code.SCREEN)
        else:
            screen.gaming_screen.display_statue(code.T["Player 1"] + code.T["MISS"], code.SCREEN)
    elif t_command == -1:
        player.HP += 1
        screen.gaming_screen.display_statue(code.T["Player 1"] + code.T["HP Recovery"], code.SCREEN)
    elif t_command == -2:
        player.DEF_dice += 1
        screen.gaming_screen.display_statue(code.T["Player 1"] + code.T["DEF + 1"], code.SCREEN)
    else:
        "fight error"
    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
    if screen.gaming_screen.screen_win(operation.find_winner(player.HP, other_players.HP)):
        return
    screen.gaming_screen.ui_gaming_data_new(player, other_players)
    player.selected(False)


if __name__ == '__main__':
    code.game_init()
    map_pos = code.load_map["list pos"]
    win_dot_occ = code.load_map["win dot occ list"]
    count = 0
    code.play_music()
    code.date_write("-GAME INIT DONE-", code.DATE_FILE)
    while True:
        screen.load()
        command = screen.menu.menu_main()
        if command == "start":
            command = screen.menu.menu_start()
            person_capacity = screen.gaming_screen.map["person capacity"]
            if command == "PVP":
                player1 = person.Person("1", (
                    screen.gaming_screen.map["person init pos"][0], code.change_pos(screen.gaming_screen.map["person init pos"][0])), "player 1")
                player2 = person.Person("2", (
                    screen.gaming_screen.map["person init pos"][1], code.change_pos(screen.gaming_screen.map["person init pos"][1])), "player 2")
                screen.gaming_screen.start_init(occ_dict=win_dot_occ)
                screen.gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                screen.gaming_screen.ui_gaming_val(win_dot_occ)
                screen.gaming_screen.ui_gaming_data_new(player1, player2)
                TURN = True
                # 开始回合
                code.date_write("-GAMING INIT DONE-", code.DATE_FILE)
                while TURN:
                    player1.action_move = 1
                    player2.action_move = 1
                    count += 1
                    screen.ui_gaming_turn(count)
                    turn_move(player1, player2)
                    turn_move(player2, player1)
                    turn_fight(player1, player2)
                    turn_fight(player2, player1)
            elif command == "PVE":
                player1 = person.Person("1", (
                    screen.gaming_screen.map["person init pos"][0], code.change_pos(screen.gaming_screen.map["person init pos"][0])), "player 1")
                player2 = person.AIPerson("2", (
                    screen.gaming_screen.map["person init pos"][1], code.change_pos(screen.gaming_screen.map["person init pos"][1])), "player 2")
                screen.gaming_screen.start_init(occ_dict=win_dot_occ)
                screen.gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                screen.gaming_screen.ui_gaming_val(win_dot_occ)
                screen.gaming_screen.ui_gaming_data_new(player1, player2)
                TURN = True
                # 开始回合
                code.date_write("-GAMING INIT DONE-", code.DATE_FILE)
                while TURN:
                    player1.action_move = 1  # 移动次数
                    player2.action_move = 1
                    count += 1  # 回合数
                    screen.ui_gaming_turn(count)
                    # move p1
                    turn_move(player1, player2)
                    # move p2
                    player2.selected()
                    person_pos, again = AI_operation.AI_move(player2, player1)
                    player2.action_move -= 1
                    if person_pos:
                        player2.pos = (person_pos, code.change_pos(person_pos))
                    if player2.occ_buff(map_pos):
                        win_dot_occ[code.map_dict_key_rel(player2.pos[0])] = "p2"
                    screen.gaming_screen.ui_gaming_data_new(player1, player2)
                    screen.gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 0.5)
                    if screen.gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
                        break
                    if player2.action_move > 0:
                        player2.selected()
                        person_pos, again = AI_operation.AI_move(player2, player1)
                        player2.action_move -= 1
                        if person_pos:
                            player2.pos = (person_pos, code.change_pos(person_pos))
                        if player2.occ_buff(map_pos):
                            win_dot_occ[code.map_dict_key_rel(player2.pos[0])] = "p2"
                        screen.gaming_screen.ui_gaming_data_new(player1, player2)
                        screen.gaming_screen.flip_screen(player1, player2, count, win_dot_occ)
                        time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 0.5)
                        if screen.gaming_screen.screen_win(operation.find_winner(occ_dict=win_dot_occ)):
                            break
                    # p1 fight
                    turn_fight(player1, player2)
                    # p2 fight
                    if player2.DEF_dice:
                        player2.DEF_dice = 0
                        screen.gaming_screen.ui_gaming_data_new(player1, player2)
                    player2.selected()
                    screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["Please throw!"], code.SCREEN)
                    screen.gaming_screen.gaming_throw("AI")
                    command_fight = operation.dice("f")
                    screen.gaming_screen.display_statue(code.T["Player 2"] + code.T[command_fight], code.SCREEN)
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    command = operation.fight_kill_val(player2.pos[0], player1.pos[0], command_fight, map_pos)
                    if command >= 0:
                        command = command - (player1.DEF_prop + player1.DEF_dice)
                        if command > 0:
                            player1.HP -= command
                            screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["Kill Val is "] + str(command), code.SCREEN)
                        else:
                            screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["MISS"], code.SCREEN)
                    elif command == -1:
                        player2.HP += 1
                        screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["HP Recovery"], code.SCREEN)
                    elif command == -2:
                        player2.DEF_dice += 1
                        screen.gaming_screen.display_statue(code.T["Player 2"] + code.T["DEF + 1"], code.SCREEN)
                    else:
                        "fight error"
                    time.sleep((100 - code.Config["SETTING"]["game speed"]) * 0.02 * 1)
                    if screen.gaming_screen.screen_win(operation.find_winner(player1.HP, player2.HP)):
                        break
                    screen.gaming_screen.ui_gaming_data_new(player1, player2)
                    player2.selected(False)
            else:
                continue  # error
            code.date_write("-GAMING OVER-", code.DATE_FILE)
        elif command == "course":
            screen.menu.menu_course()
        elif command == "setting":
            screen.menu.menu_setting()
        elif command == "exit":
            pygame.quit()
            sys.exit()
        else:
            continue  # error
