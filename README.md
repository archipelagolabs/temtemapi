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
