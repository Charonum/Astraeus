import math
import random
import numpy as np
from PIL import Image
from noise import pnoise2
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


def coherent_noise(in_color_map, h_map, save_path, h_path):
    width, height = 2500, 1250
    subdivisions = random.randint(1, 16)

    scale = 0.05
    octaves = 6
    persistence = 0.5

    color_map = {}

    for i in in_color_map.keys():
        id_ = 0
        for item in in_color_map.keys():
            if i == item:
                break
            else:
                id_ += 1
        try:
            color_map[in_color_map.get(i)] = h_map[id_]
        except:
            break
    print(color_map)

    @lru_cache(maxsize=None)
    def generate_elevation(x, y):
        nx = x * scale
        ny = y * scale
        elevation = 0.0
        freq = 1.0
        amp = 1.0
        for _ in range(octaves):
            elevation += pnoise2(nx * freq, ny * freq, octaves=1) * amp
            freq *= 2.0
            amp *= persistence
        return elevation

    elevation_map = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            elevation = generate_elevation(x / subdivisions, y / subdivisions)
            elevation_map[y][x] = elevation

    min_elevation = np.min(elevation_map)
    max_elevation = np.max(elevation_map)
    elevation_map = (elevation_map - min_elevation) / (max_elevation - min_elevation)

    image = Image.new("RGB", (width, height))
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            elevation = elevation_map[y][x]
            for elevation_range, color in color_map.items():
                if elevation_range[0] <= elevation < elevation_range[1]:
                    pixels[x, y] = color
                    break

    upscaled_image = image.resize((width * subdivisions, height * subdivisions), resample=Image.BICUBIC)

    upscaled_image = upscaled_image.resize((width, height))

    upscaled_image.save(save_path)

    #color_map = {
        #(17, 241, 231): (5, 25),
        #(158, 25, 25): (25, 50),
        #(47, 22, 22): (1, 6),
        #(158, 79, 79): (50, 100)
    #}

    # Generate the height map from the image with added randomness
    height_map = generate_height_map(save_path, color_map, noise_scale=4)

    # Save the height map as an image
    image = Image.fromarray((height_map * 255).astype(np.uint8), mode="L")
    image.save(h_path)


def generate_height_map(image_path, color_map, noise_scale=0.01):
    # Load the image
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    # Create the empty height map
    height_map = np.zeros((height, width))

    # Iterate over each pixel in the image
    for y in range(height):
        for x in range(width):
            # Get the color of the pixel
            color = image.getpixel((x, y))

            # Find the corresponding elevation range based on the color
            elevation_range = None
            for color_range, range_values in color_map.items():
                if color_range == color:
                    elevation_range = range_values
                    break

            if elevation_range is not None:
                # Calculate the average of the elevation range
                elevation = (elevation_range[0] + elevation_range[1]) / 2
                # Assign the elevation to the height map
                height_map[y, x] = elevation

    # Apply noise to the height map
    height_map += np.random.uniform(-noise_scale, noise_scale, size=(height, width))

    # Normalize the height map
    height_map = normalize_height_map(height_map)

    return height_map


def normalize_height_map(height_map):
    # Normalize the height map to the range [0, 1]
    min_elevation = np.min(height_map)
    max_elevation = np.max(height_map)
    height_map = (height_map - min_elevation) / (max_elevation - min_elevation)
    return height_map


def calculate_temperature(radius, altitude):
    solar_constant = 1361  # Solar constant in W/m^2
    stefan_boltzmann = 5.67e-8  # Stefan-Boltzmann constant in W/(m^2 K^4)

    temperature = math.sqrt(radius / (radius + altitude))

    temperature *= math.sqrt(solar_constant / stefan_boltzmann)

    return temperature

