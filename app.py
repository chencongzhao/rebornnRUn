from flask import Flask, request
from app import demo

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return demo(request)

if __name__ == "__main__":
    app.run(debug=True)
