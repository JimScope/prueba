import configparser
import logging
import socket

config = configparser.ConfigParser()
config.read('config.ini')
config_def = config['DEFAULT']
logging.basicConfig(level=logging.DEBUG)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((config_def['ADDRESS'], int(config_def['PORT'])))
    logging.info(f"Connection established with the server")

    with open(f"{config_def['FILE_PATH']}", "r") as f:
        send_data = f.read()

    client.send(send_data.encode(config_def['FORMAT']))
    logging.info("File sended")

    server_response = client.recv(int(config_def['SIZE'])).decode(config_def['FORMAT'])
    logging.info(f"OK: {server_response}")

    logging.info("Disconnected from the server")
    client.close()


if __name__ == "__main__":
    main()
