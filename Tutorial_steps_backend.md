# Setup virtual environment
python -m venv env
env/Scripts/activate.bat

# install requirements
# it is possible to run from text file
# install requirements
pip install -r requirements.txt
# start project, in this case, the backend
django-admin startproject backend

# create app (to organize functions of the application)
python manage.py startapp api

# add necessary details in backend/settings.py

# JWT is needed. Access token and Refresh token created. Access token expires faster tan refresh token

# time to create a serializer.py and import the following
from rest_framework import serializers
from django.contrib.auth.models import User

# and define UserSerializer

# User present because django handles authentication
# the serializer converts the python data to json compatible data

# Add the following to views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Class based view that allows user registration
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# Add the following to backend/urls.py
from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
]


# views return the data, URLs is how we get them

# recall make migrations and migrate every time we edit models
python  manage.py makemigrations
python  manage.py migrate

# can run server on local host
python  manage.py runserver

# Read error page as localhost home not defined
# Test the urls

# Create Note model and add User foreign key to establish relationships

# Add Note to models

from django.db import models
from django.contrib.auth.models import User

<!-- # Django hadles conversion to Database codes -->
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # auto_now_add, automatically added
    created_at = models.DateTimeField(auto_now_add=True) 
    # foreign key for entity relatioships
    # on_delete, if user deleted delete user's notes
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title

# Add NoteSerializer to serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}
# Add Notes to view
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer,NoteSerializer
from .models import Note

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

# Create api/urls.py for notes to be used in backend/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
]

# Add api/urls.py patterns to backend/urls.py
path("api/", include("api.urls")),

# After finsihing work on the frontend, time to deploy
# Create a database
# choreo allows for mySQL consider that going forward
# Create environment variable file for the database (backend/.env) and fill the details below

DB_HOST = ""
DB_PORT = ""
DB_USER = ""
DB_NAME = ""
DB_PWD =  ""

# Next alter settings.py
load_dotenv() 
<!-- loads the environment file for us -->

# Change databases. Working with Postgres 
# TODO: find mySQL method 
# Add the following
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PWD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# Migrate because of new database

python manage.py migrate

# Run the server
<!-- backend -->
python manage.py runserver

<!-- frontend -->
npm run dev

# include a gitignore in backend and frontend to remove env file, should not be pushed

# in backend creae .choreo/endpoints.yaml and include endpoints, in clude the lines below

version: 0.1
endpoints:
 - name: "REST API"
   port: 8000
   type: REST
   networkVisibility: Public
   context: /

# Include backend/Procfile and add the following command
# the 0.0.0.0:8000 means run on any origin or public IP address of the server we are executing on
web: python manage.py runserver 0.0.0.0:8000