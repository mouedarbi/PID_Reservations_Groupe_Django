from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserSignUpForm

class UserSignUpView(UserPassesTestMixin, CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def test_func(self):
        return self.request.user.is_anonymous or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Vous êtes déjà inscrit!")
        return redirect('home')

@login_required
def profile(request):
    languages = {
        "fr": "Français",
        "en": "English",
        "nl": "Nederlands",
    }

    return render(request, 'user/profile.html', {
        "user_language" : languages[request.user.usermeta.langue],
    })
