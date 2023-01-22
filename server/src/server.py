from flask import Flask
from .postgres_connector import conn

app = Flask(__name__)


@app.route("/")
def hello_world():
    cur = conn.cursor()
    cur.execute("SELECT * FROM detected_objects")
    result = cur.fetchall()
    cur.close()
    return f'<p>Detected objects: {result}</p>'