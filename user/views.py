from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        #TODO decide what to if form is not valid
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        return render(request, "user/register.html", {
            'form': UserCreationForm(),
        })

#own profile view
def profile(request):
    return render(request, 'user/profile.html', {
        'profile': profile,
    })

##### TODO Fix this shit
# User visitation view
def get_profile_by_id(request, id):
    profile = UserProfile.objects.get(id=id)
    # If buyer
    if profile.type_id == 1:
        purchaseoffers = Offer.objects.filter(buyer_id=id)
        return render(request, 'profile/profile.html', {
            'profile': profile,
            'purchaseoffers': purchaseoffers
        })
    # If seller
    else:
        properties = Property.objects.filter(seller_id=id)
        return render(request, 'profile/profile.html', {
            'profile': profile,
            'properties': properties
        })