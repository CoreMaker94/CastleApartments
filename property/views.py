from django.shortcuts import HttpResponse
from django.shortcuts import render
import property
from property.models import Property
# Create your views here.
#View to display all properties
def property_list(request):
    return render(request, "property/properties.html", {
        "properties": property.objects.all()
    })
# View to display a single property by its ID
def property_by_id(request, id):
    property = Property.objects.get(id=id)
    return render(request, "property/property_details.html", {
        "property": property
    })
