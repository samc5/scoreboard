import requests
from humanize import number
from flask import Flask, render_template, request, Response, session, redirect
from turbo_flask import Turbo
import threading
import time
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

@app.before_first_request
def before_first_request():
    pass
    #threading.Thread(target=?).start()

@app.route("/", methods = ["POST", "GET"])
def display():
    #r = requests.get("https://push.gamechanger.io/push/game/629688bbf99f001df3000789/stream/629688bbf996007c590007a3?index=0&sabertooth_aware=true")
    
    r = requests.get("https://push.gamechanger.io/push/game/64066eb0d12b5e9d6600000c/stream/64066eb0d12b5e9de2000010?index=0&sabertooth_aware=true")
    data = r.json()
    #print(data['game']['accounts'][0])


    home_score = data['game']['accounts'][0]['scores'][0]['score']
    away_score = data['game']['accounts'][0]['scores'][1]['score']

    balls = data['game']['accounts'][0]['state']['count']['balls']
    strikes = data['game']['accounts'][0]['state']['count']['strikes']
    outs = data['game']['accounts'][0]['state']['count']['outs']

    inning = data['game']['accounts'][0]['state']['inning']
    inning_suffix = number.ordinal(inning)

    pitcher_first = data['game']['accounts'][0]['state']['pitcher']['first_name']
    pitcher_last = data['game']['accounts'][0]['state']['pitcher']['last_name']
    batter_first = data['game']['accounts'][0]['state']['batter']['first_name']
    batter_last = data['game']['accounts'][0]['state']['batter']['last_name']
    base_array = [0,0,0]
    bases_unclear = data['game']['accounts'][0]['state']['bases']
    
    for i in bases_unclear:
        base = i["base"]
        base_last = i["player"]["last_name"]
        base_array[base-1] = 1
    base_text = check_bases(base_array)
    half = data['game']['accounts'][0]['state']['half']
    if half == 0:
        half_inning = "top"
    else:
        half_inning = "bottom"

    print(f'The score is {home_score} to {away_score} in the {half_inning} of the {inning_suffix} inning, the count is {balls}-{strikes}, with {outs} outs.\n{pitcher_first} {pitcher_last} is facing hitter {batter_first} {batter_last}')
    return render_template("index.html", base_text = base_text, home=home_score,away=away_score,half=half_inning,inning=inning,balls=balls,strikes=strikes,outs=outs,pitcher_first=pitcher_first,pitcher_last=pitcher_last,batter_first=batter_first,batter_last=batter_last)




if __name__ == "__main__":
    app.debug = True
    app.run()