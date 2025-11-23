from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)


@app.route("/")
def initial():
    return redirect(url_for("welcome"))


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/stirring")
def stirring():
    return render_template("stirring.html")

@app.route("/temperature")
def temperature():
    return render_template("temperature.html")

@app.route("/ph")
def ph():
    return render_template("ph.html")


if __name__ == "__main__":
    app.run()
