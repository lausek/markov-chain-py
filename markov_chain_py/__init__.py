#!/usr/bin/python3

def build_spacy_chain(mode, lang):
    try:
        from .spacy_chain import SpacyPosMarkovChain, SpacyTagMarkovChain
    except:
        from spacy_chain import SpacyPosMarkovChain, SpacyTagMarkovChain

    mode, lang = mode.lower(), lang.lower()

    if lang != 'de':
        raise Exception('only language de is currently supported')

    model = 'de_core_news_sm'

    if mode == 'pos':
        return SpacyPosMarkovChain(model)
    elif mode == 'tag':
        return SpacyTagMarkovChain(model)

    raise Exception('unknown mode %s' % mode)


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', type=int, default=20, help='Amount of words to generate.')
    parser.add_argument('-s', type=int, default=None, help='Amount of sentences to generate. This will overturn -n.')
    parser.add_argument('--mode', type=str, default='', help='Text generation mode: pos, tag')
    parser.add_argument('--lang', type=str, default='de', help='Text language: de')

    args = parser.parse_args()
    
    if args.mode.lower() in ['tag', 'pos']:
        gen = build_spacy_chain(args.mode, args.lang)

    else:
        try:
            from .chain import MarkovChain
        except:
            from chain import MarkovChain

        gen = MarkovChain()

    gen.add_string(sys.stdin.read())

    try:
        text = gen.generate_text(args.s) if args.s else gen.generate(args.n)

        print(' '.join(text))

    except Exception as e:
        print('ERROR:', e)


if __name__ == '__main__':
    main()
