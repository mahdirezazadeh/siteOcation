import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import Profile
from .models import Comment
from .models import Website


class RenewLogin(forms.Form):
    renew_date = forms.DateField(help_text='Enter a date between now and 4 weeks (default 3).', )

    # input_formats = 'YYYY-MM-DD'

    def clean_renewal_date(self):
        data = self.cleaned_data['renew_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # return the cleaned data.
        return data


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(max_length=50, required=False, )
    date_of_birth = forms.DateField(required=False, )
    user_picture = forms.ImageField(required=False, )

    class Meta:
        model = Profile
        fields = ('bio', 'date_of_birth', 'user_picture', )


class AddComment(forms.ModelForm):
    comment = forms.CharField(max_length=600)

    class Meta:
        model = Comment
        fields = ('comment', )


class AddWebsite(forms.ModelForm):
    description = forms.CharField(max_length=1000)
    founded = forms.DateField(help_text='Enter a date that the website have been created.', )

    class Meta:
        model = Website
        fields = ('website_domain_name', 'name', 'description', 'founded', 'numberOfEmployees', 'description')


class UserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ('username', 'email', 'first_name', 'last_name')


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()

    def clean(self):
        if 'new_password1' in self.cleaned_data and 'new_password2' in self.cleaned_data:
            if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
# class Join(forms.ModelForm):
#
#     class Meta:
#         model =
#         field

