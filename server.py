import configparser
import logging
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
config = configparser.ConfigParser()
config.read("config.ini")
config_def = config["DEFAULT"]

logging.basicConfig(level=logging.DEBUG)


def handle_connections(connection, address) -> None:
    logging.info(f"Connection established with: {address}")

    data = connection.recv(int(config_def["SIZE"])).decode(config_def["FORMAT"])
    logging.debug("Data received")
    connection.send("OK".encode(config_def["FORMAT"]))

    logging.info(f"{address} disconnected")
    connection.close()


def main():
    logging.info("Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config_def["ADDRESS"], int(config_def["PORT"])))
    server.listen()
    logging.info(f"Server is listening on {IP}:{config_def['PORT']}")

    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_connections, args=(connection, address))
        thread.start()
        logging.info(f"Active Connections {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
