import socket
import threading
import requests
from flask import Flask, render_template, request, jsonify
from os import getenv

# Flask Web Server setup
app = Flask(__name__)

# Example coordinate storage (can be updated dynamically)
current_coords = {'latitude': 51.505, 'longitude': -0.09}

@app.route('/')
def map_view():
    return render_template('index.html')

@app.route('/get-coordinates')
def get_coordinates():
    return jsonify(current_coords)

@app.route('/update-coordinates', methods=['POST'])
def update_coordinates():
    global current_coords
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    if latitude and longitude:
        current_coords = {'latitude': latitude, 'longitude': longitude}
        return jsonify({'status': 'success', 'message': 'Coordinates updated successfully.'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid coordinates.'}), 400

# GPS Server setup
def parse_gps_data(data):
    # Parse the GPS data string into latitude and longitude
    secondSplit = data.split(',')
    lat = secondSplit[3]
    log = secondSplit[4]
    utcTime = secondSplit[2]
    return lat, log, utcTime

def send_coordinates_to_webserver(lat, log, webserver_url):
    try:
        payload = {'latitude': float(lat), 'longitude': float(log)}
        response = requests.post(webserver_url, json=payload)
        if response.status_code == 200:
            print("Coordinates successfully sent to the web server.")
        else:
            print(f"Failed to send coordinates. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error while sending coordinates to web server: {e}")

def start_gps_server(host, port, webserver_url):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    while True:
        s.listen()
        print(f"GPS Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                lat, log, _ = parse_gps_data(data.decode())
                print("Received:", "Latitude:", lat, "Longitude:", log)
                send_coordinates_to_webserver(lat, log, webserver_url)
        print("Connection Interrupted")

# Multithreading to run both servers concurrently
def run_web_server():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    hostIP = getenv("GPS_SERVER_IP", "0.0.0.0")
    hostPort = int(getenv("GPS_SERVER_PORT", 65432))
    webserver_url = getenv("WEB_SERVER_URL", "http://127.0.0.1:5000/update-coordinates")

    # Create threads for the GPS server and the Flask web server
    gps_thread = threading.Thread(target=start_gps_server, args=(hostIP, hostPort, webserver_url))
    web_thread = threading.Thread(target=run_web_server)

    # Start both threads
    gps_thread.start()
    web_thread.start()

    # Wait for both threads to complete
    gps_thread.join()
    web_thread.join()

