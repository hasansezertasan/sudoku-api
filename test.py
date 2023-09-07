import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

test_generate_data = [
    (3, 3, 0, 0.75),
    (2, 2, 1, 0.5),
]

@pytest.mark.parametrize("width, height, seed, difficulty", test_generate_data)
def test_generate(width, height, seed, difficulty):
    response = client.post(
        url="/generate",
        json={
            "width": width,
            "height": height,
            "seed": seed,
            "difficulty": difficulty,
        },
    )
    assert response.status_code == 200


def test_solve():
    response = client.post(
        url="/solve",
        json={
            "width": 3,
            "height": 3,
            "puzzle": [
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
        },
    )
    assert response.status_code == 200
