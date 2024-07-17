from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer,NoteSerializer
from .models import Note

# Create your views here.

# Class based view that allows user registration
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all() # check to not create an already existing user
    serializer_class = UserSerializer # Info about the data
    permission_classes = [AllowAny] # see who can call it, allowing anyone for now

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer # Info about the data
    permission_classes = [IsAuthenticated] # see who can call it, Only authenticated for now

    # Views notes written by you
    # overriding get_queryset from generics
    def get_queryset(self):
        # Due to authenticating ourselves, the user should never be anonymous
        user = self.request.user
        # use user as a filterto get their notes
        return Note.objects.filter(author=user)

    # overriding perform_create from generics
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