## Docker Installation (Recommended)
- Install [Docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/).
- Clone the repo and run docker-compose.
```shell
 $ git clone https://github.com/wistic/CV-Builder.git
 $ cd CV-Builder
 $ docker-compose up
```
- Go to [localhost:5000](http://localhost:5000/) to use the application.
- Run `docker-compose down` to stop the containers.

Note: To use [adminer](https://www.adminer.org/), go to [localhost:5001](http://localhost:5001/).

## Normal Installation

- Install [MySQL](https://dev.mysql.com/downloads/).
- Test your Mysql installation by running
```shell
 $ mysql -u root -h 127.0.0.1 -p
```

#### Setup Database

- Execute [CV_Builder.sql](https://github.com/wistic/CV-Builder/blob/master/reference-material/CV_Builder.sql) via [shell](https://dev.mysql.com/doc/refman/8.0/en/mysql-batch-commands.html) or using [MySQL WorkBench](https://dev.mysql.com/downloads/workbench/).
- Then run [testing.sql](https://github.com/wistic/CV-Builder/blob/master/reference-material/testing.sql) to add a demo test entry.


#### Setup Python Environment

- Clone the repo
```shell
 $ git clone https://github.com/wistic/CV-Builder.git
```
- Install [virtualenv](https://pypi.org/project/virtualenv/) and install the requirements
```shell
 $ cd CV-Builder
 $ pip install virtualenv
 $ virtualenv venv
 $ source venv/bin/activate
 $ pip install -r requirements.txt
```
- Edit [config.py](https://github.com/wistic/CV-Builder/blob/master/config.py) according to your local configuration.
- Export FLASK Environment variables and run the application
```shell
 $ EXPORT FLASK_APP=app.py
 $ flask run
```
- Go to [localhost:5000](http://localhost:5000/) to use the application.

#### Additional notes:
- To run in development mode
```shell
 $ EXPORT FLASK_ENV=development
 $ EXPORT FLASK_DEBUG=1
```
- For additional security, export the configuration variables as an environment variable
```shell
 $ EXPORT MYSQL_PASSWORD=<your-password-here>
```
