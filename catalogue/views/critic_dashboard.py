from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from catalogue.models import PressArticle, Show
from catalogue.forms.PressArticleForm import PressArticleForm

def is_critic(user):
    return user.is_authenticated and (user.groups.filter(name='PRESS_CRITIC').exists() or user.is_superuser)

@login_required
@user_passes_test(is_critic)
def critic_dashboard(request):
    """
    Espace dédié aux critiques de presse pour gérer leurs articles.
    """
    articles = PressArticle.objects.filter(user=request.user).select_related('show').order_by('-created_at')
    
    context = {
        'page_title': 'Mes Articles de Presse',
        'articles': articles,
    }
    return render(request, 'user/press_articles.html', context)

@login_required
@user_passes_test(is_critic)
def submit_press_article(request, pk=None):
    """
    Vue pour soumettre ou modifier un article de presse.
    """
    article = None
    if pk:
        article = get_object_or_404(PressArticle, pk=pk, user=request.user)
        
    if request.method == 'POST':
        form = PressArticleForm(request.POST, instance=article)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.user = request.user
            new_article.validated = False # Re-validation required on edit
            new_article.save()
            
            messages.success(request, "Votre article a été enregistré et est en attente de validation par le producteur du spectacle.")
            return redirect('catalogue:critic_dashboard')
    else:
        form = PressArticleForm(instance=article)
        
    context = {
        'page_title': 'Rédiger un Article' if not pk else 'Modifier l\'Article',
        'form': form,
        'is_edit': pk is not None
    }
    return render(request, 'user/submit_press_article.html', context)
