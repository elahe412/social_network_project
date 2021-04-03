from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView

from apps.profiles.models import Profile
from registration.forms import ProfileCreationForm
from registration.tokens import account_activation_token


class SignupView(CreateView):
    """
    sign up user view
    """

    form_class = ProfileCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Deactivate account till it is confirmed,user cant login before confirmation
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('registration/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

        else:
            form = ProfileCreationForm
        return render(request, 'registration/signup.html', {'form': form})


class ActivateView(View):
    """
    check activation and if profile confirmed login user
    """

    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Profile.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('login')
        else:
            return HttpResponse('Activation link is invalid!')

@login_required()
def Logout(request):
    """logout logged in user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('posts:main-post-view')
        else:
            return render(request, 'registration/login.html')

    def post(self, request):
        message = ''
        username = request.POST.get("username")
        password = request.POST.get("password")
        is_logout = request.POST.get("logout")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    message = 'Login was successful!'
                    login(request, user)
                    return redirect('posts:main-post-view')
                else:
                    message = 'User is deactivated!'
            else:
                message = 'Username or password was wrong!'
        elif is_logout:
            logout(request)
            message = 'Logout successful'
        return render(request, 'registration/login.html', {'message': message})


@login_required()
def change_password(request):
    """
    user can change his/her password by PasswordChangeForm
    :param request
    :return: render of request, change_password.html and form
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })
