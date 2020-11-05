from __future__ import annotations
import sys
import typing

from c_integer import CInt
from exceptions import (
    StackOverflow,
    StackUnderflow,
    StackEmpty
)


class Stack:
    """Represents the abstract data type: stack.
    Items can only be added (pushed) or removed (popped) to this stack from the top.

    Parameters
    ----------
    values: Optional[Iterable[CInt]]
        A list of values to pre-populate the stack with.
    max_size: Optional[Int]
        The maximum number of items the stack can hold. Defaults to the value returned by sys.maxsize.
        This value should not be changed after instantiation, because this class does not have functionality to
        truncate the list of values to be under this limit should it change.
    """
    def __init__(self, values: typing.Iterable[CInt] = None, max_size: int = None) -> None:
        self.max_size = max_size if max_size else sys.maxsize
        self._values = []
        if values:
            self.push_many(values)

    def __len__(self) -> int:
        """Returns the number of items currently in the stack"""
        return len(self._values)

    def __str__(self) -> str:
        """Returns a string-like representation of the list of items in the stack"""
        return str(self._values)

    def __eq__(self, other: Stack) -> bool:
        """Returns True if the values and max_size in both stacks are the same. Otherwise False."""
        return self._values == other._values and self.max_size == other.max_size

    def __ne__(self, other: Stack) -> bool:
        """Returns True if the values or max_size in both stacks are different. Otherwise False."""
        return not self.__eq__(other)

    @property
    def is_empty(self) -> bool:
        """Returns True is the stack is currently empty. Otherwise False."""
        return True if self.count == 0 else False

    @property
    def is_full(self) -> bool:
        """Returns True if the stack is currently full"""
        return self.count >= self.max_size

    @property
    def count(self) -> int:
        """Returns as an integer, the number of values currently in the stack"""
        return len(self._values)

    def show(self) -> typing.List[CInt]:
        """Returns a list of values contained in the Stack."""
        if self.is_empty:  # Pressing d before pushing anything to the stack, returns the lowest possible number.
            return [CInt(CInt.min_value), ]

        return self._values

    def clear(self) -> None:
        """Remove all items from the stack."""
        if not self.is_empty:
            self._values = []

    def push(self, value: CInt) -> None:
        """Push a single CInt to the top of the stack.
        Raises `ValueError` should the type not be a CInt.
        Raises `StackOverflow` if the stack is already full.
        """
        if not isinstance(value, CInt):
            raise ValueError('Value is not a CInt')

        if self.count >= self.max_size:
            raise StackOverflow()

        self._values.append(value)

    def pop(self) -> CInt:
        """Removes and returns a single CInt from the top the stack.
        Raises `StackUnderflow` if the stack is empty.
        """
        if self.is_empty:
            raise StackUnderflow()

        return self._values.pop(-1)

    def peek(self) -> CInt:
        """Returns the top CInt from the stack
        Raises `StackEmpty` if the stack is empty.
        """
        if self.is_empty:
            raise StackEmpty()

        return self._values[-1]

    def push_many(self, values: typing.Iterable[CInt]) -> None:
        """Same functionality as `push`, but for multiple values. Adds then sequentially."""
        if not isinstance(values, typing.Iterable):
            raise ValueError('Values should be an iterable')

        for value in values:
            self.push(value)

    def pop_many(self, n: int) -> typing.List[CInt]:
        """Same functionality as `pop`, but for multiple values. Maintains their order."""
        if n > self.count:
            raise StackUnderflow()

        values = []
        for i in range(n):
            values.append(self.pop())
        return list(reversed(values))

    def peek_many(self, n: int) -> typing.List[CInt]:
        """Same functionality as `peek`, but for multiple values. Maintains their order."""
        if n < 1:  # An integer less than 1 would return a value from the back of the stack. This shouldn't be possible.
            raise ValueError("Can't peek from back to front.")

        if n > self.count:  # Requesting to peek more items than exist.
            raise StackUnderflow()

        values = []
        for i in range(-1, -n - 1, -1):  # range(start, stop, step).
            values.insert(0, self._values[i])
        return values
