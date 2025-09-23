#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == '__main__':
    # Ensure the repository root is on sys.path so sibling packages like `src`
    # can be imported when running manage.py from within `django_app/`.
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root))

    # Use test settings when running tests to avoid external DB dependencies
    if 'test' in sys.argv:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_framework.test_settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_framework.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise
    execute_from_command_line(sys.argv)
