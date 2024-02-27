REQUIREMENTS:

pip install tkcalendar
pip install pymysql

create phpmyadmin db named tasklist

SQL:

CREATE TABLE `tasks`(
    `PRIORITY` varchar(200) NOT NULL,
    `TITLE` varchar(200) NOT NULL,
    `DATE` varchar(200) NOT NULL,
    `TIME` varchar(200) NOT NULL,
    PRIMARY KEY (`TITLE`)
)
