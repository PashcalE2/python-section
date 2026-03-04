from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:
    def __init__(self, per_page: int) -> None:
        self.per_page = per_page

    def __iter__(self):
        page = 0
        while True:
            page += 1
            data: Page = request(Query(per_page=self.per_page, page=page))

            for value in data.results:
                yield value

            if data.next is None:
                break


class Fibo:
    __counter: int
    __last: int
    __current: int

    def __init__(self, n: int) -> None:
        self._n = n

    def __iter__(self):
        self.__counter = 0
        self.__last = 0
        self.__current = 1

        return self

    def __next__(self):
        self.__counter += 1

        if self.__counter == 1:
            return 0
        if self.__counter == 2:
            return 1
        if self.__counter > self._n:
            raise StopIteration()

        self.__last, self.__current = self.__current, self.__last + self.__current
        return self.__current
