# LG WebOS TV Remote Control

This project provides a web-based remote control interface for LG WebOS TVs. It allows you to control your LG TV using a web browser on your computer or mobile device.

## Features

- Discover and connect to LG WebOS TVs on the local network
- Power on/off the TV
- Change volume
- Navigate the TV menu using arrow keys and OK button
- Launch apps (e.g., Netflix)
- Mute/unmute the TV
- Display notifications
- Access remote control via mobile devices, on the same network

## Prerequisites

- Python >= 3.9
- Flask web framework
- `pywebostv` library
- `wakeonlan` library

## Installation

1. Clone the repository:
   `git clone https://github.com/DanielTeshager/lgtv_remote.git`
2. Install the required dependencies:
   `pip install -r requirements.txt`
3. Run the Flask web server:
   `python3 run.py`

4. Open a web browser and visit `http://localhost:5001` to access the remote control interface.

## Usage

1. Make sure your LG WebOS TV is connected to the same local network as the device running the Flask application.

2. Click the "Discover" button to discover and connect to your LG TV.

3. Once connected, you can use the various buttons and controls on the web interface to interact with your TV.

4. You can power on/off the TV, change channels and volume, navigate the menu, launch apps, and mute/unmute the TV.

## Configuration

- Update the `config.py` file with your TV's MAC address for Wake-on-LAN functionality.

## Troubleshooting

- If the TV is not discovered or connected, ensure that it is turned on and connected to the same local network as the device running the Flask application.

- If the TV is in standby mode and not responding to Wake-on-LAN packets, you may need to enable Wake-on-LAN in your TV's settings.

- If you encounter any issues or errors, please refer to the error messages in the console or log files for more information.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [pywebostv](https://github.com/supersaiyanmode/PyWebOSTV) - Library for communicating with LG WebOS TVs.
- [Flask](https://flask.palletsprojects.com/) - Web framework used for the remote control interface.
