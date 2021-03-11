from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout


@login_required
def logout(request):
    logout(request)
    return redirect('/')
