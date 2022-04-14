# PythonAPI
A simple API written in python by _jean-baptiste.despujol_ and _martin.mallein_. \
We used the fastapi framework, pytest for the tests, it contains a production and a test sqlite database.

*The documentation is available with the **/docs** route*

# Install dependencies
```$> cd PythonAPI && poetry install```

# Launch API
In the folder of the project: \
```$> poetry run uvicorn pythonapi.app:app --reload```

# Run tests
```$> poetry run pytest```
