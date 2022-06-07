#!/usr/bin/env bash
flask db migrate
flask db upgrade
flask run --host=0.0.0.0