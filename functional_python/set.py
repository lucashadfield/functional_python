from typing import Callable, List, TypeVar, NewType

T = TypeVar('T')
FunctionalSet = NewType('FunctionalSet', Callable)  # function of the form (x: T) -> bool
Filter = NewType('Filter', Callable)  # function of the form (x: T) -> bool
Mapper = NewType('Mapper', Callable)  # function of the form (x: T) -> T


def singleton_set(elem: T) -> FunctionalSet:
    return lambda x: elem == x


def functional_set(items: List) -> FunctionalSet:
    def loop(s: FunctionalSet, items: List):
        if not len(items):
            return s
        else:
            return loop(union(s, singleton_set(items[0])), items[1:])

    return loop(singleton_set(items[0]), items[1:])


def contains(s: FunctionalSet, elem: T):
    return s(elem)


def union(s: FunctionalSet, t: FunctionalSet) -> FunctionalSet:
    return lambda x: True if (contains(s, x) or contains(t, x)) else False


def intersect(s: FunctionalSet, t: FunctionalSet) -> FunctionalSet:
    return lambda x: True if (contains(s, x) and contains(t, x)) else False


def diff(s: FunctionalSet, t: FunctionalSet) -> FunctionalSet:
    return lambda x: True if (contains(s, x) and not contains(t, x)) else False


def filter(s: FunctionalSet, p: Filter) -> FunctionalSet:
    return lambda x: True if (contains(s, x) and p(x)) else False


def for_all(s: FunctionalSet, p: Filter, bound=1000) -> bool:
    def loop(a: T) -> bool:
        if a > bound:
            return True
        elif contains(s, a) and not p(a):
            return False
        else:
            loop(a + 1)

    return loop(-bound)


def exists(s: FunctionalSet, p: Filter) -> bool:
    return not for_all(s, lambda x: not p(x))


def map(s: FunctionalSet, f: Mapper) -> FunctionalSet:
    return lambda x: exists(s, lambda y: f(y) == x)
