"""
    Story for seven chapters. How much of this we use is a different matter.
"""

from collections import namedtuple

Story = namedtuple("Story", "title intro ground epilogue")

chapters = [
    Story(
        "The Beginning",
        """
        The Datapawns, rejects from terrible indie computer games,
        lay on the scrapheap of history.
        Until the rise of the Data Moon, which restored their old
        powers and led them on their holy mission.

        To Ruin Video Games Somehow.
        """,
        "[DDD1] Keep Moving Right. That is The First Law.",
        """
        The Datapawn Tribe had its first success,
        but that was only the beginning.
        """
    ),
    Story(
        "The Diggening",
        """
        The Datapawns are unable to climb steep vertical steps.
        But the Data Moon has bestowed the power of The Diggening.

        It must be used wisely. It's kind of indiscriminate.
        """,
        "[DD01] changes the leader, [1D-1] makes the leader dig.",
        """
        The Datapawns eventually outwitted some inanimate obstacles.
        But soon they would meet foes very slightly cleverer.
        """
    ),
    Story(
        "The Magenta Moon",
        """
        Under the evil Magenta Moon a terrible demon appeared.
        Magenta is objectively the worst colour. It's not
        even a proper colour.
        """,
        "Spanners are no more use here. Fly, you fools",
        """
        No really, look at the rainbow: it's not there.
        It's unnatural. If you look at magenta too much
        you get eye cancer.
        """
    ),
    Story(
        "The Gun People",
        """
        The Gun People are squashy mortals with fantasies of power.
        They feel Called to the Duty of making a lot of noise to
        no creative effect.

        They are vulnerable to The Diggening.
        """,
        "C A N  Y O U  D I G  I T",
        """
        The Gun People are not very good at preventing the
        Ruination of Video Games Somehow. To say the least.
        """
    ),
]
