from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.shortcuts import render
from property.models import Property

from purchaseoffer.forms.purchase_offer_form import PurchaseOfferForm
from purchaseoffer.models import Offer
from django.contrib import messages

# Create your views here.
@login_required
def make_offer(request, id):
    # For posting new purchase offer
    if request.method == "POST":
        form = PurchaseOfferForm(request.POST)
        prop = get_object_or_404(Property, id=id)
        buyer = request.user

        # Verify that buyer != seller
        if prop.seller.id == buyer.id:
            form.add_error(None, "You can't make a purchase offer")
            messages.error(request, "There was an issue with your offer.")
            return render(request, "property/single_property.html", {"form": form, "property": prop})

        # Verify that there is not another pending/accepted/contingent offer
        existing_offer = Offer.objects.filter(property=prop, buyer=buyer).first()
        if existing_offer:
            if existing_offer.status.name != "Rejected": # TODO if we add expired have an OR clause
                form.add_error(None, f"You already have purchase offer that is {existing_offer.status.name}")
                messages.error(request, "There was an issue with your offer.")
                return render(request, "property/single_property.html", {"form": form, "property": prop})

        # Check that expiration date is in the future
        if form.is_valid():
            expires_at = form.cleaned_data["expires_at"]
            if expires_at <= date.today():
                form.add_error("expires_at", "Expiration date must be in the future")
                messages.error(request, "There was an issue with your offer.")
                return render(request, "property/single_property.html", {"form": form, "property": prop})
        # Check that offer amount is integer, not negative
        offer = form.save(commit=False)
        offer.property = prop
        offer.buyer = buyer
        offer.expires_at = expires_at
        offer.status_id = 1
        offer.save()
        messages.success(request, "Your purchase offer was submitted successfully!")
        return redirect("property_by_id", id=id)
    # For get, display form
    else:
        form = PurchaseOfferForm()
        messages.error(request, "There was an issue with your offer.")

    prop = get_object_or_404(Property, id=id)
    return render(request, "property/single_property.html", {"form": form, "property": prop})