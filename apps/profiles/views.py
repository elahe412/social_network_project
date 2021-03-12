from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render


from apps.profiles.forms import ProfileModelForm
from apps.profiles.models import Profile


@login_required
def index(request):
    return render(request,'accounts/index.html')

def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return render(request,'index.html')
    context['form']=form
    return render(request,'registration/signup.html',context)

def edit_my_profile_view(request):
    obj = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=obj)
    confirm = False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {'obj': obj, 'form': form, 'confirm': confirm}
    return render(request, 'profiles/myprofile.html', context)
