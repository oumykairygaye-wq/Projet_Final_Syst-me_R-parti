import socket
import time
import json
import psutil
import platform
from config.config import SERVER_HOST, SERVER_PORT


def check_port(port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    result = s.connect_ex(("127.0.0.1", port))
    s.close()

    if result == 0:
        return "OPEN"
    else:
        return "CLOSED"


def check_service(service_name):

    for process in psutil.process_iter(['name']):
        try:
            if service_name.lower() in process.info['name'].lower():
                return "ACTIVE"
        except:
            pass

    return "INACTIVE"


def collect_metrics():

    metrics = {
        "node": platform.node(),
        "os": platform.system(),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "uptime": int(time.time() - psutil.boot_time()),

        "ports": {
            "80": check_port(80),
            "443": check_port(443),
            "22": check_port(22),
            "3306": check_port(3306)
        },

        "services": {
            "http": check_service("http"),
            "ssh": check_service("ssh"),
            "mysql": check_service("mysql"),
            "chrome": check_service("chrome"),
            "firefox": check_service("firefox"),
            "vscode": check_service("code")
        }
    }

    return metrics


def start_client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        client.connect((SERVER_HOST, SERVER_PORT))
        print("Agent connecté au serveur")

        while True:

            metrics = collect_metrics()

            message = json.dumps(metrics)

            client.sendall((message + "\n").encode())

            print("Métriques envoyées :", message)

            time.sleep(5)

    except Exception as e:

        print("Erreur :", e)

    finally:

        client.close()
        print("Connexion fermée")


if __name__ == "__main__":
    start_client()