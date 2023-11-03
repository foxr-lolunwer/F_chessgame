import pygame

import init
import map_load


class Person:
    def __init__(self, screen, number, pos, name=None):
        self.screen = screen
        self.img = (pygame.image.load(init.Config["IMG"]["person " + str(number + 1)][0]).convert(),
                    pygame.image.load(init.Config["IMG"]["person " + str(number + 1)][1]).convert())
        self.img[0].set_colorkey(init.WHITE)
        self.img[1].set_colorkey(init.WHITE)
        self.number = number
        self.HP = 5
        self.DEF_prop = 0
        self.DEF_dice = 0
        self.pos = pos  # (g_pos, (p_pos))
        if name:
            self.name = name
        else:
            self.name = "player " + str(self.number)
        self.damage_mul = 1
        self.action_move = 1
        self.action_damage = 1

    def selected(self, statue=True):
        if statue:
            self.screen.blit(self.img[1], self.pos[1])
        else:
            self.screen.blit(self.img[0], self.pos[1])
        pygame.display.flip()

    def flip_person_pos(self, i):
        self.screen.blit(self.img[i], self.pos[1])
        pygame.display.flip()
        
    def occ_buff(self):
        self.DEF_prop = 0
        if self.pos[0] not in map_load.MAP.pos_available:
            return None
        # 生命恢复点位
        if self.pos[0] in [208, 802]:
            if self.HP < 9:
                self.HP += 1
            return None
        # 堡垒点位
        elif self.pos[0] in [406, 604]:
            self.DEF_prop = 1
            return None
        # 大炮点位
        elif self.pos[0] == 505:
            self.damage_mul = 2
            return None
        # 再次移动点位
        elif self.pos[0] in [404, 606]:
            self.action_move += 1
            return None
        # 占领点位
        elif self.pos[0] in map_load.MAP.pos_win:
            return self.pos[0]
        else:
            return None


class AIPerson(Person):
    def __init__(self, number, pos, name, AI_Config_difficulty=init.Config["SETTING"]["AI Difficulty"][init.Config["SETTING"]["AI Difficulty"]["setting"]]):
        super().__init__(number, pos, name)
        self.HP = AI_Config_difficulty["hp init"]
        self.DEF_ai = AI_Config_difficulty["def init"]
