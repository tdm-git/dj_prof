from django import forms
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from products.models import ProductsCategory, Products


class UserAdminRegisterForm(UserRegisterForm):

    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'first_name','last_name', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': False}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': False}))


class CategoryAdminForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Наименование'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Описание'}))

    class Meta:
        model = ProductsCategory
        fields = ('name', 'description')


class ProductsAdminForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Наименование'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Описание'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control py-4', 'placeholder': 'Цена'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control py-4', 'placeholder': 'Количество'}))

    category = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Категория товара'}),
                                      queryset=ProductsCategory.objects.all())
    # category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Категория товара'}))
    # category = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Категория товара'}),
    #                               label='pk', choices=ProductsCategory.objects.values_list('pk','name'))

    class Meta:
        model = Products
        fields = ('name', 'image', 'description', 'price', 'quantity', 'category')

    # def __init__(self, *args, **kwargs):
    #     super(ProductsAdminForm, self).__init__(*args, **kwargs)
    #     self.fields['category'].choices = ProductsCategory.objects.values_list('id','name')

