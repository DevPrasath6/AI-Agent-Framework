import os
import sys

# Ensure project root is on sys.path so pytest can import the django project package
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Default Django settings for pytest-django if not provided externally
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_framework.test_settings")
# Ensure the Django app package directory is available on sys.path so apps
# declared with top-level labels (like 'agents') can be imported during test
# collection.
DJANGO_APP_PATH = os.path.join(ROOT, "django_app")
if os.path.isdir(DJANGO_APP_PATH) and DJANGO_APP_PATH not in sys.path:
    sys.path.insert(0, DJANGO_APP_PATH)
