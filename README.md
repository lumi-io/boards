# Boards

Application Tracking System

[![License](http://img.shields.io/badge/License-MIT-brightgreen.svg)](./LICENSE) [![build Actions Status](https://github.com/lumi-io/boards/workflows/build/badge.svg)](https://github.com/lumi-io/boards/actions)

## Notes:

### To activate a virtual environment

```bash
pipenv shell
```

### To deactivate a virtual environment

```bash
deactivate
exit
```

### To install all the dependencies from pipenv

```bash
pipenv install
```

### To install a specific dependency into the project (make sure you are within the virtual environment)

```bash
pipenv install dependency_name
```

### To run the Flask App

```bash
export FLASK_APP=manage.py
flask run
```

### To run the Flask App on Debug Mode

```bash
export FLASK_APP=manage.py
export FLASK_ENV=development
flask run
```



### Documentation/Guides
- https://flask.palletsprojects.com/en/1.0.x/
- https://flask.palletsprojects.com/en/1.1.x/tutorial/views/
- https://flask.palletsprojects.com/en/1.1.x/patterns/mongoengine/
