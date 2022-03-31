from flask import Flask,request,redirect,render_template,flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

@app.route("/")
def details():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("root.html", title = title, instructions = instructions)

@app.route("/questions/<int:qid>")
def add_questions(qid):
    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/complete")
    if qid != len(responses):
        flash(f"Invalid question id: {qid}.")
        return redirect(f'/questions/{len(responses)}')
    question = satisfaction_survey.questions[qid].question
    choices = satisfaction_survey.questions[qid].choices
    return render_template ( "questions.html", qid = qid, questions = question, choices = choices )

@app.route("/answer", methods = ["POST"])
def next():
    choice = request.form["answer"]
    responses.append(choice)
    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/complete")
    return redirect(f'/questions/{len(responses)}')

@app.route("/complete")
def thanks():
    return render_template("thanksyou.html")