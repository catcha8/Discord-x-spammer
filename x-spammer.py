import requests, json, threading, random, time,sys,websocket,os

os.system("cls")
#servid= input("servid: ")

channid= int(input("channid: "))

counter = 0
proxys = []

WORDS = ["**BAHAHHA**", "**BAHAHHA**", "**BAHAHHA**"]

ID = ["884117157879877693"]

def connect(token):
    global counter
    header = { "Authorization": str(token).replace("\n", ""),
               "Content-type": "application/json",
            }

    msg = ""

    for x in ID:
        msg += f"<@{x}> "

    data = {"content": f"{msg} **SEND LES T0KENS EN MP STP <3**" } #f"{random.choice(WORDS)}"}
                                                    
    #  NSL chat "https://discord.com/api/v9/channels/971495740268511244/messages"

    for x in range(1000000):
        r = requests.post(f"https://discord.com/api/v9/channels/{channid}/messages", headers=header, json=data)
        if r.status_code == 200:
            counter +=1
            print(counter)
        time.sleep(.3)


def changegame(token, game, type, status):
    #print("Done " + token)
    ws = websocket.WebSocket()
    if status == "random":
        stat = ['online', 'dnd', 'idle']
        status = random.choice(stat)
    ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
    hello = json.loads(ws.recv())
    heartbeat_interval = hello['d']['heartbeat_interval']
    if type == "Playing":
        gamejson = {
            "name": game,
            "type": 0
        }
    elif type == 'Streaming':
        gamejson = {
            "name": game,
            "type": 1,
            "url": "https://www.twitch.tv/catcha80"
        }
    elif type == "Listening to":
        gamejson = {
            "name": game,
            "type": 2
        }
    elif type == "Watching":
        gamejson = {
            "name": game,
            "type": 3
        }
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": sys.platform,
                "$browser": "RTB",
                "$device": f"{sys.platform} Device"
            },
            "presence": {
                "game": gamejson,
                "status": status,
                "since": 0,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }
    ws.send(json.dumps(auth))
    ack = {
        "op": 1,
        "d": None
    }
    while True:
        time.sleep(heartbeat_interval / 1000)
        try:
            ws.send(json.dumps(ack))
        except Exception as e:
            break



f = open("tokens.txt", 'r')

for token in f:
    #print("CONNECTING TO TOKEN: ", token)
    type = "Playing"
    game = "discord.gg/catcha"
    status = ['online', 'dnd', 'idle','random']
    status = status[3]
    threading.Thread(target=connect, args=(token,)).start()
    threading.Thread(target=lambda : changegame(token.replace("\n",""), game, type, status)).start()
