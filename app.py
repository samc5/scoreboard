import requests
import json
from humanize import number
import threading
import time
from flask import Flask, render_template, request, Response, session, redirect
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

app.secret_key = "6gBvzKwE8RWOt6amHzNz"

#def 

def check_bases(base_array):
    output = ""
    if base_array[0] == 1:
        output += "There's a runner on first. "
    if base_array[1] == 1:
        output += "There'es a runner on second. "
    if base_array[2] == 1:
        output += "There'es a runner on third. "
    if base_array[0] == 0 and base_array[1] == 0 and base_array[2] == 0:
        return "no-one on"
    return output

def color_bases(base_array):
    output = []
    for i in range(3):
        if base_array[i] == 1:
            output.append("#EFB21F")
        else:
            output.append("#888888")
    return output
@app.context_processor
def requester():
    game_file = open("game.txt", "r")
    game_url = game_file.read()
    game_file.close()

    #url = "https://push.gamechanger.io/push/game/64066eb0d12b5e9d6600000c/stream/64066eb0d12b5e9de2000010?index=0&sabertooth_aware=true"
    r = requests.get(game_url)
    data = r.json()
    #print(data['game']['accounts'][0])


    home_score = data['game']['accounts'][0]['scores'][0]['score']
    away_score = data['game']['accounts'][0]['scores'][1]['score']

    balls = data['game']['accounts'][0]['state']['count']['balls']
    strikes = data['game']['accounts'][0]['state']['count']['strikes']
    outs = data['game']['accounts'][0]['state']['count']['outs']

    inning = data['game']['accounts'][0]['state']['inning']
    inning_suffix = number.ordinal(inning)

    pitcher_first = "No pitcher"
    pitcher_last = "No pitcher"
    batter_first = "No batter"
    batter_last = "No batter"

    json_string = json.dumps(data)
    data = json.loads(json_string)
    if data['game']['accounts'][0]['state']['pitcher'] != None:
        pitcher_first = data['game']['accounts'][0]['state']['pitcher']['first_name']
        pitcher_last = data['game']['accounts'][0]['state']['pitcher']['last_name']
    if data['game']['accounts'][0]['state']['batter'] != None:
        batter_first = data['game']['accounts'][0]['state']['batter']['first_name']
        batter_last = data['game']['accounts'][0]['state']['batter']['last_name']

    base_array = [0,0,0]
    bases_unclear = data['game']['accounts'][0]['state']['bases']
    
    for i in bases_unclear:
        base = i["base"]
        base_last = i["player"]["last_name"]
        base_array[base-1] = 1
    base_text = check_bases(base_array)
    base_colors = color_bases(base_array)
    half = data['game']['accounts'][0]['state']['half']
    if half == 0:
        half_inning = "top"
    else:
        half_inning = "bottom"
    print(base_colors)
    return {'base_colors':base_colors,'base_text':base_text, 'home':home_score,'away':away_score,'half':half_inning,'inning':inning,'balls':balls,'strikes':strikes,'outs':outs,'pitcher_first':pitcher_first,'pitcher_last':pitcher_last,'batter_first':batter_first,'batter_last':batter_last}



@app.route("/", methods = ["POST", "GET"])
def display():
    stream_file = open("stream.txt", "r")
    stream_url = stream_file.read()
    print(stream_url)
    stream_file.close()
    return render_template("index.html", stream = stream_url)

@app.route("/input2", methods = ["POST", "GET"])
def display2():
    game = request.form["game"]
    stream = request.form["stream"]
    code = request.form["code"]
    #print(f'Game: {game}, stream: {stream}')
    if code == "3007":
        stream_file = open("stream.txt", "w")
        stream_file.write(f'{stream}')
        stream_file.close()
        game_file = open("game.txt", "w")
        game_file.write(f'{game}')
        game_file.close()
    #time.sleep(2)
    return redirect("/")

def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('scoreboard.html'), 'sb'))

th = threading.Thread(target=update_load)
th.daemon = True
th.start()

# if __name__ == "__main__":
#     app.debug = True
#     app.run()