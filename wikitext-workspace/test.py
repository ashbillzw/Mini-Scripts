import pykakasi

source = "ワン·ツー·スリー"
result = pykakasi.kakasi().convert(source)

for word in result:
    print(word["hira"], end=',')
