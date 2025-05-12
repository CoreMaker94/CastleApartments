from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from purchaseoffer.models import Offer
from property.models import Property
from user.forms.profile_form import BuyerProfileForm, SellerProfileForm, CustomUserCreationForm
from user.models import Profile
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        #TODO give error message when registration fails
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'user/register.html', {
                'form': form
            })

    else:
        return render(request, "user/register.html", {
            'form': CustomUserCreationForm(),
        })

# Own profile view
def profile(request):
    # Get their profile or create an empty one if they lack a profile
    user_profile = Profile.objects.get(user=request.user)
    # For updating a profile
    if request.method == "POST":
        if user_profile.type.id == 1:
            form = BuyerProfileForm(request.POST, request.FILES, instance=user_profile)
        else:
            form = SellerProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Profile successfully updated!")
            return redirect('profile')
        else:
            messages.error(request, "There was a problem updating your profile. Please check the form.")

    # Sending the form for get request
    if user_profile.type.id == 1:
        form = BuyerProfileForm(instance=user_profile)
    else:
        form = SellerProfileForm(instance=user_profile)
    return render(request, 'user/profile.html', {
        'form' : form,
        'profile' : user_profile,
    })

# TODO Fix visit view
# TODO "should" not allow viewing buyers, unless difficult to implement
# User visitation view
def get_profile_by_id(request, id):
    profile = Profile.objects.get(user_id=id) # TODO fix this, maybe has to be id=id
    # If buyer
    if profile.type_id == 1: # TODO check if this still works after changes
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