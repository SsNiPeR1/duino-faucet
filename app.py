import numbers
from flask import Flask, render_template, request, send_file
import json
import os
from numpy import number
import requests
from captcha.image import ImageCaptcha
import random

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

@app.route("/captcha")
def cpth():
    numbers = random.randint(1, 1000000)
    global validcaptchas
    validcaptchas = []
    validcaptchas.append(str(numbers))
    image = ImageCaptcha(fonts=["static/arial.ttf"])
    data = image.generate(str(numbers))
    return send_file(data, mimetype="image/png")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if str(request.form.get('captcha')) in validcaptchas:
                data = requests.get(f"https://server.duinocoin.com/transaction?username={user}&password={password}&recipient={request.form.get('textbox')}&amount=0.01&memo=Free%20coins%20from%20faucet").text
                retdata = str(json.loads(data)['success'])
                if "True" in retdata:
                    validcaptchas.remove(request.form.get('captcha'))
                    return render_template("success.html", sent=request.form.get('textbox'))
                else:
                    validcaptchas.remove(request.form.get('captcha'))
                    return render_template("failure.html", sent=request.form.get('textbox'))

            else:
                return "Invalid token."
        except:
            return "Invalid token."

    jsondata = requests.get(f"https://server.duinocoin.com/balances/{user}").text
    jsonobj = json.loads(jsondata)
    balance = jsonobj['result']['balance']

    return render_template("index.html", balance=balance)

if __name__ == "__main__":
    app.run()