from django.http import HttpResponse
from django.shortcuts import render


def index_view(request):
    response = render(request, 'index.html')
    return HttpResponse(response)
