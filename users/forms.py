from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from .models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for fild_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    age = forms.CharField(widget=forms.NumberInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name','last_name', 'password1', 'password2', 'age')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите почту пользователя'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Введите подтверждение'
        self.fields['age'].widget.attrs['placeholder'] = 'Введите возраст'
        for fild_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserProfileForm(UserChangeForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'readonly': True}))
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    age = forms.CharField(widget=forms.NumberInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name','last_name', 'image', 'age')


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите почту пользователя'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['age'].widget.attrs['placeholder'] = 'Введите возраст'
        for fild_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


    # def clean_image(self):
    #     data = self.cleaned_data['image']
    #     if data.size > 1024:
    #         raise forms.ValidationError('Слишком большой размер файла!')
    #
    #     return data