from userapp.settings.base import ALLOWED_HOSTS

ALLOWED_HOSTS += [
    "http://localhost:3000",
    "localhost",
    "127.0.0.1",
    "user-app-hvr7.onrender.com",
]

DEBUG = True
