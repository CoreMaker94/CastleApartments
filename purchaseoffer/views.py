from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.shortcuts import render
from django.views.decorators.http import require_POST

from property.models import Property

from purchaseoffer.forms.purchase_offer_form import PurchaseOfferForm

from purchaseoffer.models import Offer, Status
from user.models import Profile
from django.contrib import messages
from django.utils.timezone import now
from purchaseoffer.models import Finalize, PaymentMethod



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
        is_buyer = True
    else:
        offers = Offer.objects.filter(property__seller=user)
        is_buyer = False

    # Expire all pending offers
    expired_pending_offers = offers.filter(status__name="Pending", expires_at__lte=date.today())
    expired_pending_offers.update(status=rejected_status)

    offers_data = []

    for offer in offers.select_related("property", "status", "property__seller__profile"):
        offers_data.append({
            "id": offer.id,
            "offer": offer.offer,
            "status": offer.status.name,
            "created_at": offer.created_at,
            "expires_at": offer.expires_at,
            "property": {
                "id": offer.property.id,
                "address": offer.property.address
            },
            "seller": {
                "name": offer.property.seller.profile.name,
                "id" : offer.property.seller.id
            },
            "is_finalized": Finalize.objects.filter(offer=offer).exists(),
            "finalize_url": f"/offer/{offer.id}/finalize/"
        })

    return render(request, 'purchaseoffer/purchaseoffers.html', {
        "offers": offers_data,
        "is_buyer": is_buyer
    })

@require_POST
@login_required
def change_status_seller(request, id):
    offer = get_object_or_404(Offer, id=id)

    # Check if user is seller of offer
    if offer.property.seller != request.user:
        messages.error(request, "You can't change your offer's seller status.")
        return redirect("get-offers")

    # Check if offer is pending and not expired
    if offer.status.name != "Pending":
        messages.warning(request, "You can only change pending offers.")
        return redirect("get-offers")

    if offer.expires_at and offer.expires_at < date.today():
        messages.warning(request, "Offer has expired and cannot be changed.")
        return redirect("get-offers")

    # Get new status from POST (e.g., "Accepted" or "Rejected")
    new_status_name = request.POST.get("status")
    if new_status_name not in ["Accepted", "Rejected"]:
        messages.error(request, "Invalid status.")
        return redirect("get-offers")

    # Update the status
    new_status = Status.objects.get(name=new_status_name)
    offer.status = new_status
    offer.save()

    messages.success(request, f"Offer has been {new_status_name.lower()}.")
    return redirect("get-offers")

@login_required
def finalize_offer(request, id):
    offer = get_object_or_404(Offer, id=id)

    if offer.buyer != request.user:
        messages.error(request, "You are not authorized to finalize this offer.")
        return redirect("get_offers")

    step = request.GET.get("step", "contact")
    if request.method == "POST":
        step = request.POST.get("step", step)

    session_key = f"finalize_offer_{offer.id}"
    stored_data = request.session.get(session_key, {})

    if request.method == "POST":
        if step == "contact":
            stored_data["name"] = request.POST.get("name", "")
            stored_data["email"] = request.POST.get("email", "")
            stored_data["phone"] = request.POST.get("phone", "")
            request.session[session_key] = stored_data
            return redirect(f"{request.path}?step=payment")

        elif step == "payment":
            stored_data["payment_method"] = request.POST.get("payment_method", "")
            if stored_data["payment_method"] == "card":
                stored_data["card_number"] = request.POST.get("card_number", "")
                stored_data["exp_date"] = request.POST.get("exp_date", "")
                stored_data["cvv"] = request.POST.get("cvv", "")
            elif stored_data["payment_method"] == "loan":
                stored_data["loan_bank"] = request.POST.get("loan_bank", "")
                stored_data["loan_ref"] = request.POST.get("loan_ref", "")
            request.session[session_key] = stored_data
            return redirect(f"{request.path}?step=review")

        elif step == "review":
            request.session[session_key] = stored_data
            return redirect(f"{request.path}?step=confirm")

        elif step == "confirm":
            if not Finalize.objects.filter(offer=offer).exists():
                try:
                    # Map internal form values to DB values
                    payment_map = {
                        "card": "Credit Card",
                        "loan": "Loan"
                    }

                    payment_key = stored_data.get("payment_method")
                    payment_name = payment_map.get(payment_key)

                    if not payment_name:
                        messages.error(request, "Invalid payment method.")
                        return redirect("get-offers")

                    try:
                        method = PaymentMethod.objects.get(name=payment_name)
                    except PaymentMethod.DoesNotExist:
                        messages.error(request, "Selected payment method is not available.")
                        return redirect("get-offers")

                except PaymentMethod.DoesNotExist:
                    messages.error(request, "Invalid payment method.")
                    return redirect("get-offers")

                Finalize.objects.create(
                    offer=offer,
                    buyer_address="placeholder address",
                    buyer_zipcode="101",
                    buyer_country="Iceland",
                    buyer_city="Reykjavík",
                    pay_method=method
                )

                finalized_status = Status.objects.get(name="Finalized")
                offer.status = finalized_status
                offer.save()

            request.session.pop(session_key, None)
            step = "confirm"  #  Tell the template to show the confirmation step

    return render(request, "purchaseoffer/finalize_offer.html", {
        "offer": offer,
        "step": step,
        "form_data": stored_data,
    })
