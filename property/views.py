from collections import defaultdict
from datetime import date

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, aget_object_or_404, get_object_or_404
from django.contrib import messages

from property.forms.property_form import CreatePropertyForm, PropertyImageForm
from property.models import Property, PropertyImage
from purchaseoffer.forms.purchase_offer_form import PurchaseOfferForm
from user.models import Profile, Type as ProfileType
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
                properties = properties.order_by('price')
            elif order_by == 'p-desc':
                properties = properties.order_by('-price')
            elif order_by == 'n-asc':
                properties = properties.order_by('address')
            elif order_by == 'n-desc':
                properties = properties.order_by('-address')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # Validate if both are provided and min > max
        if min_price and max_price:
            try:
                if int(min_price) > int(max_price):
                    return JsonResponse({
                        "error": "Minimum price cannot be greater than maximum price."
                    }, status=400)
            except ValueError:
                pass  # Ignore if values are not valid integers

        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)

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
        offer = Offer.objects.filter(property_id=id, buyer_id = request.user.id).last()
    property = get_object_or_404(Property, id=id)
    other_properties = Property.objects.exclude(id=id)[:6]
    form = PurchaseOfferForm(instance=offer)
    return render(request, "property/single_property.html", {
        "property": property,
        "other_properties": other_properties,
        "offer": offer,
        "form" : form,
    })

@login_required
def create_property(request):
    if not settings.DEBUG:
        messages.error(request, "The creation of properties is not enabled. Turn on debug mode to enable it.")
        return redirect("home")

    type_buyer = ProfileType.objects.get(name="Buyer")
    profile = Profile.objects.get(user=request.user)

    # Enforce Seller
    if profile.type == type_buyer:
        messages.error(request, "Buyers are not allowed to create properties")
        return redirect('home')

    if request.method == "POST":
        property_form = CreatePropertyForm(request.POST)
        images_form = PropertyImageForm(request.POST, request.FILES)
        if property_form.is_valid() and images_form.is_valid():
            # Validate prop form and then save
            # Check if rooms >= beds
            # Check price is not negative
            new_property = property_form.save(commit=False)
            new_property.seller = request.user
            new_property.list_date = date.today()
            new_property.is_sold = False
            new_property.save()

            PropertyImage.objects.create(
                property=new_property,
                image=images_form.cleaned_data.get('main_image'),
                is_main=False
            )

            other_images = request.FILES.getlist("other_images")

            for image in other_images:
                image_ins = PropertyImage(property=new_property, image=image, is_main=False)
                image_ins.save()
            messages.success(request, "Property created successfully")
            return redirect('property_by_id', id=new_property.id)
        else:
            print("Prop_form errors:", property_form.errors)
            print("Image form errors:", images_form.errors)
            messages.error(request, f"Please enter a valid property")
            return render(request, "property/create_property.html", {
                'property_form': property_form,
                'images_form': images_form
            })
    else:
        property_form = CreatePropertyForm()
        images_form = PropertyImageForm()
        return render(request, 'property/create_property.html', {
            'property_form': property_form,
            'images_form': images_form,
        })

@login_required
def my_properties(request):
    buyer_type = ProfileType.objects.get(name="Buyer")
    profile = Profile.objects.get(user=request.user)
    if profile.type == buyer_type:
        messages.error(request, "You are not allowed to create properties")
        return redirect('home')
    properties = Property.objects.filter(seller=request.user)

    return render(request, "property/my_properties.html", {
        "properties": properties,
    })
@login_required
def edit_property(request, id):

    property = Property.objects.get(id=id)

    if request.method == "POST":
        property_form = CreatePropertyForm(request.POST, instance=property)
        if property_form.is_valid():
            property_form.save()
            messages.success(request, "Property updated successfully.")
            return redirect("property_by_id", id=property.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        property_form = CreatePropertyForm(instance=property)

    return render(request, "property/edit_property.html", {
        "property_form": property_form,
        "property": property,
    })
