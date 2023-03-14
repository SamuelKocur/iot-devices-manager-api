import os
import datetime

from django.http import HttpResponse
from django.shortcuts import render


def index_view(request):
    file_path = 'media/mobile/android/app-arm64-v8a-release.apk'
    last_modified = os.path.getmtime(file_path)
    last_modified_date_android = datetime.datetime.fromtimestamp(last_modified)
    last_modified_date_ios = ""
    context = {
        'last_modified_android': last_modified_date_android,
        'last_modified_ios': last_modified_date_ios,
    }

    response = render(request, 'index.html', context)
    return HttpResponse(response)
