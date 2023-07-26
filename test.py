# Django setup
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LangLearn.settings')  # replace 'myproject' with your project name
django.setup()

# import the function
from user_management.user_buffer import get_practice_buffer  # replace with the actual module name


def test_get_practice_buffer():
    username = 'adrian'  # replace with the actual username
    result = get_practice_buffer(username)

    print(result)


if __name__ == "__main__":
    test_get_practice_buffer()
