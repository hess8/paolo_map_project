sudo sudo -u postgres dropdb paolo
sudo sudo -u postgres createdb paolo -O $USER
sudo sudo -u postgres psql -d paolo -c 'CREATE EXTENSION postgis;' 
#sudo sudo -u postgres psql -d paolo -c 'CREATE EXTENSION fuzzystrmatch;' #not needed

./manage.py makemigrations paolo_map
./manage.py migrate paolo_map
