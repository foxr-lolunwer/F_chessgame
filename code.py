import pygame
import datetime

import init


def create_date_file(file):
    if file:
        date_file = "log/%s-%s-%s-%s.txt" % (datetime.date.today(), datetime.datetime.now().hour,
                                             datetime.datetime.now().minute, datetime.datetime.now().second)
        return date_file
    else:
        return


DATE_FILE = create_date_file(False)


def date_write(text, file):
    try:
        with open(file, mode='a') as gaming_log:
            gaming_log.write(str(pygame.time.get_ticks()) + ":" + text + "\n")
        del gaming_log
        print(str(pygame.time.get_ticks()) + ":" + text)
    except:
        return


def load_map():
    map_load = init.Config["MAP"][init.Config["MAP"]["default map"]]
    return map_load

# def map_dict_key_rel(val, map_dict_rel=load_map["win dot occ list rel"]):
#     dict_keys = map_dict_rel.keys()
#     for i in dict_keys:
#         if val == map_dict_rel[i]:
#             return i
#     return None
