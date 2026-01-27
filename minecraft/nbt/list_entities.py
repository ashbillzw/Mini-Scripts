import pathlib
import csv

import anvil # pip install anvil-parser2


root = pathlib.Path("D:\\Program Files\\PCL2\\.minecraft\\versions\\新岛铁道 v1.5.1 AshBill版\\saves\\create-cn_world_2026-01-25_DATA\\entities") # /path/to/entities


with open("entities.csv", "w", newline="", encoding="utf-8") as entities_file, \
     open("chunks.csv", "w", newline="", encoding="utf-8") as chunks_file:
    entities_writer = csv.writer(entities_file)
    entities_writer.writerow(["uuid", "id", "x", "y", "z"])
    chunks_writer = csv.writer(chunks_file)
    chunks_writer.writerow(["chunk", "count"])

    for path in root.rglob("*.mca"):
        region = anvil.Region.from_file(str(path))
        for x in range(32):
            for z in range(32):
                try:
                    nbt = region.chunk_data(x, z)
                    if nbt is not None:
                        entities = nbt["Entities"]
                        chunks_writer.writerow([nbt["Position"].value, len(entities)])
                        for entity in entities:
                            uuid = 0
                            for n in entity["UUID"].value:
                                uuid = uuid << 32 | n & 0xFFFFFFFF
                            uuid = f"{uuid:032x}"
                            id = entity.get("id")
                            pos = [d.value for d in entity.get("Pos")]
                            print(uuid, id, pos)
                            entities_writer.writerow([uuid, id] + pos)

                except IndexError:
                    print("Failed to read region: ", path, (x, z))
