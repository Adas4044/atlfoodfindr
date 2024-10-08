from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from restaurants.models import UserProfile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New Username'
        })


# Updated UserRegistrationForm to include specific security questions
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    # Specific security questions
    security_answer_1 = forms.CharField(label="What is your favorite color?")
    security_answer_2 = forms.CharField(label="What is your favorite food?")
    security_answer_3 = forms.CharField(label="What is your favorite movie?")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'security_answer_1', 'security_answer_2', 'security_answer_3']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Save security questions and answers to UserProfile
            UserProfile.objects.create(
                user=user,
                security_answer_1=self.cleaned_data['security_answer_1'],
                security_answer_2=self.cleaned_data['security_answer_2'],
                security_answer_3=self.cleaned_data['security_answer_3'],
            )
        return user


# Security Question Form for password reset
class SecurityQuestionForm(forms.Form):
    username = forms.CharField(label="Enter your username")
    email = forms.EmailField(label="Enter your email")
    answer_1 = forms.CharField(label="Answer to 'What is your favorite color?'")
    answer_2 = forms.CharField(label="Answer to 'What is your favorite food?'")
    answer_3 = forms.CharField(label="Answer to 'What is your favorite movie?'")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")


# CustomUserCreationForm with security questions
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add the email field

    # Add specific security questions
    answer_1 = forms.CharField(label="What is your favorite color?", max_length=255)
    answer_2 = forms.CharField(label="What is your favorite food?", max_length=255)
    answer_3 = forms.CharField(label="What is your favorite movie?", max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Save email to the user model
        if commit:
            user.save()
            # Save security answers to UserProfile
            UserProfile.objects.create(
                user=user,
                security_answer_1=self.cleaned_data['answer_1'],
                security_answer_2=self.cleaned_data['answer_2'],
                security_answer_3=self.cleaned_data['answer_3']
            )
        return user
