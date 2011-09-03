from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class LoginForm(AuthenticationForm):
    keep_signed_in = forms.BooleanField(label=_(u'Keep me signed in'), help_text=_(u'Do not enable this if you are on a public or shared computer.'), required=False)

class UserAccountForm(forms.ModelForm):
    '''
    Used in account details editing.

    ``ModelForm`` Auto-generated Fields:

    * ``fields = ('email', 'first_name', 'last_name',)``

    '''
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user != self.instance:
                raise forms.ValidationError(u'An account with that email address already exists.')
        except User.DoesNotExist:
            pass
        return email

    def save(self, commit=True):
        instance = super(UserAccountForm, self).save(commit)

        return instance

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)
