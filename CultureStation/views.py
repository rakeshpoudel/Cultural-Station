import json
from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from shop.models import Product, Cart, Dresse, Caste, OrderSummary, OrderDetail, Event


file = open('chat.txt','r').readlines()
chatbot = ChatBot("rentbot")
# trainer = ListTrainer(chatbot)
# trainer.train(file)


@csrf_exempt
def get_response(request):
    response = {'status': None}

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data['message']

        chat_response = chatbot.get_response(message).text
        response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
        response['status'] = 'ok'

    else:
        response['error'] = 'no post data found'

    return HttpResponse(
        json.dumps(response),
            content_type="application/json"
        )


def home(request):
    # -------------- views to display product by category
    # allprods = []
    # catprods = Product.objects.values('category')
    # cats = {item['category'] for item in catprods}
    #
    # for cat in cats:
    #     prod = Product.objects.filter(category=cat)
    #     n = len(prod)
    #     allprods.append([prod, range(1, n)])
    #
    # context = {'allprods':allprods}

    # --------------------------------end
    current_user = request.user.id

    prods_in_order = []
    products = []
    prod = Product.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(prod, 12)
    try:
        prods = paginator.page(page)
    except:
        prods = paginator.page(1)

    n = len(prods)
    products.append([prods, range(1, n)])

    prod_order = OrderSummary.objects.filter(user_id=current_user).last()
    if prod_order:
        prods_num = prod_order.order_number
        prods_in_order = OrderDetail.objects.filter(order_number=prods_num, customer_id=current_user)

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')
    event = Event.objects.last()
    e_post = event.event_posted
    e_day = event.event_days
    e_status = event.event_status
    expire_d = e_post + timedelta(days=e_day)
    expire_t = datetime.now().date()
    if expire_d <= expire_t:
        expire = 1
    else:
        expire = 0

    ctx = {}
    query = request.GET.get('q')

    if query:
        lookups = Q(name__icontains=query) | Q(dress_type__dress__icontains=query) | Q(designer__designer__icontains=query) | Q(caste_category__caste__icontains=query)| Q(element_category__icontains=query)
        prodquery = []
        pq = Product.objects.filter(lookups).distinct()
        page = request.GET.get('page', 1)
        paginator = Paginator(pq, 10)
        try:
            pqs = paginator.page(page)
        except:
            pqs = paginator.page(1)

        n = len(pqs)
        prodquery.append([pqs, range(1, n)]) 
    else:
        prodquery = ''

    ctx["prodquery"] = prodquery

    if request.is_ajax():
        html = render_to_string(
                template_name = "shop/search_related.html",
                context = {"prodquery":prodquery}
            )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    context = {'products': products, 'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'event': event, 'expire': expire, 'event_status': e_status, 'prod_order': prod_order, 'prods_in_order': prods_in_order, 'ctx':ctx}
    return render(request, 'index.html', context)
