from django import forms
from django.contrib.auth.models import User, Group, Permission
from catalogue.models.user_meta import UserMeta

class AdminUserUpdateForm(forms.ModelForm):
    langue = forms.CharField(max_length=2, required=False, label="Langue (ex: fr, en)")

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 
            'is_active', 'is_staff', 'is_superuser', 
            'groups', 'user_permissions'
        ]
        labels = {
            'username': 'Identifiant',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse e-mail',
            'is_active': 'Actif (Peut se connecter)',
            'is_staff': 'Statut équipe (Accès administration)',
            'is_superuser': 'Statut super-utilisateur (Tous les droits)',
            'groups': 'Groupes',
            'user_permissions': 'Permissions spécifiques',
        }
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
            'user_permissions': forms.SelectMultiple(attrs={'size': '15'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            try:
                user_meta = UserMeta.objects.get(user=self.instance)
                self.fields['langue'].initial = user_meta.langue
            except UserMeta.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.save_m2m()
            # Save UserMeta (Language)
            langue = self.cleaned_data.get('langue')
            if langue:
                user_meta, created = UserMeta.objects.get_or_create(user=user)
                user_meta.langue = langue
                user_meta.save()
        return user
