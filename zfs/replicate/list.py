"""Common List Functions."""

from typing import Sequence, TypeVar

A = TypeVar("A")

def inits(elements: Sequence[A]) -> Sequence[Sequence[A]]:
    """All initial segments of the given list.

    The shortest lists are first.

    >>> inits(["a", "b", "c"])
    [[], ['a'], ['a', 'b'], ['a', 'b', 'c']]

    """

    return [elements[:n] for n in range(len(elements) + 1)]


def venn(lefts: Sequence[A], rights: Sequence[A]) -> (Sequence[A], Sequence[A], Sequence[A]):
    """A venn diagram of the two sequences.

    A venn diagram shows the elements both sets contain individually as well as
    the elements they have in common.  We return a 3-tuple with the left only,
    common, and right only elements in its respective components.

    """

    return (
        filter(lambda x: x not in rights, lefts),
        filter(lambda x: x in rights, lefts),
        filter(lambda x: x not in lefts, rights)
        )
