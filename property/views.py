from collections import defaultdict

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
    # Check if there are any search params
    if request.GET:
        properties = Property.objects.all()

        # Address search
        search_query = request.GET.get('address_name', '').strip()
        if search_query:
            properties = properties.filter(address__icontains=search_query)

        # Zip code filter
        zip_filter = request.GET.get('zip_filter')
        print(zip_filter)
        if zip_filter:
            zipcodes_ids = zip_filter.split(',')
            print(zipcodes_ids)
            properties = properties.filter(zipcode__id__in=zipcodes_ids)

        # Property type filter
        type_filter = request.GET.get('type_filter')
        if type_filter:
            print("Type Filter Query:", type_filter)
            property_types_ids = type_filter.split(",")
            properties = properties.filter(type__id__in=property_types_ids)

        # Price sorting - Should be orderby and check name also
        order_by = request.GET.get('order_by')
        if order_by:
            if order_by == 'p-asc':
                properties = properties.order_by('-price')
            elif order_by == 'p-desc':
                properties = properties.order_by('price')
            elif order_by == 'n-asc':
                properties = properties.order_by('name')
            elif order_by == 'n-desc':
                properties = properties.order_by('-name')

        return JsonResponse({
            'data': [
                {
                    'id': x.id,
                    'address': x.address,
                    'price': x.price,
                    'type': x.type.name,
                    'zipcode': x.zipcode.code,
                    'beds': x.beds,
                    'bath': x.bath,
                    'size': x.size,
                    'image': x.images.first().image.url if x.images.first() else ""
                } for x in properties
            ]
        })

    # For page load
    properties = Property.objects.all()
    property_types_ids = Type.objects.all()
    # Korri's zipcode testing
    zipcodes_ids = ZipCode.objects.select_related('area', 'city').all()

    area_map = defaultdict(list)
    for z in zipcodes_ids:
        area_map[z.area.name].append({
            "id": z.id,
            "code": z.code,
            "city": z.city.name
        })
    areas = []
    for area_name, zips in area_map.items():
        areas.append({
            "area": area_name,
            "zipcodes": zips
        })

    return render(request, "property/properties.html", {
        "properties": properties,
        "areas": areas,
        "property_types": property_types_ids,
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
