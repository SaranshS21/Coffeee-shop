import os
import sys

# Add the parent directory of your Django project to the Python path
sys.path.append('/opt/render/project/src/myproject')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
