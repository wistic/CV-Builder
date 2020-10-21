### Installation

- Install [Docker](https://docs.docker.com/engine/install/)
- Run the following command:
```shell
 docker run -d \
    -p 3306:3306 \
    -v todo-mysql-data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=secret \
    -e MYSQL_DATABASE=todos \
    mysql
```
