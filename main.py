from typing import List, Union

from fastapi import Body, FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, root_validator
from sudoku import Sudoku
from sudoku.sudoku import UnsolvableSudoku


class PuzzleSize(BaseModel):
    width: int = Field(
        ...,
        gt=0,
        lt=50,
        title="Width of the puzzle",
        description="The width of the puzzle",
        example=3,
    )
    height: int = Field(
        ...,
        gt=0,
        lt=50,
        title="Height of the puzzle",
        description="The height of the puzzle",
        example=3,
    )


class PuzzleGenerateSchema(PuzzleSize):
    seed: int = Field(
        default=0,
        title="Seed of the puzzle",
        description="The seed of the puzzle.",
        example=0,
    )
    difficulty: float = Field(
        ...,
        gt=0,
        le=0.75,
        title="Difficulty of the puzzle",
        description="The difficulty of the puzzle. Closer to 0 is easier, closer to 1 is harder",
        example=0.5,
    )


class UnsolvedPuzzleSchema(PuzzleSize):
    puzzle: List[List[Union[int, None]]] = Field(
        ...,
        title="Puzzle",
        description="The puzzle",
        example=[
            [9, None, None, 2, None, 4, None, None, None],
            [3, None, None, 5, 8, None, None, 9, 7],
            [8, None, 5, None, 3, None, None, 6, None],
            [7, 8, None, 4, 6, 2, 9, None, 3],
            [6, None, None, 7, 5, None, 1, None, None],
            [4, 5, None, None, 9, None, None, None, None],
            [None, None, 8, None, 4, 9, 5, 2, None],
            [None, 4, 6, None, 7, 5, None, 3, None],
            [5, None, 9, 6, None, 8, None, 1, None],
        ],
    )

    @root_validator(pre=False, skip_on_failure=True)
    def puzzle_values(cls, values):
        width, height = len(values["puzzle"][0]), len(values["puzzle"])  # 9, 9
        if width != height:
            raise ValueError("Puzzle is not square")
        grid_size = values["width"] * values["height"]  # 3 * 3 = 9
        if grid_size != width or grid_size != height:
            raise ValueError("Grid size does not match puzzle size")
        for row in values["puzzle"]:
            if len(row) != grid_size:
                raise ValueError("Puzzle is not square")
            row = [value for value in row if value is not None]
            if len(row) != len(set(row)):
                raise ValueError("Puzzle contains duplicate values")
            if any(value < 1 or value > grid_size for value in row):
                raise ValueError("Puzzle contains invalid values")
        items = [item for sublist in values["puzzle"] for item in sublist if item is not None]
        if len(items) < grid_size**2 * 0.25:
            raise ValueError("Puzzle is too empty")
        return values


class PuzzleSchema(UnsolvedPuzzleSchema):
    solution: List[List[int]] = Field(
        ...,
        title="Solution",
        description="The solution",
        example=[
            [9, 6, 7, 2, 1, 4, 3, 8, 5],
            [3, 1, 4, 5, 8, 6, 2, 9, 7],
            [8, 2, 5, 9, 3, 7, 4, 6, 1],
            [7, 8, 1, 4, 6, 2, 9, 5, 3],
            [6, 9, 2, 7, 5, 3, 1, 4, 8],
            [4, 5, 3, 8, 9, 1, 6, 7, 2],
            [1, 7, 8, 3, 4, 9, 5, 2, 6],
            [2, 4, 6, 1, 7, 5, 8, 3, 9],
            [5, 3, 9, 6, 2, 8, 7, 1, 4],
        ],
    )


app = FastAPI(
    title="Sudoku API",
    description="Sudoku API is a RESTful API for generating and solving sudoku puzzles.",
    version="0.0.1",
    contact={
        "name": "Hasan Sezer Taşan",
        "url": "http://www.hasansezertasan.com",
        "email": "hasansezertasan@gmail.com",
    },
    responses={
        404: {
            "description": "Not found",
        },
        500: {
            "description": "Internal Server Error",
        },
    },
)


@app.exception_handler(UnsolvableSudoku)
async def unsolvable_sudoku(
    request: Request,
    exc,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "Sudoku is unsolvable",
        },
    )


@app.exception_handler(Exception)
async def http_exception_handler(
    request: Request,
    exc,
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal Server Error",
        },
    )


@app.post(
    path="/generate",
    response_model=PuzzleSchema,
    name="Generate Sudoku Puzzle",
    operation_id="generate-puzzle",
    description="Generate a sudoku puzzle",
)
async def puzzle_generate_with_json_body(
    data: PuzzleGenerateSchema = Body(...),
) -> PuzzleSchema:
    sudoku = Sudoku(
        width=data.width,
        height=data.height,
        seed=data.seed,
    ).difficulty(difficulty=data.difficulty)
    return PuzzleSchema(
        width=data.width,
        height=data.height,
        puzzle=sudoku.board,
        solution=sudoku.solve().board,
    )


@app.post(
    path="/solve",
    response_model=PuzzleSchema,
    name="Solve Sudoku Puzzle",
    operation_id="solve-puzzle",
    description="Solve a sudoku puzzle",
)
async def puzzle_solve_with_json_body(
    data: UnsolvedPuzzleSchema = Body(...),
) -> PuzzleSchema:
    return PuzzleSchema(
        width=data.width,
        height=data.height,
        puzzle=data.puzzle,
        solution=Sudoku(
            width=data.width,
            height=data.height,
            board=data.puzzle,
        )
        .solve()
        .board,
    )
