from django.http import JsonResponse
from django.shortcuts import render
from property.models import Property
from zipcode.models import ZipCode
from property.models import Type


def property_list(request):
    if 'search_filter' in request.GET:
        return JsonResponse({
            'data': [
                {
                    'id': x.id,
                    'address': x.address,
                    'price': x.price,
                    'type': x.type.name,
                    # TODO: image
                    # 'image', x.propertyimage_set_first().image if x.propertyimage_set.exists() else None,
                    'zipcode': x.zipcode.code,
                } for x in Property.objects.filter(address__icontains=request.GET['search_filter']).order_by('address')
            ]
        })
    properties = Property.objects.all()
    return render(request, "property/properties.html", {
        "properties": properties,
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
    property = Property.objects.get(id=id)
    other_properties = Property.objects.exclude(id=id)[:6]
    return render(request, "property/single_property.html", {
        "property": property,
        "other_properties": other_properties,

    })
