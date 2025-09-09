from django.shortcuts import render

# Create your views here.
def jambo_view(request):
    return render(request, "jambo_view.html")