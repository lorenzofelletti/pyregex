import sys
from src.engine import RegexEngine


def usage():
    pass


reng = RegexEngine()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Missing arguments.")
        usage()

    regex = sys.argv[1]
    print("Regular expression: '{}'".format(regex))

    i = 2
    while i < len(sys.argv):
        test_str = sys.argv[i]
        res, _ = reng.match(regex, test_str)
        print_string = "'{}' match with the regex".format(test_str) if res == True else "'{}' doesn't match with the regex".format(test_str)
        print(print_string)
        i += 1
