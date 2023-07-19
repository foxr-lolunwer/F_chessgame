import sys

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
    count = 0
    while True:
        screen.load()
        command = menu.menu_main()
        if command == "start":
            command = menu.menu_start()
            person_capacity = gaming_screen.map["person capacity"]
            if command == "PVP":
                # for i in range(0, person_capacity):
                #     locals()['player' + str(i)] = person.Person(str(i), code.Config["MAP"]["person init pos"][i])
                #     person_list.append((locals()['player' + str(i)].img, locals()['player' + str(i)].pos[1]))
                player1 = person.Person("1", (gaming_screen.map["person init pos"][0], code.change_pos(gaming_screen.map["person init pos"][0])))
                player2 = person.Person("2", (gaming_screen.map["person init pos"][1], code.change_pos(gaming_screen.map["person init pos"][1])))
                gaming_screen.start_init()
                gaming_screen.flip_screen(player1, player2, count)
                ui.ui_gaming_bottom()
                TURN = True
                # 开始回合
                while TURN:
                    player1.action_move = 1
                    player2.action_move = 1
                    count += 1
                    screen.ui_gaming_turn(count)
                    # move p1
                    player1.selected()
                    command_move = operation.dice("m")
                    command = operation.move_person_pos(player1.pos[0], player2.pos[0], command_move, map_pos)
                    gaming_screen.display_move_red_dot(command)
                    person_pos = operation.move_click(command)
                    player1.pos = person_pos
                    player1.action_move -= 1
                    player1.occ_buff(map_pos)
                    ui.ui_gaming_bottom_new(player1, player2)
                    gaming_screen.flip_screen(player1, player2, count)
                    if player1.action_move > 0:
                        player1.selected()
                        command = operation.move_person_pos(player1.pos[0], player2.pos[0], command_move, map_pos)
                        gaming_screen.display_move_red_dot(command)
                        person_pos = operation.move_click(command)
                        player1.pos = person_pos
                        player1.action_move -= 1
                        player1.occ_buff(map_pos)
                        ui.ui_gaming_bottom_new(player1, player2)
                        gaming_screen.flip_screen(player1, player2, count)
                    # move p2
                    player2.selected()
                    command_move = operation.dice("m")
                    # code.text_display("")
                    command = operation.move_person_pos(player2.pos[0], player1.pos[0], command_move, map_pos)
                    gaming_screen.display_move_red_dot(command)
                    person_pos = operation.move_click(command)
                    player2.pos = person_pos
                    player2.action_move -= 1
                    player2.occ_buff(map_pos)
                    ui.ui_gaming_bottom_new(player1, player2)
                    gaming_screen.flip_screen(player1, player2, count)
                    if player2.action_move > 0:
                        player2.selected()
                        command = operation.move_person_pos(player2.pos[0], player1.pos[0], command_move, map_pos)
                        gaming_screen.display_move_red_dot(command)
                        person_pos = operation.move_click(command)
                        player2.pos = person_pos
                        player2.action_move -= 1
                        player2.occ_buff(map_pos)
                        ui.ui_gaming_bottom_new(player1, player2)
                        gaming_screen.flip_screen(player1, player2, count)
                    # p1 fight
                    if not player1.DEF_dice:
                        player1.DEF_dice = 0
                        ui.ui_gaming_bottom_new(player1, player2)
                    player1.selected()
                    command_fight = operation.dice("f")
                    command = operation.fight_kill_val(player1.pos[0], player2.pos[0], command_fight, map_pos)
                    if command > 0:
                        command = player2.DEF_prop + player2.DEF_dice - command
                        if command > 0:
                            player2.HP -= command
                    elif command == -1:
                        player1.HP += 1
                    elif command == -2:
                        player1.DEF_dice += 1
                    else:
                        "fight error"
                    ui.ui_gaming_bottom_new(player1, player2)
                    player1.selected(False)
                    # p2 fight
                    if not player2.DEF_dice:
                        player2.DEF_dice = 0
                        ui.ui_gaming_bottom_new(player1, player2)
                    player2.selected()
                    command_fight = operation.dice("f")
                    command = operation.fight_kill_val(player2.pos[0], player1.pos[0], command_fight, map_pos)
                    if command > 0:
                        command = player1.DEF_prop + player1.DEF_dice - command
                        if command > 0:
                            player1.HP -= command
                    elif command == -1:
                        player2.HP += 1
                    elif command == -2:
                        player2.DEF_dice += 1
                    else:
                        "fight error"
                    ui.ui_gaming_bottom_new(player1, player2)
                    player2.selected(False)

            elif command == "PVE":
                continue
            else:
                continue  # error
        elif command == "course":
            menu.menu_course()
        elif command == "setting":
            menu.menu_setting()
        elif command == "exit":
            pygame.quit()
            sys.exit()
        else:
            continue  # error
