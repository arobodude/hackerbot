import json
from flask import Flask, request, jsonify
from hackerbot.hackerbot import HackerBot

app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps({'name': 'HACKERBOT'})

@app.route('/init/', methods = ['POST'])
def init_command():
    result = hackerbot.init_command()
    if result:
        return jsonify({'response': 'INIT Command Successful'})
    return jsonify({'error': 'Could not initaliaze robot connection'})

@app.route('/goto/', methods=['POST'])
def goto_command():
    data = json.load(request.data)
    x_coord = data['x_coord']
    y_coord = data['y_coord']
    angle = data['angle']
    speed = data['speed']
    result = hackerbot.goto_command(x_coord, y_coord, angle, speed)
    if result:
        return jsonify({'response': 'GOTO Command Successful'})
    return jsonify({'error': 'Could not send GOTO command to device'})

@app.route('/dock/', methods = ['POST'])
def dock_command():
    result = hackerbot.dock_command()
    if result:
        return jsonify({'response': 'DOCK Command Successful'})
    return jsonify({'error': 'Could not send dock command to device'})

@app.route('/ping/', methods=['GET'])
def ping_command():
    result = hackerbot.ping_command()
    if result:
        return jsonify({'response': 'PING Command Successful'})
    return jsonify({'error': 'Could not ping device'})

@app.route('/raw-command/', methods =['POST'])
def raw_command():
    data = json.load(request.data)
    result = hackerbot.send_command(data['command'])
    if result:
        return jsonify({'response': 'Raw Command Successful'})
    return jsonify({'error': 'Could not send raw command to device'})

@app.route('/getml/', methods=['GET'])
def get_map_list_command():
    result = hackerbot.get_ml_command()
    if result:
        return jsonify({'response': 'Raw Command Successful'})
    return jsonify({'error': 'Could not get map list from device'})

@app.route('/play-audio/', methods = ['POST'])
def play_audio_command():
    data = json.load(request.data)
    audio_file = data['audio_file']
    result = hackerbot.play_audio_file(audio_file)
    if result:
        return jsonify({'response': 'Play Audio File Successful'})
    return jsonify({'error': 'Could not play audio file on device'})


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
    hackerbot = HackerBot()
