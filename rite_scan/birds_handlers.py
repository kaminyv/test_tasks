import json
from java import jclass

noClass = jclass("ru.travelfood.simple_ui.NoSQL")
ncl = noClass("db_birds")

def birds_on_start(hashMap, _files=None, _data=None):
    birds_cards = {"cards": []}
    db_keys = json.loads(ncl.getallkeys())
    for key in db_keys:
        db_data = json.loads(ncl.get(key))
        birds_cards["cards"].append({
            "key": key,
            "picture": "",
            "description": "",
            "items": [
                {
                    "key": "Название птицы",
                    "value": key,
                    "size": "18",
                    "color": "#1b31c2",
                },
                {
                    "key": "Цвет оперения",
                    "value": db_data.get("feather_color"),
                    "size": "18",
                    "color": "#1b31c2"
                }]
            })

    hashMap.put("birds_list",json.dumps(birds_cards))
         
    return hashMap


def birds_input(hashMap, _files=None, _data=None):
    if hashMap.get("listener") == "btn_add":
        hashMap.put("name", "")
        hashMap.put("feather_color", "")
        hashMap.put("ShowScreen", "ПтицыЗапись")
    elif hashMap.get("listener") == "btn_db_clean":
        ncl.destroy()
        hashMap.put("toast", "База очищена")
    elif hashMap.get("listener")=="CardsClick":
        key = hashMap.get("selected_card_key")
        db_data = json.loads(ncl.get(key))
        hashMap.put("name", key)
        hashMap.put("feather_color", db_data.get("feather_color"))
        hashMap.put("ShowScreen", "ПтицыЗапись")

    return hashMap


def bird_record_on_start(hashMap, _file=None, _data=None):
    if not hashMap.containsKey("name"):
        hashMap.put("name", "")
    if not hashMap.containsKey("feather_color"):
        hashMap.put("feather_color", "")
    return hashMap


def bird_record_input(hashMap, _file=None, _data=None):   
    if hashMap.get("listener") == "btn_save":
        if len(hashMap.get("name")) == 0 or len(hashMap.get("feather_color")) == 0:
            hashMap.put("toast", "Не заполнены поля")
        else:
            data = {
                "feather_color": hashMap.get("feather_color")}
            ncl.put(hashMap.get("name"), json.dumps(data ,ensure_ascii=False), True)
            hashMap.put("ShowScreen", "Птицы")
    elif hashMap.get("listener") == "menu_del":
        ncl.delete(hashMap.get("name"))
        hashMap.put("ShowScreen","Птицы")

    return hashMap


def init(hashMap, _files=None, _data=None):
    ncl.run_index("nameindex","name")
    return hashMap
