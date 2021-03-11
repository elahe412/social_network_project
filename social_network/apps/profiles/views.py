from django.shortcuts import render

# Create your views here.
from apps.profiles.forms import ProfileModelForm
from apps.profiles.models import Profile


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
