from flask import render_template, request, jsonify, Blueprint, Response, stream_with_context
from app.tv_control import discover_tv, control_tv, system_state
from app.utils import load_store, write_store
import json

main = Blueprint('main', __name__)

store = load_store()


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/discover', methods=['POST'])
def discover():
    global store

    def generate():
        try:
            for status in discover_tv(store):
                if status == "prompted":
                    yield json.dumps({"success": True, "message": "Please accept the connection on the TV!"})
                elif status == "registered":
                    yield json.dumps({"success": True, "message": "Registration successful!"})
                elif status == "completed":
                    write_store(store)
                    yield json.dumps({"success": True, "message": "Discovery completed."})
        except Exception as e:
            print(f"Error discovering and connecting to TV: {str(e)}")
            yield json.dumps({"success": False, "message": str(e)})

    return Response(stream_with_context(generate()), mimetype='application/json')


@main.route('/control', methods=['POST'])
def control():
    command = request.json['command']
    try:
        control_tv(command)
        return jsonify(success=True)
    except Exception as e:
        print(f"Error sending command: {str(e)}")
        return jsonify(success=False, message='Error sending command')


@main.route('/status', methods=['GET'])
def status():
    # Check the actual connection status of the TV
    is_connected = system_state()
    return jsonify(connected=is_connected)
