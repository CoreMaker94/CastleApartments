from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.
def register(request):
    if request.method == "POST":
        print(1)
    else:
        return render(request, "user/register.html", {
            'form': UserCreationForm(),
        })