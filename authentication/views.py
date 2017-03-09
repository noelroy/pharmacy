from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from authentication.forms import SignUpForm, SignUpFormDetailed, AddressForm

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'authentication/signup.html',
                          {'form': form})

        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/signupdetailed')

    else:
        return render(request, 'authentication/signup.html',
                      {'form': SignUpForm()})

@login_required()
def signupdetailed(request):
    if request.user.profile.type:
        return redirect('/')
    if request.method == 'POST' :
        form1 = SignUpFormDetailed(request.POST,instance=request.user.profile)
        form2 = AddressForm(request.POST)
        if not form1.is_valid():
            return render(request, 'authentication/signupdetailed.html',
                          {'form1': form1, 'form2': form2})
        if not form2.is_valid():
            return render(request, 'authentication/signupdetailed.html',
                          {'form1': form1, 'form': form2})
        new_profile = form1.save()
        new_address = form2.save(commit=False)
        new_address.profile = new_profile
        new_address.save()
        logout(request)
        return render(request, 'approve.html')
    return render(request, 'authentication/signupdetailed.html',
                  {'form1': SignUpFormDetailed(), 'form2': AddressForm()})