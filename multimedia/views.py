from django.shortcuts import render
from .models import VideoUpload
# Create your views here.

def types(request):
    typer = request.GET["type"]
    user = request.user
    # fetch video based on type
    videoDetails = VideoUpload.objects.filter(typs = typer)
    print(len(videoDetails))
    context = {
        'user': user,
        "videoDetails":videoDetails,
    }
    return render(request, "type.html", {"context": context})

def cart(request):
    cartName = request.GET["cartName"]
    # fetch video basedon cartName value from request
    videoDetails = VideoUpload.objects.filter(cartegory_id = cartName)
    context = {
        "videoDetails": videoDetails,
    }
    return render(request, "categories.html", {"context":context})
