import typer
from sudoku import Sudoku

app = typer.Typer(
    name="Sudoku Toolbox",
)


def stringified_sudoku(sudoku: list) -> str:
    flattened = [item for sublist in sudoku for item in sublist]
    flattened = [0 if item is None else item for item in flattened]
    flattened = [str(item) for item in flattened]
    return "".join(flattened)


def listified_sudoku(width: int, height: int, sudoku: str) -> list:
    size = width * height
    sudoku = [int(item) if item != "0" else None for item in sudoku]
    values = []
    for i in range(0, size):
        values.append(sudoku[i * size : (i + 1) * size])
    return values


@app.command(
    name="generate",
    help="Generate a sudoku puzzle.",
    short_help="Generate a sudoku puzzle.",
)
def generate(
    width: int = typer.Option(
        3,
        help="Width of the sudoku puzzle.",
        prompt=True,
        min=0,
        max=50,
    ),
    height: int = typer.Option(
        3,
        help="Height of the sudoku puzzle.",
        prompt=True,
        min=0,
        max=50,
    ),
    seed: float = typer.Option(
        0,
        help="Seed for the random number generator.",
        prompt=True,
    ),
    difficulty: float = typer.Option(
        0.5,
        help="Difficulty of the puzzle.",
        prompt=True,
        min=0,
        max=0.75,
    ),
):
    """
    Generate a sudoku puzzle.

    Usage:
        toolbox generate
        toolbox generate --width 3 --height 3 --seed 0 --difficulty 0.5
    """
    puzzle = Sudoku(width, height, seed).difficulty(difficulty)
    puzzle.show()
    typer.echo(stringified_sudoku(puzzle.board))
    solution = puzzle.solve()
    solution.show()
    typer.echo(stringified_sudoku(solution.board))


@app.command(
    name="solve",
    help="Solve a sudoku puzzle.",
    short_help="Solve a sudoku puzzle.",
)
def solve(
    width: int = typer.Option(
        3,
        help="Width of the sudoku puzzle.",
        prompt=True,
        min=0,
        max=50,
    ),
    height: int = typer.Option(
        3,
        help="Height of the sudoku puzzle.",
        prompt=True,
        min=0,
        max=50,
    ),
    puzzle: str = typer.Option(
        ...,
        help="The puzzle to solve.",
        prompt=True,
    ),
):
    """
    Solve a sudoku puzzle.

    Usage:
        toolbox solve
    """
    if len(puzzle) != (width * height) ** 2:
        typer.echo("Invalid puzzle.")
        return
    puzzle = listified_sudoku(width, height, puzzle)
    puzzle = Sudoku(width, height, board=puzzle)
    puzzle.show()
    typer.echo(puzzle.board)
    solution = puzzle.solve()
    solution.show()
    typer.echo(solution.board)


if __name__ == "__main__":
    app()
