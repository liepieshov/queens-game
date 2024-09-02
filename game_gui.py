import tkinter as tk
import uuid
import os
from dataclasses import dataclass
from typing import Optional, TypeAlias
Coordinate: TypeAlias = tuple[int, int]

BASIC_PALETTE = [
    "#9e0142",
    "#d53e4f",
    "#f46d43",
    "#fdae61",
    "#fee08b",
    "#ffffbf",
    "#e6f598",
    "#abdda4",
    "#66c2a5",
    "#3288bd",
    "#5e4fa2",
]
@dataclass
class Level:
    solution: list[int]
    coloring: list[list[Coordinate]]
    name: Optional[str] = None

def gen_colours(n: int) -> list[str]:
    assert len(BASIC_PALETTE) > 0
    if n > len(BASIC_PALETTE):
        raise RuntimeError("not enough colours in paletter")
    result = []
    step = len(BASIC_PALETTE) // n
    i = 0
    while len(result) < n:
        result.append(BASIC_PALETTE[i])
        i += step
    assert len(result) == n
    return result


def load_levels() -> list[Level]:
    levels_folder = "levels"
    if not os.path.exists(levels_folder):
        return []
    levels = []
    for fname in os.listdir(levels_folder):
        with open(os.path.join(levels_folder, fname), "r") as fd:
            solution = list(map(int, fd.readline().split()))
            coloring = [[] for _ in range(len(solution))]
            for row, line in enumerate(fd):
                for col, color_idx in enumerate(map(int, line.split())):
                    assert color_idx < len(solution)
                    coloring[color_idx].append((row, col))
            for row in coloring:
                assert len(row) > 0
            levels.append(Level(solution=solution, coloring=coloring, name=fname))
    return levels


def create_empty_level(n: int) -> Level:
    solution = list(range(n))
    coloring = [[] for _ in range(len(solution))]

    for row in range(len(solution)):
        for col in range(len(solution)):
            coloring[col].append((row, col))
    return Level(solution, coloring, str(uuid.uuid4()))


def view_level(level: Level, menu_view: tk.Frame, board_view: tk.Frame) -> None:
    pass


def view_levels(levels_view: tk.Frame, menu_view: tk.Frame, board_view: tk.Frame) -> None:
    def handle_click(level: Level):
        return view_level(level, menu_view, board_view)

    for item in levels_view.winfo_children():
        item.destroy()
    for level in load_levels():
        btn = tk.Button(text=level.name or "<untitled>", master=levels_view, width=50)
        btn.bind(level, handle_click)
        btn.pack()


def main() -> None:
    window = tk.Tk()
    tk.Label(text="Hello, basic window!")
    c1, c2, c3 = gen_colours(3)

    # grid setup
    split_top = tk.Frame(master=window)
    split_top.pack(fill=tk.BOTH, expand=True)
    split_bottom = tk.Frame(master=window)
    split_bottom.pack(fill=tk.BOTH, expand=True)

    # levels list setup
    levels_list = tk.Frame(master=split_top, name="existing_levels", bg=c1)
    levels_list.pack(fill=tk.BOTH,  expand=True)

    # view of the board
    board_view = tk.Frame(master=split_bottom, name="board", bg=c2)
    board_view.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    # control of the board
    menu_view = tk.Frame(master=split_bottom, name="menu_view", bg=c3)
    menu_view.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    return window.mainloop()



if __name__ == '__main__':
    main()
