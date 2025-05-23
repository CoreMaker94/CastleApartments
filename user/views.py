from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from purchaseoffer.models import Offer
from property.models import Property, PropertyImage
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

# Own profile view, with offers
def profile(request):
    user_profile = (
        Profile.objects
        .select_related('type', 'zipcode__city')
        .only(
            'name',
            'image',
            'bio',
            'type__name',
            'zipcode__code',
            'zipcode__city__name',
            'user'
        )
        .get(user=request.user)
    )

    if request.method == "POST":
        form_class = BuyerProfileForm if user_profile.type.id == 1 else SellerProfileForm
        form = form_class(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully updated!")
            return redirect('profile')

        else:
            messages.error(request, "There was a problem updating your profile. Please check the form.")

    # Sending the form for get request
    else:
        form_class = BuyerProfileForm if user_profile.type.id == 1 else SellerProfileForm
        form = form_class(instance=user_profile)

    return render(request, 'user/profile.html', {
        'form': form,
        'profile': user_profile,
    })

def get_profile_by_id(request, id):
    profile = (
        Profile.objects
        .select_related('type', 'zipcode__city', 'user')
        .get(user_id=id)
    )

    # Prevent public viewing of buyer profiles
    if profile.type_id == 1 and request.user.id == profile.user.id:
        # Buyer is trying to view own profile, redirect to profile
        return redirect('profile')

    elif profile.type_id == 1 and request.user.id != profile.user.id:
        # Another user trying to access Buyer profile that is not theirs
        raise Http404

    main_image_subquery = PropertyImage.objects.filter(
        property=OuterRef('pk'),
        is_main=True
    ).values('image')[:1]

    # Fallback: any image
    fallback_image_subquery = PropertyImage.objects.filter(
        property=OuterRef('pk')
    ).values('image')[:1]

    # Annotated queryset with fallback logic
    properties = Property.objects.filter(seller_id=id).annotate(
        main_image=Coalesce(
            Subquery(main_image_subquery),
            Subquery(fallback_image_subquery)
        )
    ).values('id', 'address', 'main_image', 'price')
    return render(request, 'user/profile.html', {
        'profile': profile,
        'properties': properties,
        'MEDIA_URL': settings.MEDIA_URL,
    })
