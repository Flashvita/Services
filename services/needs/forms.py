from django import forms
from .models import Order, User, Requester, Executor, ResponseForOrder, MyOrders


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'Пользователь с логином {username} не найдет в системе')
        if not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)

    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтверждение пароля'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['email'].label = 'почта'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный email уже зарегестрирован')
        return email

    def clean_username(self):
        """Почта уже зарегестрирована"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Это имя уже используется')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'confirm_password', 'phone', 'first_name', 'last_name']


class NewOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'category', 'description', 'district', 'image', 'price', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Заказ'
        self.fields['description'].label = 'Описание заказа'
        self.fields['category'].label = 'Категория'
        self.fields['category'].empty_label = 'Выбирите категорию'
        self.fields['district'].label = 'Район заказа'
        self.fields['district'].empty_label = 'Выберите район'
        self.fields['image'].label = 'Фото'
        self.fields['price'].label = 'Примерная стоимость'


class UserEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'Почта'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ExecutorEditForm(forms.ModelForm):
    text = forms.CharField(max_length=255, label='О себе', widget=forms.Textarea, required=False)
    age = forms.CharField(max_length=2, label='Возраст', required=False, widget=forms.NumberInput)
    phone = forms.CharField(max_length=11, label='Номер телефона', required=False, widget=forms.NumberInput)
    time_work = forms.CharField(max_length=100, label='Время работы', required=False)
    days_of_work = forms.CharField(max_length=100, label='Дни работы', required=False)
    education = forms.CharField(max_length=100, label='Образование', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['certificates'].label = 'Сертификаты'
        self.fields['district'].empty_label = 'Выберети район'
        self.fields['district'].label = 'Район выполнения заказов'
        self.fields['category'].empty_label = 'Выберите категорию'
        self.fields['category'].label = 'Категория'


    class Meta:
        model = Executor
        fields = [
            'text', 'age', 'phone', 'district', 'category',
            'time_work', 'days_of_work', 'education', 'certificates'
        ]


class RequesterEditForm(forms.ModelForm):
    phone = forms.CharField(max_length=11, label='Номер телефона', required=False, widget=forms.NumberInput)
    age = forms.CharField(max_length=2, label='Возраст', required=False, widget=forms.NumberInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Requester
        fields = ['age', 'phone']


class ResponseForm(forms.ModelForm):
    text = forms.CharField(max_length=400, label='Напишите своё предложение клиенту', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ResponseForOrder
        fields = ['text']


class SearchOrderForm(forms.Form):
    query = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['query'].label = ''


class MyWorksForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Название заказа')
    description = forms.CharField(max_length=400, label='Описание выполненых работы', widget=forms.Textarea)
    image = forms.ImageField(label='Фото')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = MyOrders
        fields = ['name', 'description', 'image']
