from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)


@app.route("/")
def initial():
    return redirect(url_for("welcome"))


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


if __name__ == "__main__":
    app.run()
