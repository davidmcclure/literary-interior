

import spacy

from .utils import cached_class_property


class Tokenizer:

    @classmethod
    def from_file(cls, path):
        """Read text file.
        """
        with open(path) as fh:
            return cls(fh.read())

    def __init__(self, raw):
        self.raw = raw

    @cached_class_property
    def nlp_sents(self):
        nlp = spacy.blank('en')
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        return nlp

    @cached_class_property
    def nlp(self):
        return spacy.load('en')

    def sents(self):
        """Tokenize sentences.
        """
        return list(self.nlp_sents(self.raw).sents)

    def __iter__(self):
        """Generate tokens.

        Yields: token, sent idx, word idx, char idx.
        """
        word_i = 0
        for sent_i, sent in enumerate(self.sents()):

            parsed_sent = self.nlp(sent.text_with_ws)

            for token in parsed_sent:
                char_i = sent.start_char + token.idx
                yield token, sent_i, word_i, char_i
                word_i += 1
