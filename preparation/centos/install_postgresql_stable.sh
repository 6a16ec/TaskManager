yum -y install postgresql-server postgresql-contrib
postgresql-setup initdb

/file!

sudo systemctl start postgresql
sudo systemctl enable postgresql