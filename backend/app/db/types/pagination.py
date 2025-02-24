from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import Select


from typing import Generic, Iterator, List, Sequence

from typing import TypeVar


T = TypeVar("T")


class Pagination(Generic[T], Sequence[T]):
    """
    Pagination result class for async SQLAlchemy queries.

    :attr items: List of items to paginate
    :attr total_items: Total number of items
    :attr total_pages: Total number of pages
    :attr page: Current page number
    :attr per_page: Number of items per page
    :attr has_next: Has next page
    :attr has_previous: Has previous page
    :attr next_page: Next page number
    :attr previous_page: Previous page number
    """

    def __init__(
        self,
        items: List[T],
        total_items: int,
        page: int = 1,
        per_page: int = 10,
    ):
        """
        Initialize the pagination result.

        :param items: List of items to paginate
        :param page: Current page number
        :param per_page: Number of items per page
        :param total_items: Total number of items
        """
        if page < 1:
            raise ValueError("Page number must be at least 1")
        if per_page < 1:
            raise ValueError("Items per page must be at least 1")
        if total_items < 0:
            raise ValueError("Total items must be at least 0")

        # logic to check if the page number is out of range
        if (per_page * page) > total_items:
            raise ValueError("Page number is out of range")

        # logic to check if the items length is out of range
        if len(items) > per_page:
            raise ValueError("Items length must be less than or equal to per_page")

        self.items = items
        self.page = page
        self.per_page = per_page
        self.total_items = total_items

    @property
    def total_pages(self) -> int:
        return (self.total_items + self.per_page - 1) // self.per_page

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1

    @property
    def next_page(self) -> int | None:
        if self.has_next:
            return self.page + 1
        return None

    @property
    def previous_page(self) -> int | None:
        if self.has_previous:
            return self.page - 1
        return None

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> T:
        return self.items[index]

    def __setitem__(self, index: int, value: T) -> None:
        raise NotImplementedError("Pagination is immutable")

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __contains__(self, item: T) -> bool:
        return item in self.items

    def __reversed__(self) -> Iterator[T]:
        return reversed(self.items)

    @classmethod
    async def from_query(
        cls, session: AsyncSession, query: Select[T], page: int = 1, per_page: int = 10
    ) -> "Pagination[T]":
        """
        Create pagination from an SQLAlchemy query.

        :param session: Async SQLAlchemy session
        :param query: SQLAlchemy select query
        :param page: Page number (1-indexed)
        :param per_page: Number of items per page
        :return: Pagination instance
        """
        if page < 1:
            raise ValueError("Page number must be at least 1")
        if per_page < 1:
            raise ValueError("Items per page must be at least 1")

        # Count total items
        total_items_result = await session.execute(
            select(func.count()).select_from(query)
        )
        total_items = total_items_result.scalar_one()

        # Get items
        result = await session.execute(
            query.offset((page - 1) * per_page).limit(per_page)
        )
        items = result.scalars().all()

        return cls(items=items, page=page, per_page=per_page, total_items=total_items)
