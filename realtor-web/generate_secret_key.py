#!/usr/bin/env python
"""
Generate a secure Django SECRET_KEY
Run this script and copy the output to your .env file
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("\n" + "="*70)
    print("DJANGO SECRET KEY GENERATOR")
    print("="*70)
    print("\nYour new SECRET_KEY:")
    print("-"*70)
    print(secret_key)
    print("-"*70)
    print("\nCopy this key to your .env file:")
    print(f"DJANGO_SECRET_KEY={secret_key}")
    print("\n⚠️  IMPORTANT: Keep this key secret! Never commit it to version control.")
    print("="*70 + "\n")
