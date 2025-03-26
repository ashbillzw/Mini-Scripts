import pykakasi

source_lines = open("in.wikitext", 'r', encoding="utf-8").readlines()

result_text = str()

for line in source_lines:
    if '·' in line:
        print(f"WARN: Interpunct replaced at line {line[:10]}...")
        line = line.replace('·', '・')

    for word in pykakasi.kakasi().convert(line):
        if word["orig"] == '\n':
            result_text += '\n'
            break

        if not len(word["hira"]):
            print(f"WARN: Ignoring {word['orig']}")
            result_text += word["orig"]
            continue
        
        if word["orig"][0] in (word["hira"][0], word["kana"][0]):
            result_text += word["orig"]
            continue

        for index, (orig, hira, kana) in enumerate(zip(word["orig"][::-1], word["hira"][::-1], word["kana"][::-1])):
            if orig not in (hira, kana):
                kanjis = word["orig"][:-index or None]
                furigana = word["hira"][:-index or None]

                for fg_index, char in enumerate(furigana):
                    kj_index = kanjis.find(char) # Okurigana
                    if kj_index != -1:
                        print(f"WARN: Replaced {kanjis} with {kanjis[:kj_index]}({furigana[:fg_index]}), {kanjis[kj_index]}, and {kanjis[kj_index+1:]}({furigana[fg_index+1:]})")
                        result_text += f"{{{{Photrans2|{kanjis[:kj_index]}|{furigana[:fg_index]}}}}}{char}"
                        kanjis, furigana = kanjis[kj_index+1:], furigana[fg_index+1:]

                result_text += f"{{{{Photrans2|{kanjis}|{furigana}}}}}{word['orig'][-index or len(word['orig']):]}"
                break

common_corrections = {
    "|君|くん": "きみ",
    "|人|にん": "ひと",
    "|日|にち": "ひ",
    "{{Photrans2|行|い}}こう": "{{Photrans2|行|ゆ}}こう"
}

return_text = ""
for index, line in enumerate(result_text.splitlines()):

    for find, replace in common_corrections.items():
        if find[0] == '|':
            find = "{{Photrans2" + find + "}}"
            replace = "{{Photrans2|" + find.split('|')[1] + '|' + replace + "|}}"
        if line.find(find) != -1:
            line = line.replace(find, replace)
            print(f"WARN: Replaced {find} with {replace} at line {index+1}")

    return_text += line + "\n"

open("out.wikitext", 'w', encoding="utf-8").write(return_text[:-1])
