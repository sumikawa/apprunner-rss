from app import getlist
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
  return "test"

@app.route("/rss")
def rss():
  return(getlist())

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=4567, debug=True)
