from __future__ import unicode_literals
from django.db import models
import re 
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z\s]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 1:
            errors["fname"] = "First name field is required"
        if len(postData['lname']) < 1:
            errors["lname"] = "Last name field is required"
        if not NAME_REGEX.match(postData['fname']):
            errors["fname"] = "First name cannot contain any numbers or special characters!"
        if not NAME_REGEX.match(postData['lname']):
            errors["lname"] = "Last name cannot contain any numbers or special characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Email is invalid"
        if len(postData['password']) < 8:
            errors["password"] = "Password is invalid"
        if not postData['password'] == postData['password2']:
            errors["password2"] = "Passwords must match"
        if len(User.objects.filter(email=postData["email"])) > 0:
            errors["email"] = "Email already exist"
        if len(errors) == 0:
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(fname=postData['fname'], lname=postData['lname'], email=postData['email'], user_level="normal", password=hash1 )
            errors['id'] = user.id
            errors['user_level'] = user.user_level
            if user.id == 1:
                user.user_level = "admin"
                user.save()
        return errors

    def login_validator(self, postData):
        errors={}
        checklogin= User.objects.filter(email=postData["email"])
        if checklogin:
            if bcrypt.checkpw(postData['password'].encode(), checklogin[0].password.encode()) == True:
                errors["user"]=checklogin[0]

            else:
                errors["errorsuser"]="Login failed"
        else:
            errors["errorsuser"]="Login failed"
        return errors

    def edit_validator(self, postData):
        errors={}
        if len(postData['fname']) < 1:
            errors["fname"] = "First name field is required"
        if len(postData['lname']) < 1:
            errors["lname"] = "Last name field is required"
        if not NAME_REGEX.match(postData['fname']):
            errors["fname"] = "First name cannot contain any numbers or special characters!"
        if not NAME_REGEX.match(postData['lname']):
            errors["lname"] = "Last name cannot contain any numbers or special characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Email is invalid"
       
        if len(errors) == 0:
            this_user = User.objects.filter(id= postData["this_user_id"])
            print postData
            if postData["user_level"] == "admin":

                this_user.update(fname=postData['fname'], lname=postData['lname'], email=postData['email'], user_level = postData['ulvl'])
            else:

                this_user.update(fname=postData['fname'], lname=postData['lname'], email=postData['email'])
            
            
        return errors

    def pw_validator(self, postData):
        errors={}
        if len(postData['password']) < 8:
            errors["password"] = "Password is invalid"
        if not postData['password'] == postData['password2']:
            errors["password2"] = "Passwords must match"
        if len(errors) == 0:
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            this_user = User.objects.filter(id= postData["this_user_id"])
            this_user.update(password=hash1)
            
        return errors

    def message_validator(self, postData):
        errors={}
        if len(postData["message"]) == 0:
            errors["message"] = "Message cannot be empty!"
        if len(errors) == 0:
            Message.objects.create(content=postData["message"], messenger_id=postData["this_user_id"], receiver_id=postData["receiver_id"])
        
        return errors

    def comment_validator(self, postData):
        errors={}
        if len(postData["comment"]) == 0:
            errors["comment"] = "Comment cannot be empty!"
        if len(errors) == 0:
            Comment.objects.create(content=postData["comment"], commenter_id=postData["this_user_id"], message_id=postData["this_message_id"])
        
        return errors
    

class User(models.Model):
    fname = models.CharField(max_length = 255)
    lname = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    user_level = models.CharField(max_length = 255)
    desc = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    
    
    objects = UserManager()


class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    receiver = models.ForeignKey(User, related_name= "received_msgs", default="1", null=True)
    messenger = models.ForeignKey(User, related_name = "messages")
    objects = UserManager()

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    commenter = models.ForeignKey(User, related_name = "comments", default="1", null=True)
    message = models.ForeignKey(Message, related_name = "comments")
    objects = UserManager()