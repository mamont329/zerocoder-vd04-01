from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    now = datetime.now()
    return render_template(
        "index.html",
        date=now.strftime("%d.%m.%Y"),
        time=now.strftime("%H:%M:%S"),
    )


if __name__ == "__main__":
    app.run(debug=True)
