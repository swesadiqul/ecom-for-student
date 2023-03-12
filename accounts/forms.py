from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.core.validators import validate_email
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget




class UserRegistrationForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, 
    #                              required=True, 
    #                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    #                              )
    # last_name = forms.CharField(max_length=30, 
    #                             required=True, 
    #                             widget=forms.TextInput(attrs={'class': 'form-control'})
    #                             )
    # email = forms.EmailField(max_length=254, 
    #                          required=True, 
    #                          widget=forms.EmailInput(attrs={'class': 'form-control'})
    #                          )
    # newsletter = forms.BooleanField(required=False, label='Sign Up for Newsletter',
    #                                 widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    #                                 )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'sign_up_for_newsletter',  'password1', 'password2')
        # widgets = {
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ['user']




#today
class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        validators=[validate_email],
        widget=forms.EmailInput(attrs={
            'class': 'input-group__field newsletter__input',
            'placeholder': 'E-mail address'
        })
    )

    class Meta:
        model = Newsletter
        fields = ('email',)