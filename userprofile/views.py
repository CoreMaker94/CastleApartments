from django.shortcuts import render

import purchaseoffer
from userprofile.models import UserProfile
from purchaseoffer.models import Offer
from property.models import Property

# Create your views here.
# In the future will be used to only see your own profile, we'll see
def profile(request):
    profile = UserProfile.objects.get(id=1)
    return render(request, 'profile/profile.html', {
        "profile": profile,
    })

# Probably will be used for visitor view, and only for viewing other sellers?
def get_profile_by_id(request, id):
    profile = UserProfile.objects.get(id=id)
    # If buyer
    if profile.type_id == 1:
        purchaseoffers = Offer.objects.filter(buyer_id=id)
        return render(request, 'profile/profile.html', {
            'profile': profile,
            'purchaseoffers': purchaseoffers
        })
    # If seller
    else:
        properties = Property.objects.filter(seller_id=id)
        return render(request, 'profile/profile.html', {
            'profile': profile,
            'properties': properties
        })