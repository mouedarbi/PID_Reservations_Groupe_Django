from django import forms
from catalogue.models import PressArticle, Show

class PressArticleForm(forms.ModelForm):
    class Meta:
        model = PressArticle
        fields = ['show', 'title', 'summary', 'content']
        widgets = {
            'show': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de votre article'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Bref résumé captivant...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Rédigez votre critique ici...'}),
        }
        labels = {
            'show': 'Spectacle concerné',
            'title': 'Titre de l\'article',
            'summary': 'Résumé / Chapô',
            'content': 'Contenu de l\'article',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On ne propose que les spectacles publiés (ou tous ?)
        # L'utilisateur demande des articles sur les spectacles
        self.fields['show'].queryset = Show.objects.filter(status='published').order_by('title')
