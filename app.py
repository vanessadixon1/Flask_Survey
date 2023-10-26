from flask import Flask, request, render_template, redirect, flash, session


import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secet"

question_len = 0

@app.route("/")
def home():
   info = surveys.personality_quiz
   if not session.get("response"):
        session["response"] = []

   return render_template("homepage.html", info = info)

@app.route("/questions/<id>")
def question(id):
    global question_len
    info = surveys.personality_quiz
    question_len = len(info.questions)

    url_id = int(request.url.split("/")[-1])
    
    if url_id > question_len:
        flash("Ivalid Pick!", 'error')
        return redirect(f"/questions/{len(session['response'])}")

    indx = int(id)
    
    response =  render_template("form.html", info = info.questions[indx])

    return response

@app.route("/answer", methods=['POST'])
def answer():
    try:
        if request.form.get("q", False):
            s = session["response"]
            s.append(request.form["q"])
            session["response"] = s

        while question_len > len(session["response"]):
            return redirect(f"/questions/{len(session['response'])}")

        flash("Thank You!", 'success')
        return redirect("/")  
    except:
        raise
