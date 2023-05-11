from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates')


@app.route("/")
def hello_world():
    manager = app.config['MQTT']
    objects = manager.objects
    return render_template('template.html', data=objects)
