from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'e.g., JohnDoe',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'e.g., johndoe@gmail.com',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    
    # Add a choice field for user type
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('inventory_manager', 'Inventory Manager'),
        ('admin', 'Admin'),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
    )

    # Override the save method to set the user type
    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data['user_type']

        if user_type == 'customer':
            user.is_customer = True
        elif user_type == 'inventory_manager':
            user.is_inventoryManager = True
        elif user_type == 'admin':
            user.is_admin = True

        if commit:
            user.save()

        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
        
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full py-3 px-4 rounded-xl mb-2'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'e.g., johndoe@gmail.com',
        'class': 'w-full py-3 px-6 rounded-xl mb-2'
    }))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone', 'image']

    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full py-3 px-4 rounded-xl mb-2'
    }))

    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'w-full py-3 px-6 rounded-xl mb-2'
    }))
    image = forms.ImageField(required=False)
