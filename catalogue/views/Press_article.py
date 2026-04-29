@login_required
def my_articles(request):
    if not request.user.groups.filter(name='PRESS_CRITIC').exists():
        messages.error(request, "Accès réservé aux critiques de presse.")
        return redirect('catalogue:show-index')

    articles = PressArticle.objects.filter(author=request.user).order_by('-created_at')
    # On pointe vers le nouveau dossier 'press'
    return render(request, 'press/my_articles.html', {'articles': articles})

@login_required
def create_article(request):
    if request.method == 'POST':
        form = PressArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.status = None 
            article.save()
            messages.success(request, "Article soumis avec succès !")
            return redirect('catalogue:my-articles')
    else:
        form = PressArticleForm()
    
    return render(request, 'press/create.html', {'form': form})

@login_required
def producer_dashboard(request):
    # Sécurité : Seul le groupe PRODUCER ou les admins
    if not (request.user.groups.filter(name='PRODUCER').exists() or request.user.is_superuser):
        messages.error(request, "Accès réservé aux producteurs.")
        return redirect('catalogue:show-index')

    articles = PressArticle.objects.all().order_by('-created_at')
    return render(request, 'press_article/producer_dashboard.html', {'articles': articles})

@login_required
def validate_article(request, article_id, action):
    article = get_object_or_404(PressArticle, id=article_id)
    
    if action == 'approve':
        article.status = True
        messages.success(request, f"L'article '{article.title}' a été approuvé.")
    elif action == 'reject':
        article.status = False
        messages.error(request, f"L'article '{article.title}' a été rejeté.")
    
    article.save()
    return redirect('catalogue:producer-dashboard')