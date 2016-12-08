

import re

from IPython.display import Markdown, display

from lint.singletons import session
from lint.models import Token, Text


# TODO|dev


def print_snippet(text, prefix, match, suffix):

    """
    Print an individual snippet.
    """

    snippet = '{0} <span style="color: blue">{1}</span>'.format(prefix, match)

    if re.match('^[a-z]', suffix, re.I):
        snippet += ' '

    snippet += suffix

    # Scrub indentation.
    snippet = re.sub('(?<=\n)[ \t]*', '', snippet)

    display(Markdown('### {}, {} {}, {}'.format(
        text.title,
        text.author_first,
        text.author_last,
        text.year
    )))

    display(Markdown(snippet))
    display(Markdown('---'))


def query_snippets(
    token,
    year1=None,
    year2=None,
    ratio1=None,
    ratio2=None,
    limit=100,
):

    """
    Print snippets that fall within a range of years and ratios.
    """

    query = (
        session
        .query(Token)
        .join('text')
        .filter(Token.token==token)
    )

    if year1:
        query = query.filter(Text.year >= year1)

    if year2:
        query = query.filter(Text.year <= year2)

    if ratio1:
        query = query.filter(Token.ratio >= ratio1)

    if ratio2:
        query = query.filter(Token.ratio <= ratio2)

    for token in query.limit(limit):
        print_snippet(token.text, *token.snippet())


def snippets_csv(
    token,
    year1=None,
    year2=None,
    ratio1=None,
    ratio2=None,
    limit=100,
):

    """
    Print snippets to a CSV.
    """

    query = (
        session
        .query(Token)
        .join('text')
        .filter(Token.token==token)
    )

    if year1:
        query = query.filter(Text.year >= year1)

    if year2:
        query = query.filter(Text.year <= year2)

    if ratio1:
        query = query.filter(Token.ratio >= ratio1)

    if ratio2:
        query = query.filter(Token.ratio <= ratio2)

    for token in query.limit(limit):
        print('{} *{}* {}'.format(*token.snippet(50)))
