temapi
======

Temtem API with data extracted from Gamepedia

**Live version: http://api.temtemapi.com/redoc**


Setup
-----

Temapi uses `poetry` for dependency management.
Install dependencies with:

```
$ poetry install
```

Extractor
---------

Running the extractor:

```
$ poetry run extract
```

Output will be written on json files in outputs/

API
---

Running the API:

```
$ poetry run uvicorn temapi.api:app --reload
```

The API will be available at http://localhost:8000/ and the docs at http://localhost:8000/redoc

Example URL: http://localhost:8000/temtems/72


Contributing
------------

When contributing, there are tasks that can be executed using `invoke`:

To run Pylint (prints a pretty complete report about code quality):

```
inv lint
```

**Note**: If your editor is able to show pylint warnings, you may want to configure it, or
set your PYLINTRC variable to point to the `pylintrc` file in this repository,
since the raw config for pylint is a bit more than what we care about. The
`lint` task on `invoke` already uses the proper `pylintrc` file.

To run Flake8 (simpler linter):

```
inv flake8
```

To run our formatters:

```
inv format
```

To check formatting (useful for git hooks and CI):

```
inv format-check
```

Please run everything on your submission before asking for a review on your PR.
