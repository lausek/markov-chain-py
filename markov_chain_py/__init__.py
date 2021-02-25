#!/usr/bin/python3

def main():
    import argparse
    import sys

    try:
        from .chain import MarkovChain
    except:
        from chain import MarkovChain

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', type=int, default=20, help='Amount of words to generate.')
    parser.add_argument('-s', type=int, default=None, help='Amount of sentences to generate. This will overturn -n.')

    args = parser.parse_args()

    mc = MarkovChain()

    mc.add_string(sys.stdin.read())

    try:
        text = mc.generate_text(args.s) if args.s else mc.generate(args.n)

        print(' '.join(text))

    except IndexError:
        print('ERROR: Input sequence is too short.')

    except Exception as e:
        print('ERROR:', e)


if __name__ == '__main__':
    main()
