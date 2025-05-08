from django.shortcuts import HttpResponse
from django.shortcuts import render
from purchaseoffer.models import Offer

# Create your views here.
def offer_list(request):
    offer = Offer.objects.all()
    return render(request, "purchaseoffer/purchaseoffers.html", {
        'offer': offer,
    })
#def finalized_offer_detail(request, offer_id):
    # finsih this
