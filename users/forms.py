from .models import User
from django import forms
from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)  # ✅ fix authenticate to use 'email'
            if user is None:
                raise forms.ValidationError("Invalid email or password")
            if not user.is_active:
                raise forms.ValidationError("User is inactive")
            self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user

class UserSignupForm(forms.ModelForm):
    password = forms.ChartField(widget=forms.PasswordInput)
    password_confirm = forms.ChartField(widget=forms.PasswordInput)
    Role_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    role = forms.ChoiceField(choices=Role_CHOICES)
    class Meta:
        model = User
        fields = ["email", "name","password", "password_confirm", "role"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passoword do not match")
        return cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password'])
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user



class TeacherSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'teacher'  # ✅ set role instead of is_teacher
        if commit:
            user.save()
        return user


class StudentSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'student'  # ✅ set role instead of is_student
        if commit:
            user.save()
        return user


class AdminSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'admin'  # ✅ set role instead of is_admin
        if commit:
            user.save()
        return user
