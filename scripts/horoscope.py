#!/usr/bin/python3

TTS_SERVICE_HOST = 'https://freetts.com'
TTS_SERVICE_URL = f'{TTS_SERVICE_HOST}/Home/PlayAudio'
TTS_SERVICE_AUDIO = f'{TTS_SERVICE_HOST}/audio'
TTS_LANGUAGE = 'de-DE'
TTS_VOICES = ['de-DE-Standard-A', 'de-DE-Standard-B']

TTS_MAX_TEXT_LEN = 300

def freetts(text):
    import random
    import requests

    data = {
        'Language': TTS_LANGUAGE,
        'Voice': random.choice(TTS_VOICES),
        'TextMessage': text,
        'type': 0,
    }

    res = requests.get(TTS_SERVICE_URL, params=data)
    res = res.json()

    res = requests.get(f'{TTS_SERVICE_AUDIO}/{res["id"]}')

    return res.content


def marytts(text):
    import random
    import requests

    HOST_URL = 'http://mary.dfki.de:59125'
    VOICES = ['bits1-hsmm', 'bits4', 'bits3-hsmm', 'bits3']

    data = {
        'INPUT_TEXT': text,
        'INPUT_TYPE': 'TEXT',
        'OUTPUT_TYPE': 'AUDIO',
        'LOCALE': TTS_LANGUAGE[:2],
        'VOICE': random.choice(VOICES),
        'AUDIO': 'WAVE_FILE',
    }

    res = requests.get(f'{HOST_URL}/process', params=data)

    if res.status_code != 200:
        raise Exception('tts failed: ' + str(data))

    return res.content


def tts(text):
    return marytts(text)


def play_audio(audio):
    import io
    import pydub
    import pydub.playback
    import threading

    def play_background():
        buf = io.BytesIO(audio)
        #seg = pydub.AudioSegment.from_mp3(buf)
        seg = pydub.AudioSegment.from_file(file=buf, format='wav')
        pydub.playback.play(seg)

    play_thread = threading.Thread(target=play_background)
    play_thread.start()


def read_horoscope_data():
    from pathlib import Path

    path = Path(__file__).parent.parent / 'examples' / 'horoskop.md'

    with open(path, 'r') as fin:
        return fin.read()


def main():
    import argparse
    import logging
    import sys

    logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)

    from markov_chain_py.ngram_chain import NGramMarkovChain

    sentence_n = 4
    parser = argparse.ArgumentParser()

    parser.add_argument('--lookback', type=int, default=6, help='amount of states to consider for determining the next state.')
    parser.add_argument('--verbose', default=False, action='store_true', help='output verbose information about the text generation.')

    args = parser.parse_args()
    gen = NGramMarkovChain(args.lookback)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    gen.add_string(read_horoscope_data())

    logging.info('rolling the dice...')

    text = gen.generate_text(sentence_n)
    while TTS_MAX_TEXT_LEN < len(text):
        text = gen.generate_text(sentence_n)

    play_audio(tts(text))

    logging.info(text)


if __name__ == '__main__':
    main()
