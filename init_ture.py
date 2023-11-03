import json

f1 = open("config/set.json", mode="r")
f2 = open("config/img.json", mode="r")
f3 = open("config/sound.json", mode="r")
f4 = open("config/map.json", mode="r")
content1 = f1.read()
content2 = f2.read()
content3 = f3.read()
content4 = f4.read()
f1.close()
f2.close()
f3.close()
f4.close()
Config = {"SETTING": json.loads(content1), "IMG": json.loads(content2), "SOUND": json.loads(content3),
          "MAP": json.loads(content4)}
with open("localization/" + Config["SETTING"]["language"] + ".json", 'r', encoding='utf-8') as f5:
    content = f5.read()
f5.close()
T = json.loads(content)
del content4, content3, content2, content1
