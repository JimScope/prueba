import argparse
import configparser
import logging
import random
import socket
import string

config = configparser.ConfigParser()
config.read("config.ini")
config_def = config["DEFAULT"]
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(message)s", filename="client.log"
)


def main() -> None:
    parser = argparse.ArgumentParser(description="String generator")
    parser.add_argument(
        "-c",
        "--count",
        help="Count of strings to generate",
        required=False,
        default=1000000,
        type=int,
    )

    args = parser.parse_args()
    generate_file(args)


def generate_file(args: argparse.Namespace) -> None:
    """Generate a file with random strings
    :param args: argparse.Namespace
    :return: None
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((config_def["ADDRESS"], int(config_def["PORT"])))
    logging.info(f"Connection established with the server")

    with open(config_def["FILE_PATH"], "w") as file:
        for _ in range(int(args.count)):
            len = random.randint(50, 100)
            str = random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k=len
            )
            spaces_count = random.randint(3, 5)
            spaces = set()

            for _ in range(spaces_count):
                s = random.choice([x for x in range(1, len) if x not in spaces])
                spaces.add(s)
                spaces.add(s - 1)
                spaces.add(s + 1)
                str[s] = " "

            file.write("".join(str) + "\n")
            client.send("".join(str).encode(config_def["FORMAT"]))
            logging.info("String sended")
            server_response = client.recv(int(config_def["SIZE"])).decode(
                config_def["FORMAT"]
            )
            logging.info(f"Response from server received: {server_response}")
        client.send("END_SESSION".encode(config_def["FORMAT"]))
        logging.info("Disconnected from the server")
        client.close()


if __name__ == "__main__":
    main()
