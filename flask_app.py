import pickle
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pywebostv.discovery import *
from pywebostv.connection import *
from pywebostv.controls import *
import socket
import time

app = Flask(__name__)
CORS(app, cors_allowed_source='*')

client = None
media_control = None
system_control = None
input_control = None
app_control = None
store = {}
mute_status = False
power_status = True


def loadStore():
    with open('store.pkl', 'rb') as f:
        try:
            store = pickle.load(f)
        except:
            print("Empty")
            store = None
    return store


def writeStore(store):
    with open('store.pkl', 'wb') as f:
        pickle.dump(store, f)


if loadStore():
    store = loadStore()
    print(store)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/discover', methods=['POST'])
def discover():
    global client, media_control, system_control, input_control, app_control, store
    try:
        send_wol_packet('C0:D7:AA:91:B5:02')
        print('Waking up the TV..')
        time.sleep(2)
        print("starting discovery...")
        client = WebOSClient.discover()[0]
        print(f'{client} found')
        client.connect()
        print(f'Connetciton with {client} completed.')
        for status in client.register(store):
            if status == WebOSClient.PROMPTED:
                print("Please accept the connect on the TV!")
            elif status == WebOSClient.REGISTERED:
                print("Registration successful!")
            media_control = MediaControl(client)
            system_control = SystemControl(client)
            input_control = InputControl(client)
            app_control = ApplicationControl(client)
        print(store)
        writeStore(store)
        return jsonify(success=True)
    except Exception as e:
        print(f"Error discovering and connecting to TV: {str(e)}")
        return jsonify(success=False)


@app.route('/control', methods=['POST'])
def control():
    command = request.json['command']
    try:
        if command == 'power':
            global power_status
            if power_status == True:
                system_control.power_off()
                power_status = False
            else:
                send_wol_packet('C0:D7:AA:91:B5:02')
                power_status = True
                print("Magic Packet Sent")
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
            systemState()
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
        elif command == 'netflix':
            # Returns a list of `Application` instances.
            apps = app_control.list_apps()

            # Let's launch YouTube!
            ntf = [x for x in apps if "netflix" in x["title"].lower()][0]
            launch_info = app_control.launch(ntf)
        else:
            return jsonify(success=False, message='Invalid command')
        return jsonify(success=True)
    except Exception as e:
        print(f"Error sending command: {str(e)}")
        return jsonify(success=False, message='Error sending command')


def systemState():
    print(system_control.info())


def send_wol_packet(mac_address):
    # Check MAC address format and convert it to a clean format
    mac_address = ''.join(mac_address.split(':'))

    # Create a magic packet
    # The magic packet contains 6 bytes of 255 followed by 16 repetitions of the MAC address
    data = 'FF' * 6 + mac_address * 16
    magic_packet = bytes.fromhex(data)

    # Create a socket for network broadcast
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Send it to the broadcast address with the port typically used for WOL (port 9)
        sock.sendto(magic_packet, ('255.255.255.255', 9))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
