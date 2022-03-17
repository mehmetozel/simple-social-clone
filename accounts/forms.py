from django.contrib.auth import get_user_model  #returns the user model that's currently active in this project
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()  #this method gets the current model of who is accessing that website. This method will return the currently active user model

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Display Name'  #form doldururken aslında username'i doldururken sadece görsel olarak yazan Display Name olacak
        self.fields['email'].label = 'Email Address'
