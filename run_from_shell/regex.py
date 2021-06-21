import sys
from ..src.engine import RegexEngine


def usage():
    print("usage:\n{} regex test_string1 [test_string2 ...]".format(
        sys.argv[0]))
    pass


reng = RegexEngine()

if __name__ == "__main__":
    if len(sys.argv) == 1 and sys.argv[1] in ['--usage', '--help', '-u', '-h']:
        usage()

    if len(sys.argv) < 3:
        print("Missing arguments.")
        usage()

    regex = sys.argv[1]
    print("Regular expression: '{}'".format(regex))

    i = 2
    while i < len(sys.argv):
        test_str = sys.argv[i]
        res, _ = reng.match(regex, test_str)
        print_string = "'{}' match with the regex".format(
            test_str) if res == True else "'{}' doesn't match with the regex".format(test_str)
        print(print_string)
        i += 1
