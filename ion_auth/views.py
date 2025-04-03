from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from requests_oauthlib import OAuth2Session
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from oauthlib.oauth2 import TokenExpiredError
import json

CLIENT_SECRET = 'zU4tcWJTWvsnREVoZUlajOjUHxpqjquLBrQWso7XdDjdEi5jMsGqvfIYpR9uNV7wrD1sWYHRfmWLduzBOBjLMz5vP1dUUmk2qQwJiPaQbCIM7qkGKGeMdkf6807GaLcd'
CLIENT_ID = 'Spfu5kktSVTIzAqI3kAsHbORxlellqWZsEnJZhKM'
REDIRECT_URI = 'http://localhost:8000/oauth/redirect'
AUTH_URL = 'https://ion.tjhsst.edu/oauth/authorize/'
TOKEN_URL = 'https://ion.tjhsst.edu/oauth/token/'
PROFILE_URL = 'https://ion.tjhsst.edu/api/profile'

def home(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"msg": "hello"})

def ion_login(request: HttpRequest):
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["read", "write"])
    authorization_url, state = oauth.authorization_url(AUTH_URL)
    return redirect(authorization_url)

def ion_login_redirect(request: HttpRequest):
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["read", "write"])
    code = request.GET.get('code')

    try:
        # Fetch the token
        token = oauth.fetch_token(TOKEN_URL, code=code, client_secret=CLIENT_SECRET)

        # Get the user's profile data
        profile_response = oauth.get(PROFILE_URL)
        profile_data = json.loads(profile_response.content.decode())

        # Get the Ion username and email from the profile data
        ion_username = profile_data.get("ion_username")
        email = profile_data.get("email", f"{ion_username}@tjhsst.edu")  # Use a default email if not provided

        # Check if the user exists, or create a new one
        user, created = User.objects.get_or_create(username=ion_username, defaults={"email": email})

        if created:
            # Set a random password for the new user
            user.set_password(User.objects.make_random_password())
            user.save()

        # Log the user in
        login(request, user)

        # Redirect to the home page
        return redirect('/')

    except TokenExpiredError:
        # Handle token expiration and refresh
        args = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
        token = oauth.refresh_token(TOKEN_URL, **args)
        return redirect('/oauth/redirect') 

    except Exception as e:
        print(f"Error during OAuth: {e}")
        return redirect('/')
def ion_logout_redirect(request: HttpRequest):
    logout(request)
    return redirect('/') 