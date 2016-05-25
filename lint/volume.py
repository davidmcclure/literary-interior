

import json
import bz2

from collections import defaultdict, Counter

from lint.page import Page


class Volume:


    @classmethod
    def from_path(cls, path):

        """
        Inflate a volume and make an instance.

        Args:
            path (str)

        Returns: cls
        """

        with bz2.open(path, 'rt') as fh:
            return cls(json.loads(fh.read()))


    def __init__(self, data):

        """
        Read the compressed volume archive.

        Args:
            data (dict)
        """

        self.data = data


    @property
    def id(self):

        """
        Get the HTRC id.

        Returns: str
        """

        return self.data['id']


    @property
    def year(self):

        """
        Get the publication year.

        Returns: int
        """

        return int(self.data['metadata']['pubDate'])


    @property
    def language(self):

        """
        Get the language.

        Returns: str
        """

        return self.data['metadata']['language']


    @property
    def is_english(self):

        """
        Is the volume English?

        Returns: bool
        """

        return self.language == 'eng'


    def token_count(self):

        """
        Get the total number of tokens in the page "body" sections.

        Returns: int
        """

        return sum([
            p.token_count
            for p in self.pages()
        ])


    def pages(self):

        """
        Generate page instances.

        Yields: Page
        """

        for data in self.data['features']['pages']:
            yield Page(data)


    def token_offsets(self, resolution=1000):

        """
        For each token, get the offsets of each instance of the token inside
        the text, with the offset is snapped onto an integer "tick."

        args:
            resolution (int)

        Returns: dict {token: Counter({ offset: count })}
        """

        offsets = defaultdict(Counter)

        token_count = self.token_count()

        seen = 0
        for page in self.pages():

            # 0-1 ratio of the page "center."
            center = (
                (seen + (page.token_count / 2)) /
                token_count
            )

            tick = round(resolution * center)

            counts = page.merged_token_counts()

            # Register tick -> count.
            for token, count in counts.items():
                offsets[token][tick] += count

            # Track the cumulative count.
            seen += page.token_count

        return offsets



"""
it occurred to me last night that his skin
must be the most terribly delicate thing.
how great the debt, and how efficient the payment.
thorns in the hundreds, lashes in the dozens,
three little nails, a spear in the liver.
an afternoon! my charges fare much worse in an hour
and every hour is followed by another.

to my red eyes, this must be the premiere talent of god.
surely nothing suffers more excellently.
a bloody cuticle on a raw day in judea -
safisfaction for a thousand dishonored parents.
carpentry! each splinter, a war fixed.
a hemorrhoid - sodom doused.
a nasty afternoon, a few hours in the sun -
all of sin discharged?
a loudest lyre of pain -
strummed, and the universe shakes.

I have realized that in this regard, as in all others
it falls to me to be the great counterpoint.
this is the hilarious secret.
as he must specialize in pain, I in joy.
it is the truth. it grows most hugely in my heart.
my god, it is unspeakable.

I soar and sail alone in the universe
like a great invisible bird.
I am in love with the sound and sweet smell
of space dust hissing in my scales.

recently I have taken to wandering far out
to a quiet pocket in the sky
the earth a speck of blue
like some place in the middle of the ocean
with water all around forever
and I flap my huge wings and i start to spin
slowly at first and then faster, like a great top
massive and pitch black, so black that all you see
are my eyes blinking like pulsars
and I spin and spin
until the stars blur together into a plate of solid white
and when I dream most deeply
I dream that one day I will be able to hold the world
in a single glance.
"""
