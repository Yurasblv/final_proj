#!/usr/bin/env bash
flask db init
flask db migrate
flask db upgrade
#flask create
flask run --host=0.0.0.0