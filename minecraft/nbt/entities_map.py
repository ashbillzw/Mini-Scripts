# this junk is vibe code, use at your own risk

import ast
import pandas as pd
from PIL import Image, ImageDraw

MIN_C = -192
MAX_C = 192

df = pd.read_csv("chunks.csv")

def color_for(n: int):
    if n >= 32:
        return (255, 0, 0, 255)
    if n >= 16:
        return (255, 127, 0, 255)
    if n >= 8:
        return (255, 255, 0, 255)
    return (0, 0, 0, 0)

coords = df["chunk"].map(ast.literal_eval)
df["cx"] = coords.map(lambda t: int(t[0]))
df["cz"] = coords.map(lambda t: int(t[1]))
df["count"] = df["count"].astype(int)

df = df[df["cx"].between(MIN_C, MAX_C) & df["cz"].between(MIN_C, MAX_C)]
df = df.groupby(["cx", "cz"], as_index=False)["count"].sum()

span = MAX_C - MIN_C + 1
img = Image.new("RGBA", (span, span), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

for cx, cz, n in df[["cx", "cz", "count"]].itertuples(index=False, name=None):
    col = color_for(n)
    if col[3] == 0:
        continue
    x = cx - MIN_C
    y = cz - MIN_C
    draw.point((x, y), fill=col)

img.save("chunks.png")
