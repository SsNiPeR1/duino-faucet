from flask import Flask, render_template, request
import json
import os
import requests

app = Flask(__name__)

if not os.path.exists("settings.json"):
    settings = open("settings.json", "w")

    user = input("Enter your username for faucet: ")
    password = input("Enter your password for faucet:")
    
    data = {"username":user,
            "password":password}
    
    setn = json.dumps(data)
    settings.write(setn)
    settings.close()

else:
    creds = json.loads(open("settings.json", "r").read())
    user = creds["username"]
    password = creds["password"]
    print(user)
    print(password)

@app.route("/style.css")
def css():
    return open("static/style.css", "r").read()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = requests.get(f"https://server.duinocoin.com/transaction?username={user}&password={password}&recipient={request.form.get('textbox')}&amount=0.01&memo=Free%20coins%20from%20faucet").text
        retdata = str(json.loads(data)['success'])
        if "True" in retdata:
            return render_template("success.html", sent=request.form.get('textbox'))
        else:
            return render_template("failure.html", sent=request.form.get('textbox'))

    jsondata = requests.get(f"https://server.duinocoin.com/balances/{user}").text
    jsonobj = json.loads(jsondata)
    balance = jsonobj['result']['balance']

    return render_template("index.html", balance=balance)

if __name__ == "__main__":
    app.run()