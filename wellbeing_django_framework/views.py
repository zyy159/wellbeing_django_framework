from django.http import HttpResponse,JsonResponse

def login(request):
    username = request.POST["Username"];
    password = request.POST["Password"];
    return HttpResponse("True")

def register(request):
    username = request.POST["Username"];
    password = request.POST["Password"];
    email = request.POST["Email"];
    return HttpResponse("True")

