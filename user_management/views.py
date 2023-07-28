from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'user_management/register.html', {'user_form': user_form, 'profile_form': profile_form})