import pytest

from .deps import *

class TestErrors(Test):
    def test_sentence_feature_not_supported(self):
        gen = MarkovChain(lookback=1)
        gen.add_string('das hier hat keinen punkt')

        with pytest.raises(Exception):
            gen.generate_text(s=4)
