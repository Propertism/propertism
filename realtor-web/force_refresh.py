#!/usr/bin/env python
"""Force Django to reload templates by touching settings.py"""
import os
from pathlib import Path

# Touch the settings file to trigger Django reload
settings_file = Path(__file__).parent / 'realtor_project' / 'settings.py'
settings_file.touch()

print("✅ Touched settings.py - Django will reload on next request")
print("🔄 Now refresh your browser with Ctrl+F5")
