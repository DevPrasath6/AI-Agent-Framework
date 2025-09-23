#!/usr/bin/env python
import os
import sys

# Ensure repository root is on sys.path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Ensure Django uses the test settings by default when running locally
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_framework.test_settings")
# Late import because we must set DJANGO_SETTINGS_MODULE before importing Django
from django.core.management import execute_from_command_line  # noqa: E402

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
