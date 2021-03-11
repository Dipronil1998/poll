from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, min_length=5,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=50, min_length=5,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', max_length=50, min_length=8,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',
                                max_length=50, min_length=8,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class EditProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','date_joined','last_login']
        labels={'email':'Email'}
        '''
        def __init__(self, *args, **kwargs): 
            super(EditProfileForm, self).__init__(*args, **kwargs)                       
            self.fields['username'].disabled = True
        ''' 
'''
        def __init__(self,*args,**kwargs):
            super(EditProfileForm,self).__init__(*args, **kwargs)
            self.fields['username'].disabled = True
            #self.fields['username'].required = False
            #self.fields['username'].widget.attrs['disabled'] = "disabled"
            # self.fields['username'].widget.attrs['readonly'] = "readonly" 
'''     

class EditAdminProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        #fields= '__all__'
        #exclude={'groups','user_permissions'}
        fields=['username','first_name','last_name','email','date_joined','last_login','is_active','is_staff','is_superuser']
        labels={'email':'Email'}
    
        