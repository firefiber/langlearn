from django.shortcuts import render, redirect
from .forms import NewUserForm

def register(request):
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'user_management/register.html', {'user_form': user_form, 'profile_form': profile_form})