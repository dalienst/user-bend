from userapp.settings.base import ALLOWED_HOSTS

ALLOWED_HOSTS += [
    "http://localhost:3000",
    "localhost",
    "127.0.0.1",
    "user-app-hvr7.onrender.com",
    "http://127.0.0.1:3000",
    "user-bend-production.up.railway.app",
]

DEBUG = True
