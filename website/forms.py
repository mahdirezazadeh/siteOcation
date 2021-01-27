import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User


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


class Join(forms.Form):
    username = forms.CharField(max_length=150,
                               help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                               error_messages={
                                   'unique': _("A user with that username already exists."),
                               },
                               validators=[User.username_validator, ],
                               required=True,
                               )

    email = forms.EmailField(max_length=150, required=True, )
    name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    password = forms.PasswordInput()

    def check_username(self):
        u_name = self.cleaned_data['username']
        u_names = User.objects.get(username=u_name)

        # Check for username minimum length
        if len(u_name) < 4:
            raise ValidationError(_('Username must be more than 3 character!'))

        # Check for username maximum length
        if len(u_name) > 150:
            raise ValidationError(_('Username can not be more than 150 character!'))

        # Check for username being unique
        if u_names is not None:
            raise ValidationError(_('A user with that username already exists.'))

        # return valid username
        return u_name
