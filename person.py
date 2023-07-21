import pygame

import code


class Person:
    def __init__(self, number, pos):
        self.img = (pygame.image.load(code.Config["IMG"]["person " + number][0]).convert(),
                    pygame.image.load(code.Config["IMG"]["person " + number][1]).convert())
        self.img[0].set_colorkey(code.WHITE)
        self.img[1].set_colorkey(code.WHITE)
        self.HP = 5
        self.DEF_prop = 0
        self.DEF_dice = 0
        self.pos = pos
        self.name = None
        self.damage_mul = 1
        self.action_move = 1
        self.action_damage = 1

    def selected(self, statue=True):
        if statue:
            code.SCREEN.blit(self.img[1], self.pos[1])
        else:
            code.SCREEN.blit(self.img[0], self.pos[1])
        pygame.display.flip()

    def flip_person_pos(self, i):
        code.SCREEN.blit(self.img[i], self.pos[1])
        pygame.display.flip()
        
    def occ_buff(self, dict_map_pos):
        self.DEF_prop = 0
        if self.pos[0] not in dict_map_pos["game available"]:
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
        elif self.pos[0] in dict_map_pos["win dot"]:
            return self.pos[0]
        else:
            return None


class AIPerson(Person):
    def __init__(self, number, pos, AI_Config_difficulty=code.Config["SETTING"]["AI Difficulty"][code.Config["SETTING"]["AI Difficulty"]["setting"]]):
        super().__init__(number, pos)
        self.HP = AI_Config_difficulty["hp init"]
        self.DEF_ai = AI_Config_difficulty["def init"]


