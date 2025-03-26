import json, math, sys


STACK_SIZE = 64
WHEEL_RPM = 256


try:
    recipe_duration = sys.argv[1]
except IndexError:
    recipe_duration = input("Pleace specify recipe or recipe duration (e.g. 'cactus', '50', etc.): ")


try:
    recipe_duration = int(recipe_duration)
except ValueError:
    with open("crushing_wheel_recipe_durations.json") as file:
        recipe_duration = json.loads(file.read())[recipe_duration]


tps = ticks_per_stack = (recipe_duration - 20) / max(0.25, min(WHEEL_RPM * 0.08 / math.log(STACK_SIZE, 2), 20)) + 1


print(
    "",
    "(Assuming STACK_SIZE=64 and WHEEL_RPM = 256) Processing speed:",
    "",
    f"{tps:.2f} ticks per stack",
    f"{tps / 20:.2f} seconds per stack",
    "",
    f"{STACK_SIZE / tps:.2f} items per tick",
    f"{20 / tps:.2f} stacks per second",
    f"{1200 / tps:.2f} stacks per minute",
    sep = '\n'
)
