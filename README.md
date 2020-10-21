### Installation

- Install [MySQL](https://dev.mysql.com/downloads/) or
- Install [Docker](https://docs.docker.com/engine/install/) and run the following command:
```shell
 $ docker run -d \
      -p 3306:3306 \
      -v cv-data:/var/lib/mysql \
      -e MYSQL_ROOT_PASSWORD=password \
      mysql
```

- Test your Mysql installation by running
```shell
 $ mysql -u root -h 127.0.0.1 -p
```

### Setup Database

- Execute [CV_Builder.sql](https://github.com/wistic/CV-Builder/blob/master/reference-material/CV_Builder.sql) via [shell](https://dev.mysql.com/doc/refman/8.0/en/mysql-batch-commands.html) or using [MySQL WorkBench](https://dev.mysql.com/downloads/workbench/).
- Then run [testing.sql](https://github.com/wistic/CV-Builder/blob/master/reference-material/testing.sql) to add a demo test entry.


### Setup Python Environment

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
- Update [config.py](https://github.com/wistic/CV-Builder/blob/master/config.py) to include your MySQL Password.
- Export FLASK Environment variables and run the application
```shell
 $ EXPORT FLASK_APP=app.py
 $ flask run
```

#### Additional notes:
- To run in development mode
```shell
 $ EXPORT FLASK_ENV=development
 $ EXPORT FLASK_DEBUG=1
```
- For additional security, export your MySQL Password as an environment variable
```shell
 $ EXPORT MYSQLPASSWORD=<your-password-here>
```
