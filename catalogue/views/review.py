from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

from catalogue.models import Review
from catalogue.forms.ReviewForm import ReviewForm

def index(request):
    reviews = Review.objects.all()
    title = 'Liste des critiques'
    return render(request, 'review/index.html', {'reviews': reviews, 'title': title})

def show(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        raise Http404('Critique inexistante')
    
    title = 'Fiche d\'une critique'
    return render(request, 'review/show.html', {'review': review, 'title': title})

@login_required
def create(request):
    if not request.user.has_perm('catalogue.add_review'):
        messages.error(request, "Vous n'avez pas la permission de créer une critique.")
        return redirect('catalogue:review-index')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.validated = False  # Or based on some logic
            review.save()
            messages.success(request, "Critique créée avec succès.")
            return redirect('catalogue:review-show', review.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ReviewForm()

    return render(request, 'review/create.html', {'form': form})

@login_required
def edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if not request.user.has_perm('catalogue.change_review') and request.user != review.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cette critique.")
        return redirect('catalogue:review-show', review.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Critique modifiée avec succès.")
            return redirect('catalogue:review-show', review.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ReviewForm(instance=review)

    return render(request, 'review/edit.html', {'form': form, 'review': review})

@login_required
def delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if not request.user.has_perm('catalogue.delete_review') and request.user != review.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette critique.")
        return redirect('catalogue:review-show', review.id)

    if request.method == 'POST':
        review.delete()
        messages.success(request, "Critique supprimée avec succès.")
        return redirect('catalogue:review-index')
    
    # It's good practice to have a confirmation page, 
    # but for simplicity, we'll redirect from show view with a POST request.
    # This part of the view will not be reached if the deletion is initiated from a form.
    return redirect('catalogue:review-show', review.id)
