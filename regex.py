import sys
from time import perf_counter_ns
from pyregexp.engine import RegexEngine


def usage():
    print("usage: {} regex test_string1 [test_string2 ...]".format(
        sys.argv[0]))
    pass


reng = RegexEngine()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == '--usage' or sys.argv[1] == '--help' or sys.argv[1] == '-u' or sys.argv[1] == '-h':
        usage()
        exit(0)
    else:
        if len(sys.argv) < 3:
            print("Missing arguments.")
            usage()
            exit(-1)

        regex = sys.argv[1]
        print("Regular expression: '{}'".format(regex))

        i = 2
        while i < len(sys.argv):
            test_str = sys.argv[i]
            start_time = perf_counter_ns()
            res, _ = reng.match(regex, test_str)
            stop_time = perf_counter_ns()
            print(f'Execution time: {stop_time - start_time} ns.')
            print_string = f"'{test_str}' match with the regex" if res == True else f"'{test_str}' doesn't match the given regex"
            print(print_string)
            i += 1
