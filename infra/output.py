from dataclasses import dataclass

from termcolor import colored

_indent_level = 0
_indent_width = 2


@dataclass
class section:
    title: str

    def print(self, msg: str = ""):
        for line in msg.splitlines(keepends=False):
            print(_indent_width * _indent_level * " " + line)

    def __enter__(self):
        global _indent_level

        print(colored(_indent_width * _indent_level * " " + self.title, "cyan"))
        _indent_level += 1

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _indent_level
        _indent_level -= 1
