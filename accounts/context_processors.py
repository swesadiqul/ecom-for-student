from .forms import *
from django.shortcuts import redirect
from django.contrib import messages
from store.models import SiteLogo

def subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for subscribing to us.')
            return redirect('home')
    else:
        form = NewsletterForm()

    return {'subscribe': form}



def socialAccount(request):
    return {'social_media': SocialAccount.objects.all()}

def contactInfo(request):
    return {'info': ContactInformation.objects.first()}


def siteLogo(request):
    return {'siteLogo': SiteLogo.objects.last()}