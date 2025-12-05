from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

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
@permission_required('catalogue.add_review', raise_exception=True)
def create(request):
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
@permission_required('catalogue.change_review', raise_exception=True)
def edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if not request.user == review.user: # Additional check to ensure user can only edit their own review
        messages.error(request, "Vous n'êtes pas autorisé à modifier cette critique.")
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
@permission_required('catalogue.delete_review', raise_exception=True)
def delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if not request.user == review.user: # Additional check to ensure user can only delete their own review
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette critique.")
        return redirect('catalogue:review-show', review.id)

    if request.method == 'POST':
        review.delete()
        messages.success(request, "Critique supprimée avec succès.")
        return redirect('catalogue:review-index')
    
    return redirect('catalogue:review-show', review.id)
