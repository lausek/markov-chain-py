#!/usr/bin/python3

try:
    from .chain import MarkovChain
    from .ngram_chain import NGramMarkovChain
except:
    from chain import MarkovChain
    from ngram_chain import NGramMarkovChain


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
    import logging
    import sys

    logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', type=int, default=20, help='Amount of words to generate.')
    parser.add_argument('-s', type=int, default=None, help='Amount of sentences to generate. This will overturn -n.')
    parser.add_argument('--lookback', type=int, default=1, help='Amount of states to consider for determining the next state.')
    parser.add_argument('--verbose', default=False, action='store_true', help='Output verbose information about the text generation.')

    parser.add_argument('--mode', type=str, default='', help='Text generation mode: ngram, pos, tag')
    parser.add_argument('--lang', type=str, default='de', help='Text language: de')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not 1 <= args.lookback:
        raise Exception('lookback must be greater than one.')
    
    if args.mode.lower() in ['tag', 'pos']:
        gen = build_spacy_chain(args.mode, args.lang, args.lookback)

    elif args.mode.lower() in ['ngram']:
        gen = NGramMarkovChain(args.lookback)

    else:
        gen = MarkovChain(args.lookback)

    gen.add_string(sys.stdin.read())
    text = gen.generate_text(args.s) if args.s else gen.generate(args.n)

    try:
        text = gen.generate_text(args.s) if args.s else gen.generate(args.n)
        logging.info(text)

    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    main()
