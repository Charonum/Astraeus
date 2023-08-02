import math
import random
import numpy as np
from PIL import Image
from functools import lru_cache


def update_localization(id, name, desc, config_file, type):
    en_us_start = config_file.find('en-us')
    en_us_end = config_file.find('}', en_us_start)

    if en_us_start != -1 and en_us_end != -1:
        en_us_block = config_file[en_us_start:en_us_end]

        last_description_start = en_us_block.rfind('#LOC_')
        last_description_end = en_us_block.find('\n', last_description_start)

        if last_description_start != -1 and last_description_end != -1:
            last_description = en_us_block[last_description_start:last_description_end]
            indentation = last_description[:last_description.find('#')]

        new_entry = '''
        #LOC_GU_{}_{}_displayName = {}^N
        #LOC_GU_{}_{}_description = {}<color=#ffb765>Analogous to {}.</color>
        '''.format(type, id, name, type, id, desc, name)

        new_en_us_block = en_us_block[:last_description_end] + new_entry + en_us_block[last_description_end:]

        new_config_file = config_file[:en_us_start] + new_en_us_block + config_file[en_us_end:]
    else:
        print("Localization block not found in the config file.")
    return new_config_file

