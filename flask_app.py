from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pywebostv.discovery import *
from pywebostv.connection import *
from pywebostv.controls import *


app = Flask(__name__)
CORS(app, cors_allowed_source='*')

client = None
media_control = None
system_control = None
input_control = None
store = {}
mute_status = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/discover', methods=['POST'])
def discover():
    global client, media_control, system_control, input_control
    try:
        client = WebOSClient.discover()[0]
        client.connect()
        for status in client.register(store):
            if status == WebOSClient.PROMPTED:
                print("Please accept the connect on the TV!")
            elif status == WebOSClient.REGISTERED:
                print("Registration successful!")
            media_control = MediaControl(client)
            system_control = SystemControl(client)
            input_control = InputControl(client)
            return jsonify(success=True)
    except Exception as e:
        print(f"Error discovering and connecting to TV: {str(e)}")
        return jsonify(success=False)


@app.route('/control', methods=['POST'])
def control():
    command = request.json['command']
    try:
        if command == 'power':
            system_control.power_off()
        elif command == 'vol+':
            media_control.volume_up()
        elif command == 'vol-':
            media_control.volume_down()
        elif command == 'mute':
            global mute_status
            if mute_status == False:
                media_control.mute(True)
                mute_status = True
            else:
                media_control.mute(False)
                mute_status = False
        elif command == 'channel_up':
            media_control.channel_up()
        elif command == 'channel_down':
            media_control.channel_down()
        elif command == 'home':
            input_control.connect_input()
            input_control.home()
            input_control.disconnect_input()
        elif command == 'up':
            input_control.connect_input()
            input_control.up()
            input_control.disconnect_input()
        elif command == 'down':
            input_control.connect_input()
            input_control.down()
            input_control.disconnect_input()
        elif command == 'left':
            input_control.connect_input()
            input_control.left()
            input_control.disconnect_input()
        elif command == 'right':
            input_control.connect_input()
            input_control.right()
            input_control.disconnect_input()
        elif command == 'ok':
            input_control.connect_input()
            input_control.ok()
            input_control.disconnect_input()
        elif command == 'back':
            input_control.connect_input()
            input_control.back()
            input_control.disconnect_input()
        else:
            return jsonify(success=False, message='Invalid command')
        return jsonify(success=True)
    except Exception as e:
        print(f"Error sending command: {str(e)}")
        return jsonify(success=False, message='Error sending command')


if __name__ == '__main__':
    app.run(debug=True)
