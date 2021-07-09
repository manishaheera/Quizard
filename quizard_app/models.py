from django.db import models
from django.db.models.fields import related
from django.utils import tree
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
forbidden_chars = ['@#$%^&*()_+=[{/}\|]?,;:.~`!"']

# MODEL MANAGERS
class UserManager(models.Manager):
    def validator(self, postData):

        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 letters long"

        if not postData['first_name'].isalpha():
            errors['first_name_alpha'] = "First name must contain letters only"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 letters long"

        if not postData['last_name'].isalpha():
            errors['last_name_alpha'] = "Last name must contain letters only"

        if len(postData['username']) < 5:
            errors['username'] = "Username must be at least 6 letters long"
        
        for char in forbidden_chars:
            if char in postData['username']:
                errors['username'] = "You used an invalid character. Username can only contain letters and numbers."

        username_unique_check = User.objects.filter(username=postData['username'])

        if username_unique_check:
            errors['username'] = "That username is already taken"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valid email address."

        email_unique_check = User.objects.filter(email=postData['email'])

        if email_unique_check:
            errors['email'] = "Please enter a unique email."


        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."

        if postData['password'] != postData['confirm_password']:
            errors['confirm'] = "Passwords did not match"

        return errors

    def register(self, postData):
        safe_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()

        return User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], username=postData['username'], email=postData['email'], password = safe_password)

    def authenticate(self, email, password):
        users = User.objects.filter(email = email)
        if users:
            user = users[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
        
        return False

class QuizManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['quiz_name']) < 1:
            errors['quiz_name'] = "Quiz must have a title!"

        if len(postData['description']) != 0 and len(postData['description']) < 5:
            errors['description'] = "Description has to be longer than 5 characters!"

        return errors

class QuestionManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['entry']) < 1 and len(postData['answer']) != 0:
            errors['entry'] = "The prompt can't be empty!"

        if len(postData['answer']) < 1 and len(postData['entry']) != 0:
            errors['answer'] = "Question must have an answer!"


        return errors

#  MODELS
class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length = 60)
    profile_photo = models.ImageField(default='default.png', upload_to = "images/")

    # SPACE FOR RELATIONSHIPS
    # created_quizzes > created_by in quiz class
    # liked_quizzes > liked_by in quiz class
    # disliked_quizzes > disliked_by in quiz class
    # quizzes_taken > taken_by in quiz class

    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Quiz(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    category_choices = [
        ("1", "Fun"),
        ("2", "Geography"),
        ("3", "Language"),
        ("4", "Literature"),
        ("5", "Math"),
        ("6", "Miscellaneous"),
        ("7", "Science"),
        ("8", "Social Studies")
    ]
    category = models.CharField(max_length=25, choices=category_choices, default="1")
    created_by = models.ForeignKey(User, related_name="created_quizzes", on_delete=models.SET_NULL, null=True)
    liked_by = models.ManyToManyField(User, related_name="liked_quizzes", blank=True)
    disliked_by = models.ManyToManyField(User, related_name="disliked_quizzes", blank=True)
    taken_by = models.ManyToManyField(User, related_name="quizzes_taken", blank=True)
    
    # SPACE FOR RELATIONSHIPS
    # questions > quiz from question class

    objects = QuizManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_by}/Quiz/{self.name}/ID/{self.id}"


class Question(models.Model):
    entry = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    image = models.ImageField(null=True,blank=True, upload_to="images/")
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    objects = QuestionManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quiz.created_by}/Quiz/{self.quiz.name}/Question/{self.id}"