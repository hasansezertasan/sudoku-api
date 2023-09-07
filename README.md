# Sudoku API with FastAPI

The goal of this project is to create a sudoku API using FastAPI. We could have developed a sudoku solver manually, but we decided to use a great module called PySudoku to focus on the API development and deployment.

We highly reccomend for new developers to try to develop their own sudoku solver, it's a great exercise! You will learn great concepts like backtracking and recursion. There are lots of resources online.

## Technologies used

- Sudoku Solver Library: [PySudoku](https://pypi.org/project/py-sudoku/):
  - Uses recursive backtracking to solve sudoku puzzles.
- Backend: [FastAPI](https://fastapi.tiangolo.com/):
  - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- Deployment: Docker, Docker Compose:
  - Docker is a set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers.
  - Docker Compose is a tool for defining and running multi-container Docker applications.
- Development Tools:
  - Poetry:
    - Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.
  - Pre-commit:
    - A framework for managing and maintaining multi-language pre-commit hooks.
  - Black:
    - The uncompromising Python code formatter.
  - Isort:
    - A Python utility / library to sort imports alphabetically, and automatically separated into sections and by type.
  - Flake8:
    - A tool that glues together pep8, pyflakes, mccabe, and third-party plugins to check the style and quality of some python code.
  - Pytest:
    - The pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.

## How to run

### Requirements

- Docker
- Docker Compose

### Steps

1. Clone the repository
2. Run `docker-compose up --build`
3. Go to `http://localhost:8000/docs` to see the API documentation
4. Enjoy!

## API Documentation

FastAPI provides a great documentation interface. You can access it by going to `http://localhost:8000/docs` after running the application.

## Tests

To run the tests, you can run `docker-compose exec server pytest` after running the application.

## Project Structure

```bash
.
├── Dockerfile # Docker configuration
├── LICENSE # MIT License
├── README.md # This file
├── docker-compose.yml # Docker Compose configuration
├── pyproject.toml # Poetry configuration
├── .pre-commit-config.yaml # Pre-commit configuration
├── main.py # FastAPI Application
├── toolbox.py # Typer CLI Application
├── .github # Github Actions
└── test.py # Tests
```

- `main.py` contains the FastAPI application with the endpoints, schemas and the business logic. It's only 200 lines of code! We kept everything in one file to make it easier to understand for new developers.
- `toolbox.py` contains the Typer CLI application. We used Typer to showcase PySudoku abilities.
- `test.py` contains the tests for the FastAPI application. We used Pytest to write the tests. We have 100% coverage.
- `Dockerfile` contains the Docker configuration for the application.
- `docker-compose.yml` contains the Docker Compose configuration for the application.
- `pyproject.toml` contains the Poetry configuration for the application.
- `.pre-commit-config.yaml` contains the Pre-commit configuration for the application.
- `LICENSE` contains the MIT License for the application.
- `README.md` contains the README for the application.

## Author

- [hasansezertasan](https://www.github.com/hasansezertasan)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

It's an open source project mainly for educational purposes. Feel free to use it however you want.
