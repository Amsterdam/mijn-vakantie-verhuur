# Mijn Vakantie Verhuur API

## Introduction

A REST API which discloses the Landelijke Vakantie Verhuur data


### Local development

1. Clone repo and `cd` in
2. Create a virtual env and activate
3. Run `pip install -r requirements.txt`
4. Set environment variables:
   - `export FLASK_APP=app/server.py`
    
5. Run `flask run`
6. `curl http://localhost:5000` to see if api is up-and-running

### Testing
In your env created for Local development

1. Run `python -m unittest`
