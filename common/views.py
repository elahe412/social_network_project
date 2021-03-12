from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from . import forms


# from common.forms import ProfileCreationForm
#
#
# class RegisterUser(CreateView):
#     form_class = ProfileCreationForm
#     success_url = 'main-post-view'
#     template_name = 'registration/signup.html'
#
# class LoginView(View):
#     def get(self, request):
#         return render(request, 'registration/login.html')
#
#     def post(self, request):
#         message = ''
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         is_logout = request.POST.get("logout")
#         if username and password:
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     message = 'Login was successful!'
#                     login(request, user)
#                     return redirect('posts:main-post-view')
#                 else:
#                     message = 'User is deactivated!'
#             else:
#                 message = 'Username or password was wrong!'
#         elif is_logout:
#             logout(request)
#             message = 'Logout successful'
#         return render(request, 'registration/login.html', {'message': message})
#
#
#
# @login_required()
# def logout_user(request):
#     logout(request)
#     return redirect('login')


# class SignupView(FormView):
#     """sign up user view"""
#     form_class = forms.SignupForm
#     template_name = 'registration/signup.html'
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         """ process user signup"""
#         user = form.save(commit=False)
#         user.save()
#         login(self.request, user)
#         if user is not None:
#             return HttpResponseRedirect(self.success_url)
#
#         return super().form_valid(form)
#
#
# @login_required()
# def logout(request):
#     """logout logged in user"""
#     logout(request)
#     return HttpResponseRedirect(reverse_lazy('home'))
#
#
# class LoginView(FormView):
#     """login view"""
#
#     form_class = forms.LoginForm
#     success_url = reverse_lazy('home')
#     template_name = 'registration/login.html'
#
#     def form_valid(self, form):
#         """ process user login"""
#         credentials = form.cleaned_data
#
#         user = authenticate(username=credentials['email'],
#                             password=credentials['password'])
#
#         if user is not None:
#             login(self.request, user)
#             return HttpResponseRedirect(self.success_url)
#
#         else:
#             messages.add_message(self.request, messages.INFO, 'Wrong credentials\
#                                 please try again')
#             return HttpResponseRedirect(reverse_lazy('login'))
