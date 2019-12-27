from django import forms
from .models import Comment, Newletter, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'message')

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('categories','title','descriptions','slug','image','author','publish','status')

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newletter
        fields = ('email',)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={
        
        'class' : 'form-control',
        'placeholder' : 'Your name',
        
        
    }))
    email_from = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your email',
        
    }))
    subject = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={
        
        'class' : 'form-control',
        'placeholder' : 'Subject',
        
        
    }))
    message = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your Message',
    }))

class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Password',
    }))