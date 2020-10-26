from django.shortcuts import render


def index(request):
    # получаем результат из нашей БД

    return render(request, 'index.html')
