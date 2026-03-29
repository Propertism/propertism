import os

import django
from django.contrib.auth import get_user_model


def main() -> None:
    django.setup()

    username = os.environ["ADMIN_USERNAME"]
    email = os.environ["ADMIN_EMAIL"]
    password = os.environ["ADMIN_PASSWORD"]

    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        },
    )

    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password(password)
    user.save()

    print("created" if created else "updated")
    print(user.username)


if __name__ == "__main__":
    main()
