import string
import argparse
import random

def main():
    parser = argparse.ArgumentParser(description='File generator')
    parser.add_argument('-c', '--count', help='Count of strings to generate', required=False, default=1000000, type=int)
    parser.add_argument('-f', '--file', help='File to generate', required=True)

    args = parser.parse_args()

    with open(args.file, 'w') as file:
        for _ in range(int(args.count)):            
            len = random.randint(50, 100)
            str = random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=len)
            spaces_count = random.randint(3, 5)
            spaces = set()

            for _ in range(spaces_count):
                s = random.choice([x for x in range(1, len) if x not in spaces])
                spaces.add(s)
                spaces.add(s - 1)
                spaces.add(s + 1)
                str[s] = ' '
            
            file.write("".join(str) + "\n")
        



if __name__ == "__main__":
    main()