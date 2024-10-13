from urllib.parse import urlparse


def parse_db_url(url):
    parsed_url = urlparse(url)
    return {
        "ENGINE": "django.db.backends.mysql",
        "NAME": parsed_url.path[1:],
        "USER": parsed_url.username,
        "PASSWORD": parsed_url.password,
        "HOST": parsed_url.hostname,
        "PORT": int(parsed_url.port) if parsed_url.port else 3306,
    }
