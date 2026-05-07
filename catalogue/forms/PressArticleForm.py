from django import forms
from catalogue.models import PressArticle, Show
from tinymce.widgets import TinyMCE

class PressArticleForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    
    class Meta:
        model = PressArticle
        fields = ['show', 'title', 'summary', 'content']
        widgets = {
            'show': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de votre article'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Bref résumé captivant...'}),
        }
        labels = {
            'show': 'Spectacle concerné',
            'title': 'Titre de l\'article',
            'summary': 'Résumé / Chapô',
            'content': 'Contenu de l\'article',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On ne propose que les spectacles publiés ET ayant un producteur local
        self.fields['show'].queryset = Show.objects.filter(
            status='published', 
            producer__isnull=False
        ).order_by('title')
