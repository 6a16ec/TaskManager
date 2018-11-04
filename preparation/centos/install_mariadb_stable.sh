yum -y install MariaDB-server-10.1.31

systemctl start mariadb
systemctl start mariadb

sh ./mysql_secure_installation.sh

/file!

sudo systemctl start postgresql
sudo systemctl enable postgresql

https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-centos-7

yum -y install MariaDB-server-10.1.31 MariaDB-client-10.1.31 MariaDB-shared-10.1.31 MariaDB-common-10.1.31

?? sudo yum install MariaDB-server-10.1.31 MariaDB-client-10.1.31 MariaDB-shared-10.1.31 MariaDB-common-10.1.31

/usr/bin/mysql_secure_installation