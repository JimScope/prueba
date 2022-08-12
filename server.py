import configparser
import logging
import socket
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

IP = socket.gethostbyname(socket.gethostname())
config = configparser.ConfigParser()
config.read("config.ini")
config_def = config["DEFAULT"]

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(message)s", filename="server.log"
)


def handle_connections(connection: socket.socket, address: tuple) -> None:
    """ Handle the connections
    :param connection: socket.socket
    :param address: tuple
    :return: None"""
    logging.info(f"Connection established with: {address}")
    start = perf_counter()
    while True:
        try:
            data = connection.recv(int(config_def["SIZE"])).decode(config_def["FORMAT"])

            # Check for the signal to end the session
            if data == "END_SESSION":
                finish = perf_counter()
                connection.send(
                    f"Process completed in: {finish - start}".encode(
                        config_def["FORMAT"]
                    )
                )
                logging.info(f"{address} disconnected")
                connection.close()
                break

            # Filter the data
            elif "aa" in data.lower():
                logging.info(f"Double 'a' rule detected from {address} >> {data}")
                metrics = 1000
            else:
                logging.debug(f"Data received {data}")
                spaces_count = data.count(" ")
                letters_count = sum(1 for c in data if c.isalpha())
                digits_count = sum(1 for c in data if c.isdigit())
                # Metrics Calculation
                metrics = (letters_count * 1.5 + digits_count * 2) / spaces_count

            connection.send(f"Metrics: {metrics}".encode(config_def["FORMAT"]))

        except ConnectionResetError:
            logging.info("Connection closed")
            break


def main():
    logging.info("Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config_def.get("ADDRESS"), int(config_def.get("PORT"))))
    server.listen()
    logging.info(f"Server is listening on {IP}:{config_def.get('PORT')}")

    # Create a thread pool to handle the connections
    with ThreadPoolExecutor(max_workers=int(config_def.get("MAX_WORKERS"))) as executor:
        while True:
            connection, address = server.accept()
            executor.submit(handle_connections, connection, address)


if __name__ == "__main__":
    main()
