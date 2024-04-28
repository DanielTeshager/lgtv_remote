from pywebostv.discovery import *
from pywebostv.connection import *
from pywebostv.controls import *
from app.utils import send_wol_packet
from config import TV_MAC_ADDRESS
import time


client = None
media_control = None
system_control = None
input_control = None
app_control = None
mute_status = False
power_status = False


def discover_tv(store):
    global client, media_control, system_control, input_control, app_control
    send_wol_packet(TV_MAC_ADDRESS)
    print('Waking up the TV...')
    time.sleep(2)
    print("Starting discovery...")
    client = WebOSClient.discover()[0]
    print(f'{client} found')
    client.connect()
    print(f'Connection with {client} completed.')

    if store is None:
        store = {}

    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
            yield "prompted"
        elif status == WebOSClient.REGISTERED:
            print("Registration successful!")
            yield "registered"
    media_control = MediaControl(client)
    system_control = SystemControl(client)
    input_control = InputControl(client)
    app_control = ApplicationControl(client)
    print(store)
    time.sleep(2)
    system_control.notify(
        "Cheers 🍻 to a weekend Flask project")
    yield "completed"
    return store


def control_tv(command):
    global mute_status, power_status
    if command == 'power':
        if power_status:
            system_control.power_off()
            power_status = False
        else:
            send_wol_packet(TV_MAC_ADDRESS, attempts=4, delay=1)
            power_status = True
            print("Magic Packet Sent")
    elif command == 'vol+':
        media_control.volume_up()
    elif command == 'vol-':
        media_control.volume_down()
    elif command == 'mute':
        if not mute_status:
            media_control.mute(True)
            mute_status = True
        else:
            media_control.mute(False)
            mute_status = False
        system_state()
    elif command == 'channel_up':
        media_control.channel_up()
    elif command == 'channel_down':
        media_control.channel_down()
    elif command in ['home', 'up', 'down', 'left', 'right', 'ok', 'back']:
        input_control.connect_input()
        getattr(input_control, command)()
        input_control.disconnect_input()
    elif command == 'netflix':
        apps = app_control.list_apps()
        ntf = [x for x in apps if "netflix" in x["title"].lower()][0]
        app_control.launch(ntf)


def system_state():
    if system_control is not None:
        return True
    else:
        return False
