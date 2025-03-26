import time

import pyautogui


coordinates = (0, 0, 0)
facing = "north"
dimensions = (2, 2)
head = 0

glow = True
tag = "mapart-temp"

debug_mode = False
delay_at_start = 3
delay_between_step = 0.1


time.sleep(delay_at_start)
print("starting...")


for dh in range(dimensions[1]):
    for dw in range(dimensions[0]):

        pyautogui.press('t')
        time.sleep(delay_between_step)

        pyautogui.typewrite(
            "/summon minecraft:" + ("glow_" if glow else '') + "item_frame " + ' '.join(
                str(coordinates[axis] + {
                    "top": (dw, 0, -dh), "bottom": (dw, 0, dh), "east": (0, -dh, dw), "south": (-dw, -dh, 0), "west": (0, -dh, -dw), "north": (dw, -dh, 0)
                }[facing][axis]) for axis in range(3)
            ) + " {Facing:" + str({
                    "top": 0, "bottom": 1, "east": 4, "south": 2, "west": 5, "north": 3
                }[facing]
            ) + f",Item:{{id:\"minecraft:filled_map\",Count:1,tag:{{map:{head}}}}},Tags:[\"{tag}\"]}}"
        )
        time.sleep(delay_between_step)

        pyautogui.press('enter')
        time.sleep(delay_between_step)

        if debug_mode:
            input("waiting...")
            time.sleep(delay_at_start)

        head += 1

print("done.")
