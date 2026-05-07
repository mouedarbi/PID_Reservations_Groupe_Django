from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from catalogue.models import UserMeta
from django.db import models


class UserUpdateForm(UserChangeForm):
    class Language(models.TextChoices):
        NONE = "", _("Choisissez votre langue")
        FRENCH = "fr", _("Français")
        ENGLISH = "en", _("English")
        DUTCH = "nl", _("Nederlands")

    # Définir les types de champs
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    email = forms.EmailField()
    password = None

    # Ajout des champs de données personnelles supplémentaires
    langue = forms.ChoiceField(choices=Language)

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _('Login')
        self.fields['first_name'].label = _('Prénom')
        self.fields['last_name'].label = _('Nom')

        self.fields['username'].help_text = None

        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            if field_name != 'password': # Password field is not displayed for update
                field.widget.attrs['style'] = 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;'

        # Récupérer les metadonnées de l'utilisateur
        user = kwargs.get('instance')
        if user and hasattr(user, 'usermeta'):
            self.initial['langue'] = user.usermeta.langue

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'langue',
        ]

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.save()

        if self.cleaned_data['langue']:
            user_meta = UserMeta.objects.get(user_id=user.id)
            user_meta.langue = self.cleaned_data['langue']
            user_meta.save()
        return user
