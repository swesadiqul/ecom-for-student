from django.shortcuts import render
from .models import *

# Create your views here.
def privacy_policy(request):
    privacy_policy = PrivacyPolicy.objects.first()
    context = {
        'privacy_policy': privacy_policy
    }
    return render(request, 'store/privacy-policy.html', context)