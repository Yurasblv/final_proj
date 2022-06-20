- [x] FINISHED

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### All command for up and down project are in 
>`Makefile`
 
To run this project in development,
you will need to add the following 
environment variables to your .env file:
>`SECRET_KEY`
`SQLALCHEMY_DATABASE_URI`
`POSTGRES_USER`
`POSTGRES_PASSWORD`
`POSTGRES_DB`
`POSTGRES_PORT`


Also u can run this project
in test mode via docker-compose,
but at least u need to make .env.test file with following
keys:

>`SECRET_KEY`
`POSTGRES_DB`
`POSTGRES_USER`
`POSTGRES_PASSWORD`
`SQLALCHEMY_DATABASE_URI`  
! `TESTING` = `True` !
 
and run command `coverage run -m pytest .` inside tests folder.




