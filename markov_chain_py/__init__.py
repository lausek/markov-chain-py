#!/usr/bin/python3

def main():
    import argparse
    import sys

    try:
        from .chain import MarkovChain
    except:
        from chain import MarkovChain

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', type=int, default=20)

    args = parser.parse_args()

    mc = MarkovChain()

    mc.add_string(sys.stdin.read())

    try:
        print(' '.join(mc.generate(args.n)))
    except IndexError:
        print('input sequence is too short.')


if __name__ == '__main__':
    main()
