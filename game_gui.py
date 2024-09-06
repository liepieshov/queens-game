import tkinter as tk
from functools import partial
from itertools import chain
import uuid
import os
from dataclasses import dataclass

from typing import TypeAlias

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

class UnionFind:
    def __init__(self) -> None:
        self.data = {}
        self.components = 0

    def find(self, x):
        if x not in self.data:
            self.data[x] = x
            self.components += 1
        if self.data[x] != x:
            self.data[x] = self.find(self.data[x])
        return self.data[x]
    def union(self, x, y,):
        rx = self.find(x)
        ry = self.find(y)
        if rx != ry:
            self.data[rx] = ry
            self.components -= 1


@dataclass
class Level:
    solution: list[int]
    coloring: list[list[Coordinate]]
    name: str
    solution_mode: bool = True

    @property
    def n(self) -> int:
        return len(self.solution)

    def click(self, row: int, col: int):
        pass

    def change_size(self, new_value: int):
        pass

    def change_mode(self):
        pass


def read_level_from_file(filepath: str) -> Level:
    with open(filepath, "r") as fd:
        solution = list(map(int, fd.readline().split()))
        coloring = [[] for _ in range(len(solution))]
        for row, line in enumerate(fd):
            for col, color_idx in enumerate(map(int, line.split())):
                assert color_idx < len(solution)
                coloring[color_idx].append((row, col))
        for row in coloring:
            assert len(row) > 0
        return Level(
            solution=solution, coloring=coloring, name=os.path.basename(filepath)
        )


def write_level_to_folder(level: Level, folder_path: str) -> None:
    with open(os.path.join(folder_path, level.name), "w") as fd:
        rows = [level.solution]
        other_rows = [[0] * len(level.solution) for _ in range(len(level.solution))]
        for color in range(len(level.solution)):
            for row, col in level.solution[color]:
                other_rows[row][col] = color

        fd.writelines((" ".join(map(str, r)) for r in chain(rows, other_rows)))


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
        levels.append(read_level_from_file(os.path.join(levels_folder, fname)))
    return levels


def create_empty_level(n: int) -> Level:
    solution = list(range(n))
    coloring = [[] for _ in range(len(solution))]

    for row in range(len(solution)):
        for col in range(len(solution)):
            coloring[col].append((row, col))
    return Level(solution, coloring, str(uuid.uuid4()))

def reload_list_view(root: tk.Frame):
    for x in root.children:
        x.destroy()
    text = tk.Text(root)
    text.pack(side="left")
    sb = tk.Scrollbar(root, command=text.yview)
    sb.pack(side="right")
    text.configure(yscrollcommand=sb.set)
    for level in load_levels():
        button = tk.Button(text, text=level.name)
        text.window_create("end", window=button)
        text.insert("end", "\n")
    text.configure(state="disabled")
    pass

def save_level(level: Level):
    pass

def delete_level(level: Level):
    pass

def change_size(level: Level, new_size: int):
    pass

def control_view(level: Level, menu_view: tk.Frame) -> None:
    save_btn = tk.Button(menu_view, text="Save")
    save_btn.bind("<Button-1>", partial(save_level, level=level))
    save_btn.pack()
    
    delete_btn = tk.Button(menu_view, text="Delete")
    save_btn.bind("<Button-1>", partial(delete_level, level=level))
    delete_btn.pack()

    scaler = tk.Scale(menu_view, from_=1, to=level.n)
    scaler.set(level.n)
    scaler.trace("w", lambda name, index, mode, sv=scaler, lvl=level: change_size(lvl, sv.get()))
    scaler.pack()
    pass

def main() -> None:
    __root = tk.Tk()
    tk.Label(text="Hello, basic window!")

    # grid setup
    __split_top = tk.Frame(master=__root)
    __split_top.pack(fill=tk.BOTH, expand=True)
    reload_list_view(__split_top)
    __split_bottom = tk.Frame(master=__root)
    __split_bottom.pack(fill=tk.BOTH, expand=True)

    board_view = tk.Frame(master=__split_bottom, name="board")
    board_view.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def update_grid(level: Level) -> None:
        n = len(level.solution)
        colors = gen_colours(n)
        _grid = [
            [tk.Text(board_view, width=7,state=tk.DISABLED,foreground="black", heigh=7) for _ in range(n)] for _ in range(n)
        ]
        for color in range(n):
            for row, col in level.coloring[color]:
                _grid[row][col].config(bg = colors[color])
                _grid[row][col].bind("<Button-1>", partial(lambda x, row, col: print((row, col)), row=row, col=col))
                _grid[row][col].grid(row=row, column=col)

        for col, row in enumerate(level.solution):
            _grid[row][col].config(state=tk.NORMAL)
            _grid[row][col].insert(tk.END, "x")
            _grid[row][col].config(state=tk.DISABLED)
        return _grid
    lvl = create_empty_level(5)
    grid = update_grid(lvl)

    return __root.mainloop()


if __name__ == "__main__":
    main()
    # I am very silly here and do a lot of overcomplication

    # Flow -> list levels from files
    # - click level
    # - view level
    # - make changes
    # - create stack of changes
    # - validate changes all the time
    # - ?save -> {update level from stack and save into file, remove stack, view level}
    # - create level - autosave it and @view level:)
