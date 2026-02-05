import pathlib
import csv

import anvil # pip install anvil-parser2


root = pathlib.Path("entities") # /path/to/entities


with open("entities.csv", "w", newline="", encoding="utf-8") as entities_file, \
     open("chunks.csv", "w", newline="", encoding="utf-8") as chunks_file:
    entities_writer = csv.writer(entities_file)
    entities_writer.writerow(["uuid", "id", "x", "y", "z"])
    chunks_writer = csv.writer(chunks_file)
    chunks_writer.writerow(["chunk", "count"])

    for path in root.rglob("*.mca"):
        try:
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
                        print("Failed to read region's chunk: ", path, (x, z))
        except Exception as error:
            print("Failed to read region file: ", path, error)
            continue
