
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
import json

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from robots.forms import RobotForm
from robots.models import Robot


@csrf_exempt
def model_create(request):
    form_data = json.loads(request.body.decode())
    # получаем json данные, валидируем их в словарь
    f = RobotForm(form_data)
    #создаем форму RobotForm для проверки данных на правильность - is_valid()
    if f.is_valid():
        model = f.cleaned_data['model']
        version = f.cleaned_data['version']
        created = f.cleaned_data['created']
        serial = f'{model}-{version}'
        Robot.objects.create(serial=serial, model=model,version=version, created=created)
        # сохраняем в нашей модели Robot, одновременно создавая поле serial
        return HttpResponse('Robot was created')
    else:
        raise Http404
        #выводим ошибку если данные не валидны

