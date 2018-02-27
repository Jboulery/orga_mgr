from django import forms


class RegistrationForm(forms.Form):
    #Organization part
    orga_name = forms.CharField(max_length=200)
    orga_activity = forms.CharField(max_length=200)
    orga_address = forms.CharField(max_length=500)

    #User part
    user_firstname = forms.CharField(max_length=100)
    user_lastname = forms.CharField(max_length=100)
    user_email = forms.EmailField(max_length=100)
    user_password = forms.CharField(widget=forms.PasswordInput)
    user_confirmation_password = forms.CharField(widget=forms.PasswordInput)
    user_gender = forms.CharField(max_length=1)
    user_date_of_birth = forms.DateField()