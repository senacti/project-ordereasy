from django import forms
from django.contrib.auth.models import User
from OrderEasy_app.models import Cliente

class ClienteUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirma la contraseña')
    direccion = forms.CharField(max_length=255, label='Dirección', required=True)
    telefono = forms.CharField(max_length=20, label='Teléfono', required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            Cliente.objects.create(
                user=user,
                direccion=self.cleaned_data.get('direccion'),
                telefono=self.cleaned_data.get('telefono')
            )
        return user
