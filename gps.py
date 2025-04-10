import socket
import json

latest_gps_data = [{"lat": None, "lng": None, "address": "இருப்பிடம் தெரியவில்லை"}]

def gps_listener():
    HOST = '0.0.0.0'
    PORT = 8000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(" Vizhi AI GPS listener ready...")

    conn, addr = server.accept()
    print(f" GPS Connected from {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        try:
            gps_json = json.loads(data.decode().strip())
            latest_gps_data[0].update({
                "address": gps_json.get("address", "இருப்பிடம் தெரியவில்லை"),
                "lat": gps_json.get("lat"),
                "lng": gps_json.get("lng")
            })
        except Exception as e:
            print("JSON பிரச்சனை:", e)

    conn.close()