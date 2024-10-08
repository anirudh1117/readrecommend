"""
WSGI config for BookRecommend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookRecommend.settings')
sys.path.append('/home/ubuntu/read-recommend/readrecommend')
sys.path.append('/home/ubuntu/read-recommend/readrecommend/BookRecommend')

application = get_wsgi_application()
