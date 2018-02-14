

from lint.models import Token


def test_store_text():
    tokens = Token.parse('My name is David.')
    assert [t.text for t in tokens] == ['My', 'name', 'is', 'David', '.']


def test_store_lemma():
    tokens = Token.parse('My name is David.')
    assert [t.lemma for t in tokens] == ['-PRON-', 'name', 'be', 'david', '.']


def test_store_pos():
    tokens = Token.parse('My name is David.')
    assert [t.pos for t in tokens] == \
        ['ADJ', 'NOUN', 'VERB', 'PROPN', 'PUNCT']


def test_store_tag():
    tokens = Token.parse('My name is David.')
    assert [t.tag for t in tokens] == ['PRP$', 'NN', 'VBZ', 'NNP', '.']


def test_store_dep():
    tokens = Token.parse('My name is David.')
    assert [t.dep for t in tokens] == \
        ['poss', 'nsubj', 'ROOT', 'attr', 'punct']


def test_store_word_index():
    tokens = Token.parse('1 2 3 4 5')
    assert [t.word_i for t in tokens] == [0, 1, 2, 3, 4]


def test_store_character_index():
    tokens = Token.parse('12 34 56')
    assert [t.char_i for t in tokens] == [0, 3, 6]


def test_store_01_offset():
    tokens = Token.parse('1 2 3 4 5')
    assert [t.offset for t in tokens] == [0, 0.25, 0.5, 0.75, 1]
