from django.http import JsonResponse
from django.shortcuts import render
from property.models import Property
from purchaseoffer.forms.purchase_offer_form import PurchaseOfferForm
from zipcode.models import ZipCode
from property.models import Type
from django.db.models import Q
from purchaseoffer.models import Offer
from purchaseoffer.forms import purchase_offer_form


def property_list(request):
    if 'search_filter' in request.GET:
        properties = Property.objects.all()

        # Address search
        search_query = request.GET.get('search_filter', '').strip()
        if search_query:
            properties = properties.filter(address__icontains=search_query)

        # Zip code filter
        zipcode = request.GET.get('zipcode')
        if zipcode:
            properties = properties.filter(zipcode__code=zipcode)

        # Property type filter
        property_type = request.GET.get('property_type')
        if property_type:
            properties = properties.filter(type__name=property_type)

        # Price sorting
        price_order = request.GET.get('price_order')
        if price_order == 'low':
            properties = properties.order_by('price')
        elif price_order == 'high':
            properties = properties.order_by('-price')

        return JsonResponse({
            'data': [
                {
                    'id': x.id,
                    'address': x.address,
                    'price': x.price,
                    'type': x.type.name,
                    'zipcode': x.zipcode.code,
                    'image': x.images.first().image.url if x.images.first() else ""
                } for x in properties
            ]
        })

    # For page load
    properties = Property.objects.all()
    zipcodes = Property.objects.values_list('zipcode__code', flat=True).distinct()
    property_types = Property.objects.select_related('type').values_list('type__name', flat=True).distinct()

    return render(request, "property/properties.html", {
        "properties": properties,
        "zipcodes": zipcodes,
        "property_types": property_types,
    })

# view home
def home(request):
    recent = Property.objects.order_by('-list_date')[:4]
    return render(request, 'home.html', {
        "featured": recent[0] if recent else None,
        "popular": recent[1:] if len(recent) > 1 else []
    })


# View to display a single property by its ID
def property_by_id(request, id):
    offer = None
    if request.user.is_authenticated:
        offer = Offer.objects.filter(property_id=id, buyer_id = request.user.id).first()
    property = Property.objects.get(id=id)
    other_properties = Property.objects.exclude(id=id)[:6]
    form = PurchaseOfferForm(instance=offer)
    return render(request, "property/single_property.html", {
        "property": property,
        "other_properties": other_properties,
        "offer": offer,
        "form" : form,
    })
