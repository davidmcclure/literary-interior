

from lint.models import Text


def test_store_raw_text():
    text = Text.parse('My name is David.')
    assert text.raw == 'My name is David.'


def test_store_text():

    text = Text.parse('My name is David.')

    assert [t.text for t in text.tokens] == [
        'My', 'name', 'is', 'David', '.'
    ]


def test_store_lemma():

    text = Text.parse('My name is David.')

    assert [(t.text, t.lemma) for t in text.tokens] == [
        ('My', '-PRON-'),
        ('name', 'name'),
        ('is', 'be'),
        ('David', 'david'),
        ('.', '.'),
    ]


def test_store_pos():

    text = Text.parse('My name is David.')

    assert [(t.text, t.pos) for t in text.tokens] == [
        ('My', 'ADJ'),
        ('name', 'NOUN'),
        ('is', 'VERB'),
        ('David', 'PROPN'),
        ('.', 'PUNCT'),
    ]


def test_store_tag():

    text = Text.parse('My name is David.')

    assert [(t.text, t.tag) for t in text.tokens] == [
        ('My', 'PRP$'),
        ('name', 'NN'),
        ('is', 'VBZ'),
        ('David', 'NNP'),
        ('.', '.'),
    ]


def test_store_dep():

    text = Text.parse('My name is David.')

    assert [(t.text, t.dep) for t in text.tokens] == [
        ('My', 'poss'),
        ('name', 'nsubj'),
        ('is', 'ROOT'),
        ('David', 'attr'),
        ('.', 'punct'),
    ]


def test_store_word_index():

    text = Text.parse('1 2 3 4 5')

    assert [(t.text, t.word_i) for t in text.tokens] == [
        ('1', 0),
        ('2', 1),
        ('3', 2),
        ('4', 3),
        ('5', 4),
    ]


def test_store_word_index_across_sents():

    text = Text.parse('1 2. 3 4.')

    assert [(t.text, t.word_i) for t in text.tokens] == [
        ('1', 0),
        ('2', 1),
        ('.', 2),
        ('3', 3),
        ('4', 4),
        ('.', 5),
    ]


def test_store_char_index():

    text = Text.parse('12 34 56')

    assert [(t.text, t.char_i) for t in text.tokens] == [
        ('12', 0),
        ('34', 3),
        ('56', 6),
    ]


def test_store_char_index_across_sents():

    text = Text.parse('12 34. 56 78.')

    assert [(t.text, t.char_i) for t in text.tokens] == [
        ('12', 0),
        ('34', 3),
        ('.',  5),
        ('56', 7),
        ('78', 10),
        ('.',  12),
    ]


def test_store_sent_index():

    text = Text.parse('1 2. 3 4.')

    assert [(t.text, t.sent_i) for t in text.tokens] == [
        ('1', 0),
        ('2', 0),
        ('.', 0),
        ('3', 1),
        ('4', 1),
        ('.', 1),
    ]
