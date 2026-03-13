import sqlite3
import time
import socket
import threading
import json
import logging
import os
from config.config import SERVER_HOST, SERVER_PORT, MAX_THREADS

# création du dossier logs si nécessaire
os.makedirs("logs", exist_ok=True)

# configuration des logs
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

clients = []
last_seen = {}

# ===============================
# Base de données SQLite
# ===============================

conn = sqlite3.connect("metrics.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node TEXT,
    os TEXT,
    cpu REAL,
    memory REAL,
    uptime INTEGER,
    timestamp REAL
)
""")

conn.commit()


# ===============================
# Surveillance des noeuds
# ===============================

def monitor_nodes():

    while True:

        now = time.time()

        for node, last in list(last_seen.items()):

            if now - last > 90:

                alert = f"NOEUD EN PANNE : {node}"
                print(alert)
                logging.warning(alert)

        time.sleep(30)


# ===============================
# Gestion client
# ===============================

def handle_client(client_socket, client_address):

    print(f"[+] Client connecté : {client_address}")
    logging.info(f"Client connecté : {client_address}")

    clients.append(client_socket)

    try:

        while True:

            message = client_socket.recv(4096).decode().strip()

            print("MESSAGE BRUT RECU :", message)

            if not message:
                break

            try:

                data = json.loads(message)

                node = data.get("node")
                os_name = data.get("os")
                cpu = data.get("cpu")
                memory = data.get("memory")
                uptime = data.get("uptime")
                ports = data.get("ports", {})

                # mise à jour dernière activité du noeud
                last_seen[node] = time.time()

                print("\n========== METRICS RECEIVED ==========")
                print("Node:", node)
                print("OS:", os_name)
                print("CPU:", cpu, "%")
                print("Memory:", memory, "%")
                print("Uptime:", uptime)

                print("\nPorts status :")

                for port, status in ports.items():
                    print(f"Port {port} : {status}")

                print("======================================")

                logging.info(
                    f"Node={node} CPU={cpu}% MEM={memory}% UPTIME={uptime}"
                )

                # ===============================
                # Sauvegarde dans la base
                # ===============================

                cursor.execute(
                    "INSERT INTO metrics (node, os, cpu, memory, uptime, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (node, os_name, cpu, memory, uptime, time.time())
                )

                conn.commit()

                # ===============================
                # Alertes CPU
                # ===============================

                if cpu > 90:
                    alert = f"ALERTE CPU élevé sur {node} ({cpu}%)"
                    print(alert)
                    logging.warning(alert)

            except json.JSONDecodeError:

                logging.error("Message JSON invalide reçu")

    except Exception as e:

        logging.error(f"Erreur avec {client_address} : {e}")

    finally:

        print(f"[-] Client déconnecté : {client_address}")
        logging.info(f"Client déconnecté : {client_address}")

        if client_socket in clients:
            clients.remove(client_socket)

        client_socket.close()


def server_menu():

    while True:

        print("\n===== MENU SERVEUR =====")
        print("1 - Voir les noeuds actifs")
        print("2 - Voir les métriques stockées")
        print("3 - Voir les noeuds surveillés")
        print("4 - Quitter")

        choix = input("Votre choix : ")

        if choix == "1":

            print("\nNoeuds actifs :")

            if len(last_seen) == 0:
                print("Aucun noeud connecté")

            for node in last_seen:
                print(node)

        elif choix == "2":

            print("\nDernières métriques :")

            cursor.execute(
                "SELECT node, cpu, memory, uptime FROM metrics ORDER BY id DESC LIMIT 10"
            )

            rows = cursor.fetchall()

            for row in rows:

                print(
                    f"Node={row[0]} CPU={row[1]}% MEM={row[2]}% UPTIME={row[3]}"
                )

        elif choix == "3":

            print("\nNoeuds surveillés :")

            for node, last in last_seen.items():

                print(node, "- dernière activité :", int(time.time() - last), "sec")

        elif choix == "4":

            print("Arrêt du serveur...")
            os._exit(0)

        else:

            print("Choix invalide")
            

def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((SERVER_HOST, SERVER_PORT))

    server.listen(MAX_THREADS)

    print(f"Serveur de supervision démarré sur {SERVER_HOST}:{SERVER_PORT}")
    logging.info("Serveur démarré")

    # thread surveillance noeuds
    monitor_thread = threading.Thread(target=monitor_nodes)
    monitor_thread.daemon = True
    monitor_thread.start()

    menu_thread = threading.Thread(target=server_menu)
    menu_thread.daemon = True
    menu_thread.start()

    while True:

        client_socket, client_address = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )

        thread.start()


if __name__ == "__main__":
    start_server()