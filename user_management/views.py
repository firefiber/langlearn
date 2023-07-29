from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import NewUserForm

# def register(request):
#     if request.method == 'POST':
#         user_form = NewUserForm(request.POST)
#
#         if user_form.is_valid():
#             user = user_form.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#             return redirect('login')
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     return render(request, 'user_management/register.html', {'user_form': user_form, 'profile_form': profile_form})

class RegisterView(FormView):
    template_name = 'user_management/register.html'
    form_class = NewUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

