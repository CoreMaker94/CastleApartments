from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.shortcuts import render
from property.models import Property

from purchaseoffer.forms.purchase_offer_form import PurchaseOfferForm
from purchaseoffer.models import Offer, Status
from user.models import Profile


# Create your views here.
@login_required
def make_offer(request, id):
    # For posting new purchase offer
    if request.method == "POST":
        form = PurchaseOfferForm(request.POST)
        prop = get_object_or_404(Property, id=id)
        buyer = request.user

        # Check user type is not a seller (sellers can't buy)

        # Verify that buyer != seller
        if prop.seller.id == buyer.id:
            form.add_error(None, "You can't make a purchase offer")
            return render(request, "property/single_property.html", {"form": form, "property": prop})

        # Verify that there is not another pending/accepted/contingent offer
        existing_offer = Offer.objects.filter(property=prop, buyer=buyer).first()
        if existing_offer:
            if existing_offer.status.name != "Rejected": # TODO if we add expired have an OR clause
                form.add_error(None, f"You already have purchase offer that is {existing_offer.status.name}")
                return render(request, "property/single_property.html", {"form": form, "property": prop})

        # Check that expiration date is in the future
        if form.is_valid():
            expires_at = form.cleaned_data["expires_at"]
            if expires_at <= date.today():
                form.add_error("expires_at", "Expiration date must be in the future")
                return render(request, "property/single_property.html", {"form": form, "property": prop})
        # Check that offer amount is integer, not negative
        offer = form.save(commit=False)
        offer.property = prop
        offer.buyer = buyer
        offer.expires_at = expires_at
        offer.status_id = 1
        offer.save()

        return redirect("property_by_id", id=id)
    # For get, display form
    else:
        form = PurchaseOfferForm()

    prop = get_object_or_404(Property, id=id)
    return render(request, "property/single_property.html", {"form": form, "property": prop})

@login_required
def get_offers(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)

    rejected_status = Status.objects.get(name="Rejected")

    if profile.type.name == "Buyer":
        offers = Offer.objects.filter(buyer=user)
    else:
        offers = Offer.objects.filter(property__seller=user)

    # Expire all pending offers
    expired_pending_offers = offers.filter(status__name="Pending", expires_at__lte=date.today())
    expired_pending_offers.update(status=rejected_status)

    offers_data = []

    for offer in offers.select_related("property", "status", "property__seller__profile"):
        offers_data.append({
            "id": offer.id,
            "price": offer.offer,
            "status": offer.status.name,
            "created_at": offer.created_at,
            "expires_at": offer.expires_at,
            "property": {
                "id": offer.property.id,
                "address": offer.property.address
            },
            "seller": {
                "name": offer.property.seller.profile.name
            },
            "finalize_url": f"/offers/{offer.id}/finalize/" # TODO fix this url
        })

    return render(request, 'purchaseoffer/purchaseoffers.html', {"offers": offers_data})