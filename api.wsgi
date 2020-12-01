#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/html/FlaskAPI')

from flaskapp import app as application