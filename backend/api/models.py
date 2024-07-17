from django.db import models
from django.contrib.auth.models import User

# Django hadles conversion to Database codeS
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