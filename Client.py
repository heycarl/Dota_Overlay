import requests
import json
import variables
from threading import Thread


def get_data():
    while 1:
        try:
            response = json.load(open("data/response.json"))
            variables.draft = response['draft']
            variables.heroes = response['hero']
            variables.players = response['player']
            variables.items = response['items']
            variables.map_provider = response['map']
        except json.decoder.JSONDecodeError:
            pass
        except KeyError:
            pass


def stats():
    while 1:
        try:
            data = "GPM: " + str(selected_unit(1)['gpm']) + "\nXPM: " + str(selected_unit(1)['xpm']) + "\nKILL STREAK: "\
                   + str(selected_unit(1)['kill_streak'])
            requests.get(
                "http://127.0.0.1:8088/API/?Function=SetText&Input=stats&SelectedName=textBlock&Value=" + str(data))
        except TypeError:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except KeyError:
            pass


def smokes():
    while 1:
        for team in variables.heroes:
            for player in variables.heroes[team]:
                id = int(str(player)[-1])
                try:
                    if variables.heroes[team][player]['smoked']:
                        if variables.smoked[id] == 1:
                            pass
                        else:
                            requests.get(
                                "http://127.0.0.1:8088/API/?Function=MultiViewOverlayOn&Input=smoke&Value=" +
                                str(id + 1))
                            # print(str(id + 1) + " False -> True")
                        variables.smoked[id] = 1
                    else:
                        if variables.smoked[id] == 0:
                            pass
                        else:
                            requests.get(
                                "http://127.0.0.1:8088/API/?Function=MultiViewOverlayOff&Input=smoke&Value=" +
                                str(id + 1))
                            # print(str(id + 1) + " True -> False")
                        variables.smoked[id] = 0
                except requests.exceptions.ConnectionError:
                    pass


def aegis():
    while 1:
        for team in variables.items:
            for player in variables.items[team]:
                id = int(str(player)[-1])
                for slot in variables.items[team][player]:
                    slot_id = int(str(slot)[-1])
                    if variables.items[team][player][slot]['name'] == 'item_aegis':
                        if variables.aegis_slot[id] == 20:
                            requests.get(
                                "http://127.0.0.1:8088/API/?Function=MultiViewOverlayOn&Input=aegis&Value=" +
                                str(id + 1))
                            # print("Aegis in " + str(slot_id) + " on " + str(variables.heroes[team][player]['name']))
                            variables.aegis_slot[id] = slot_id
                    else:
                        if variables.aegis_slot[id] != 20 and variables.aegis_slot[id] == slot_id \
                                and slot[0:5] != "stash":
                            requests.get(
                                "http://127.0.0.1:8088/API/?Function=MultiViewOverlayOff&Input=aegis&Value=" +
                                str(id + 1))
                            # print("Aegis is not " + " on " + str(variables.heroes[team][player]['name']))
                            variables.aegis_slot[id] = 20


def selected_unit(response_type):
    for team in variables.heroes:
        for player in variables.heroes[team]:
            if variables.heroes[team][player]['selected_unit']:
                if response_type == 0:
                    return variables.heroes[team][player]
                elif response_type == 1:
                    return variables.players[team][player]


thread1 = Thread(target=get_data)
thread2 = Thread(target=stats)
thread3 = Thread(target=smokes)
thread4 = Thread(target=aegis)
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.start()
