#!/usr/bin/python3

def build_spacy_chain(mode, lang, lookback):
    mode, lang = mode.lower(), lang.lower()

    if lang != 'de':
        raise Exception('only language de is currently supported')

    try:
        from .spacy_chain import SpacyPosMarkovChain, SpacyTagMarkovChain
    except:
        from spacy_chain import SpacyPosMarkovChain, SpacyTagMarkovChain

    model = 'de_core_news_sm'

    if mode == 'pos':
        return SpacyPosMarkovChain(model, lookback)
    elif mode == 'tag':
        return SpacyTagMarkovChain(model, lookback)

    raise Exception('unknown mode %s' % mode)


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', type=int, default=20, help='Amount of words to generate.')
    parser.add_argument('-s', type=int, default=None, help='Amount of sentences to generate. This will overturn -n.')
    parser.add_argument('--lookback', type=int, default=1, help='Amount of states to consider for determining the next state.')

    parser.add_argument('--lang', type=str, default='de', help='Text language: de')
    parser.add_argument('--mode', type=str, default='', help='Text generation mode: pos, tag')

    args = parser.parse_args()

    if not 1 <= args.lookback <= 2:
        raise Exception('only lookback satisfying condition 1 <= lookback <= 2 is currently supported')
    
    if args.mode.lower() in ['tag', 'pos']:
        gen = build_spacy_chain(args.mode, args.lang, args.lookback)

    else:
        try:
            from .chain import MarkovChain
        except:
            from chain import MarkovChain

        gen = MarkovChain(args.lookback)

    gen.add_string(sys.stdin.read())
    text = gen.generate_text(args.s) if args.s else gen.generate(args.n)

    try:
        text = gen.generate_text(args.s) if args.s else gen.generate(args.n)

        print(' '.join(text))

    except Exception as e:
        print('ERROR:', e)


if __name__ == '__main__':
    main()
