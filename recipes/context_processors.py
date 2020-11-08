from recipes.models import Purchase


def number(request):
    """подсчет количества покупок"""
    purchase_number = Purchase.objects.filter(user=request.user).count()
    context = {
        'number': purchase_number
    }
    return context
