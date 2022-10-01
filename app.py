from model import give_rec
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        anime_title = request.form["title"]
        try:
            rec_names = give_rec(anime_title).to_html()
        except:
            rec_names = give_rec(anime_title)
        return render_template("index.html",rec_names=rec_names)
    return render_template("index.html")

@app.route('/table.html')
def table():
    return render_template("table.html")

if __name__ == "__main__":
    app.run()
