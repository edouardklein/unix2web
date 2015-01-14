# This will install the web-app on a ubuntu server
# intallation instructions follow recipe given here http://blog.garethdwyer.co.za/2013/07/getting-simple-flask-app-running-on.html . Thanks !

APPNAME=unix2web
INSTALLDIR=/var/www/$APPNAME
sudo yes | apt-get install apache2 libapache2-mod-wsgi python-flask
sudo mkdir -p $INSTALLDIR
sudo cp index.html $INSTALLDIR/
sudo cp index.css $INSTALLDIR/
sudo cp $APPNAME.py $INSTALLDIR/
sudo cp $APPNAME.wsgi $INSTALLDIR/
sudo cp 100$APPNAME.conf /etc/apache2/sites-available
sudo a2dissite 000-default
sudo a2ensite 100$APPNAME
sudo /etc/init.d/apache2 restart


