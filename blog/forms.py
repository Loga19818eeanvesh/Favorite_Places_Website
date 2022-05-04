from cProfile import label
from dataclasses import field
from django import forms
from .models import Comment

class CommentForm(forms.Form):
    text = forms.CharField(max_length=400,widget=forms.Textarea,label="Your Comment")
    
class PostForm(forms.Form):
    title = forms.CharField(max_length=150,label="Place Name")
    slug = forms.SlugField()
    address = forms.CharField(max_length=200,label="Address")
    image = forms.ImageField(label="Upload Image")
    content = forms.CharField(min_length=10,label="Describe about Place",widget=forms.Textarea)


class RegisterForm(forms.Form):
    user_name = forms.CharField(label="User Name",max_length=150,min_length=5,required=True,error_messages={
        "required" : "User_Name must not be empty.",
        "min_length" : "User_Name mush have atleast 5 characters.",
        "max_length" : "User_Name mush not be greater than 150 characters."
    })
    first_name = forms.CharField(label="First Name",max_length=100,required=True,error_messages={
        "required" : "User_Name must not be empty.",
        "max_length" : "User_Name mush not be greater than 100 characters."
    })
    last_name = forms.CharField(label="Last Name",max_length=100,required=True,error_messages={
        "required" : "User_Name must not be empty.",
        "max_length" : "User_Name mush not be greater than 100 characters."
    })
    user_email = forms.EmailField(label="Your Email",required=True)
    password = forms.CharField(label="Enter Password",max_length=32, widget=forms.PasswordInput)
    password1 = forms.CharField(label="Confirm Password",max_length=32, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    user_name = forms.CharField(label="User Name",max_length=150,min_length=5,required=True,error_messages={
        "required" : "User_Name must not be empty.",
        "min_length" : "User_Name mush have atleast 5 characters.",
        "max_length" : "User_Name mush not be greater than 150 characters."
    })
    password = forms.CharField(label="Enter Password",max_length=32, widget=forms.PasswordInput)
    




    
