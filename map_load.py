from pygame import image

import code


class Map:
    def __init__(self):
        load_map = code.load_map()
        self.map_img = image.load(load_map["img"]).convert()
        self.pos = load_map["list pos"]
        self.pos_tp = load_map["list pos"]["tp"]
        self.pos_win = load_map["list pos"]["win"]
        self.pos_special = load_map["list pos"]["special"]
        self.pos_available = load_map["list pos"]["available"]
        self.pos_recovery = load_map["list pos"]["recovery"]
        self.pos_fort = load_map["list pos"]["fort"]
        self.pos_cannon = load_map["list pos"]["cannon"]
        self.pos_spurt = load_map["list pos"]["spurt"]
        self.list_pos_win_occ = load_map["win dot occ list"]
        self.list_pos_win_rel = load_map["win dot occ list rel"]
        self.person_capacity = load_map["person capacity"]
        self.person_pos_init = load_map["person init pos"]


MAP = Map()
