from flask import Flask, request, render_template, redirect, flash, jsonify

import socket

import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secet"


res = []
iden = 0
question_len = 0
socket.setdefaulttimeout(5)

@app.route("/")
def home():
   info = surveys.personality_quiz

   return render_template("homepage.html", info = info)

@app.route("/questions/<id>")
def question(id):
    global iden
    global question_len
    info = surveys.personality_quiz
    question_len = len(info.questions)

    url_id = int(request.url.split("/")[-1])
    
    if url_id > question_len:
        print(res)
        indx = 0
        iden = indx
        res.clear()
        flash("Ivalid Pick!", 'error')
        return redirect(f"/questions/{len(res)}")

    indx = int(id)
    
    response =  render_template("form.html", info = info.questions[indx])

    return response

@app.route("/answer", methods=['POST'])
def answer():
    try:
        global iden
        if request.form["q"]:

            res.append(request.form["q"])

        iden += 1
        while question_len > iden:
            return redirect(f"/questions/{iden}")

        iden=0
        res.clear()
        flash("Thank You!", 'success')
        return redirect("/")  
    except:
        raise
    
  