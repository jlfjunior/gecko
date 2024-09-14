UPDATE mysql.user SET host='%' WHERE user='root';
FLUSH PRIVILEGES;
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'gecko!23';
FLUSH PRIVILEGES;