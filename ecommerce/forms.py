from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db import transaction

class CreateUserForm(UserCreationForm):
    class Meta :
        model = User
        fields = ['username','email','password1','password2']

    # @transaction.atomic
    # def data_save(self):
    #     user = super.save(commit = False)
    #     user.save()
    #     customer = Customer.objects.create(user=user)
    #     customer.save()
    #     return customer
