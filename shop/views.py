import random
import requests as req
import re
import hashlib
import hmac
import base64
import json
import uuid
from abc import ABC
from math import ceil
from twilio.rest import Client

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Avg, Func, F, Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import Product, UserDetail, Cart, Rating, ProductQuery, OrderDetail, OrderSummary, \
    Contact, OrderUpdate, ShippingCity, Wishlist, Notification, Cancellation, Dresse, Caste
from .authenticate import EmailBackend
import json
from CultureStation.settings import EMAIL_HOST_USER

UserModel = get_user_model()


def loginUser(request):
    pathnext = request.POST.get('next')
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None and pathnext == '':
                login(request, user)
                return redirect('home')
            if user is not None and pathnext != '':
                if pathnext == 'None':
                    login(request, user)
                    return redirect('home')
                else:
                    login(request, user)
                    return redirect(pathnext)
            else:
                messages.info(request, 'Email or Password is incorrect! Please enter valid email and password')

    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'pathnext': pathnext, 'dress_men': dress_men, 'dress_women': dress_women}
    return render(request, 'account/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    if request.method == 'POST':
        pathnext = request.POST.get('next')
        if pathnext == '':
            logout(request)
            return redirect('home')
        else:
            logout(request)
            return redirect(pathnext)


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if username != '' and email != '' and password1 != '':
                if password1 == password2:
                    if User.objects.filter(username=username).exists():
                        messages.info(request, 'Username already taken')
                    elif User.objects.filter(email=email).exists():
                        messages.info(request, 'Email already taken')
                    else:
                        user = User.objects.create_user(username=username, password=password1, email=email)
                        user.is_active = False
                        user.save()

                        current_site = get_current_site(request)
                        mail_subject = 'Email Verification'
                        html_message = render_to_string('account/acc_active_email.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': default_token_generator.make_token(user),

                        })
                        plain_message = strip_tags(html_message)
                        from_email = EMAIL_HOST_USER
                        to = email
                        mail.send_mail(mail_subject, plain_message, from_email, [to], fail_silently=False,
                                       html_message=html_message)
                        return redirect('verification')
                else:
                    messages.info(request, 'Your password is not matching')
            else:
                messages.info(request, 'All fields are required!')

    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'dress_men': dress_men, 'dress_women': dress_women}
    return render(request, 'account/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('verified')
    else:
        messages.info(request, 'Activation link is invalid!')
        return redirect('verified')


def verification(request):
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'dress_men': dress_men, 'dress_women': dress_women}
    return render(request, 'account/verification.html', context)


def verified(request):
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'dress_men': dress_men, 'dress_women': dress_women}
    return render(request, 'account/verified.html', context)


def header(request):
    current_user = request.user.id

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))

    context = {'cart_item': cart_item}
    return render(request, 'shop/header.html', context)


def dropdown(request):
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'dress_men': dress_men, 'dress_women': dress_women}
    return render(request, 'shop/dropdown.html', context)


# def searchMatch(query, item):
#     # '''return true only if query matches the item'''
#     if query in item.desc.lower() or query in item.name.lower():
#         return True
#     else:
#         return False


# def search(request):
#     query = request.POST.get('search', '')
#     allprods = []
#     prodtemp = Product.objects.all()
#     products = [item for item in prodtemp if searchMatch(query, item)]
#     n = len(products)
#     if len(products) != 0:
#         allprods.append([products, range(1, n)])

#     context = {'allprods': allprods, "msg": ""}
#     if len(products) == 0 or len(query) == 0:
#         context = {'msg': "Please make sure to enter relevant search query"}
#     return render(request, 'shop/search.html', context)


def search(request):
    current_user = request.user.id
    products = []
    n = 0
    if 'search' in request.session:
        del request.session['search']
        request.session.modified = True
    if request.method=="POST":
        s_query = request.POST.get('query')
        if s_query != '':
            lookups = Q(name__icontains=s_query) | Q(dress_type__dress__icontains=s_query) | Q(designer__designer__icontains=s_query) | Q(caste_category__caste__icontains=s_query)| Q(element_category__icontains=s_query) | Q(person_category=s_query)
            prods = Product.objects.filter(lookups).distinct()

            n = len(prods)
            products.append([prods, range(1, n)])

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'products':products, 'squery': s_query, 'len': n}
    return render(request, 'shop/search.html', context)


def about(request):
    context = {}
    return render(request, 'shop/about.html', context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()

    context = {}
    return render(request, 'shop/contact.html', context)


# @login_required(login_url='login')
# def tracker(request):
#     if request.method == "POST":
#         orderId = request.POST.get('orderId', '')
#         email = request.POST.get('email', '')
#         try:
#             order = Order.objects.filter(id=orderId, email=email)
#             if len(order) > 0:
#                 update = OrderUpdate.objects.filter(order_id=orderId)
#                 updates = []
#                 for item in update:
#                     updates.append({'text': item.update_desc, 'time': item.timestamp})
#                     response = json.dumps([updates, order[0].items_json], default=str)
#                 return HttpResponse(response)
#             else:
#                 return HttpResponse('{}')
#         except Exception as e:
#             return HttpResponse('{}')
#
#     context = {}
#     return render(request, 'shop/tracker.html', context)


class Round(Func, ABC):
    function = 'ROUND'
    arity = 2


def productView(request, slug):
    product = Product.objects.filter(slug=slug)
    p_id = Product.objects.filter(slug=slug).first()
    pp_id = p_id.id
    pp_dress = p_id.dress_type
    pp_gender = p_id.person_category
    pp_designer = p_id.designer
    current_user = request.user.id

    prod_list = []
    recommend_prods = Product.objects.filter(dress_type=pp_dress).exclude(slug=slug)
    n = len(recommend_prods)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    prod_list.append([recommend_prods, range(1, nSlides), nSlides])

    rating = Rating.objects.filter(product_id=pp_id).aggregate(average_rates=Round(Avg('ratings'), 1))
    rating_total_count = Rating.objects.filter(product_id=pp_id).count()
    rating_five_star_count = Rating.objects.filter(product_id=pp_id, ratings=5).count()
    rating_four_star_count = Rating.objects.filter(product_id=pp_id, ratings=4).count()
    rating_three_star_count = Rating.objects.filter(product_id=pp_id, ratings=3).count()
    rating_two_star_count = Rating.objects.filter(product_id=pp_id, ratings=2).count()
    rating_one_star_count = Rating.objects.filter(product_id=pp_id, ratings=1).count()

    query_set = []
    question = ProductQuery.objects.filter(product_id=pp_id).order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(question, 10)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    n = len(questions)
    query_set.append([questions, range(1, n)])

    review_set = []
    review = Rating.objects.filter(product_id=pp_id).exclude(review='')
    page = request.GET.get('page', 1)
    paginator = Paginator(review, 10)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    r_n = len(reviews)
    review_set.append([reviews, range(1, n)])    

    wish_prod = Wishlist.objects.filter(product_id=pp_id)

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'product': product[0],
               'rating': rating,
               'rating_five': rating_five_star_count,
               'rating_four': rating_four_star_count, 'rating_three': rating_three_star_count,
               'rating_two': rating_two_star_count, 'rating_one': rating_one_star_count,
               'rating_total_count': rating_total_count, 'prod_list': prod_list, 'query_set': query_set,
               'wish_prod': wish_prod, 'review_set': review_set, 'r_n': r_n}
    return render(request, 'shop/product_view.html', context)


@login_required(login_url='login')
def review_rate(request):
    current_user = request.user.username
    current_user_id = request.user.id
    rate = 1
    star1 = 0
    star2 = 0
    star3 = 0
    star4 = 0
    star5 = 0
    star1_c = 0
    star2_c = 0
    star3_c = 0
    star4_c = 0
    star5_c = 0
    keyword_star1 = ['worst', 'bad', 'not nice', 'not good', 'not satisfying', 'worst quality' 'not satisfied', 'not like', 'dont like', "don't like", 'sad', 'not happy', 'disappointed']
    keyword_star2 = ['not bad', 'bad quality']
    keyword_star3 = ['satisfying', 'satisfied', 'nice', 'good', 'like', 'not disappointing', 'not disappoint', 'not disappointed']
    keyword_star4 = ['perfect', 'better', 'very good', 'very nice', 'very satisfying', 'very satisfied', 'appreciate', 'quality', 'good quality']
    keyword_star5 = ['thanks', 'thank you', 'great','best', 'excellent', 'love', 'awesome', 'wow', 'fantastic', 'amazing', 'amazed', 'happy', 'fabulous', 'asthetic', 'super', 'superb', 'super quality', 'beautiful', 'most beautiful', 'very beautiful', 'best quality']
    if request.method == "POST":
        review = request.POST.get('review')
        product_id = request.POST.getlist('product_id[]')
        if review != '':
            r_string = re.sub('[!@#$.,;:"]', '', review)
            split_r = r_string.split()
            split_mul = list(map(' '.join, zip(split_r[:-1], split_r[1:])))

            for s in split_r:
                if s in keyword_star1:
                    star1 = star1 + 1
                if s in keyword_star2:
                    star2 = star2 + 1
                if s in keyword_star3:
                    star3 = star3 + 1
                if s in keyword_star4:
                    star4 = star4 + 1
                if s in keyword_star5:
                    star5 = star5 + 1
            for s in split_mul:
                if s in keyword_star1:
                    star1_c = star1_c + 1
                if s in keyword_star2:
                    star2_c = star2_c + 1
                if s in keyword_star3:
                    star3_c = star3_c + 1
                if s in keyword_star4:
                    star4_c = star4_c + 1
                if s in keyword_star5:
                    star5_c = star5_c + 1

            if star1_c != 0 or star2_c != 0 or star3_c != 0 or star4_c != 0 or star5_c != 0:
                if star1_c > star2_c:
                    if star1_c > star3_c:
                        if star1_c > star4_c:
                            if star1_c > star5_c:
                                rate = 1
                            else:
                                rate = 5
                        else:
                            if star4_c > star5_c:
                                rate = 4
                            else:
                                rate = 5
                    else:
                        if star3_c > star4_c:
                            if star3_c > star5_c:
                                rate = 3
                            else:
                                rate = 5
                        else:
                            if star4_c > star5_c:
                                rate = 4
                            else:
                                rate = 5
                else:
                    if star2_c > star3_c:
                        if star2_c > star4_c:
                            if star2_c > star5_c:
                                rate = 2
                            else:
                                rate = 5
                        else:
                            if star4_c > star5_c:
                                rate = 4
                            else:
                                rate = 5

                    else:
                        if star3_c > star4_c:
                            if star3_c > star5_c:
                                rate = 3
                            else:
                                rate = 5
                        else:
                            if star4_c > star5_c:
                                rate = 4
                            else:
                                rate = 5

            if star1_c == 0 and star2_c == 0 and star3_c == 0 and star4_c == 0 and star5_c == 0:
                if star1 > star2:
                    if star1 > star3:
                        if star1 > star4:
                            if star1 > star5:
                                rate = 1
                            else:
                                rate = 5
                        else:
                            if star4 > star5:
                                rate = 4
                            else:
                                rate = 5
                    else:
                        if star3 > star4:
                            if star3 > star5:
                                rate = 3
                            else:
                                rate = 5
                        else:
                            if star4 > star5:
                                rate = 4
                            else:
                                rate = 5
                else:
                    if star2 > star3:
                        if star2 > star4:
                            if star2 > star5:
                                rate = 2
                            else:
                                rate = 5
                        else:
                            if star4 > star5:
                                rate = 4
                            else:
                                rate = 5

                    else:
                        if star3 > star4:
                            if star3 > star5:
                                rate = 3
                            else:
                                rate = 5
                        else:
                            if star4 > star5:
                                rate = 4
                            else:
                                rate = 5
        else:
            rate = 1

        for ids in product_id:
            prod = Product.objects.filter(id=ids).first()
            image = prod.main_image
            rating = Rating(user_name=current_user, product_id=ids, ratings=rate, review=review, image=image)
            rating.save()

        prod_order = OrderSummary.objects.filter(user_id=current_user_id).last()
        prod_order_num = prod_order.order_number
        OrderSummary.objects.filter(user_id=current_user_id, order_number=prod_order_num).update(review_status='rated')

    return HttpResponse()


@login_required(login_url='login')
def rating(request):
    current_user = request.user.username

    if request.method == "POST":
        user_name = current_user
        product_id = request.POST.getlist('product_id')
        ratings = request.POST.get('ratings')
        for ids in product_id:
            rates = Rating(user_name=user_name, product_id=ids, ratings=ratings)
            rates.save()

    return HttpResponse()


@login_required(login_url='login')
def rating_refuse(request):
    current_user = request.user.id

    prod_order = OrderSummary.objects.filter(user_id=current_user).last()
    prod_order_num = prod_order.order_number
    OrderSummary.objects.filter(user_id=current_user, order_number=prod_order_num).update(review_status='refused')

    return redirect('home')


@login_required(login_url='login')
def add_to_cart(request, pid, rw, ds):
    current_user = request.user.id
    Cart.objects.filter(user_id=current_user, product_id=pid, renting_way=rw, product_size=ds).delete()
    slug_p = Product.objects.filter(id=pid).first()
    slug = slug_p.slug

    if request.method == "POST":
        slug = slug
        user_id = current_user
        product_id = pid
        product_name = request.POST.get('product_name', '')
        gender = request.POST.get('gender', '')
        caste_type = request.POST.get('caste_type', '')
        designer = request.POST.get('designer', '')
        dress_type = request.POST.get('element_type', '')
        renting_way = request.POST.get('renting_way', '')
        product_size = request.POST.get('product_size', '')
        quantity = request.POST.get('quantity', '')
        amount = request.POST.get('amount', '')
        refund = request.POST.get('refund', '')
        renting_days = request.POST.get('renting_days', '')
        delivery_date = request.POST.get('delivery_date', '')
        return_date = request.POST.get('return_date', '')
        image = request.POST.get('image', '')
        cart = Cart(slug=slug, user_id=user_id, product_id=product_id, product_name=product_name, gender=gender, caste_type=caste_type,
                    designer=designer, dress_type=dress_type, renting_way=renting_way, product_size=product_size,
                    quantity=quantity, amount=amount, refund=refund,
                    renting_days=renting_days, delivery_date=delivery_date, returning_date=return_date, image=image)
        cart.save()

    return HttpResponse()


@login_required(login_url='login')
def add_to_wishlist(request, pid):
    current_user = request.user.id
    user_name = request.user.username
    Wishlist.objects.filter(user_id=current_user, product_id=pid).delete()

    if request.method == "POST":
        user_name = user_name
        user_id = current_user
        product_id = pid
        product_name = request.POST.get('product_name', '')
        caste_type = request.POST.get('caste_type', '')
        designer = request.POST.get('designer', '')
        dress_type = request.POST.get('element_type', '')
        product_size = request.POST.get('product_size', '')
        image = request.POST.get('image', '')
        wishlist = Wishlist(user_name=user_name, user_id=user_id, product_id=product_id, product_name=product_name,
                            designer=designer, caste_type=caste_type,
                            dress_type=dress_type, product_size=product_size,
                            image=image)
        wishlist.save()

    return HttpResponse()


@login_required(login_url='login')
def cart_prod_view(request, slug, cid):
    product = Product.objects.filter(slug=slug)
    p_id = Product.objects.filter(slug=slug).first()
    pp_id = p_id.id
    pp_dress = p_id.dress_type
    current_user = request.user.id

    cart_elements = Cart.objects.filter(id=cid)

    prod_list = []
    recommend_prods = Product.objects.filter(dress_type=pp_dress).exclude(id=pp_id)
    n = len(recommend_prods)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    prod_list.append([recommend_prods, range(1, nSlides), nSlides])

    rating = Rating.objects.filter(product_id=pp_id).aggregate(average_rates=Round(Avg('ratings'), 1))
    rating_total_count = Rating.objects.filter(product_id=pp_id).count()
    rating_five_star_count = Rating.objects.filter(product_id=pp_id, ratings=5).count()
    rating_four_star_count = Rating.objects.filter(product_id=pp_id, ratings=4).count()
    rating_three_star_count = Rating.objects.filter(product_id=pp_id, ratings=3).count()
    rating_two_star_count = Rating.objects.filter(product_id=pp_id, ratings=2).count()
    rating_one_star_count = Rating.objects.filter(product_id=pp_id, ratings=1).count()

    query_set = []
    question = ProductQuery.objects.filter(product_id=pp_id).order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(question, 10)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    n = len(questions)
    query_set.append([questions, range(1, n)])

    review_set = []
    review = Rating.objects.filter(product_id=pp_id).exclude(review='')
    page = request.GET.get('page', 1)
    paginator = Paginator(review, 10)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    r_n = len(reviews)
    review_set.append([reviews, range(1, n)])  

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'product': product[0],
               'cart_elements': cart_elements[0],
               'rating': rating,
               'rating_five': rating_five_star_count,
               'rating_four': rating_four_star_count, 'rating_three': rating_three_star_count,
               'rating_two': rating_two_star_count, 'rating_one': rating_one_star_count,
               'rating_total_count': rating_total_count, 'prod_list': prod_list, 'query_set': query_set,
               'review_set': review_set, 'r_n': r_n}
    return render(request, 'shop/cart/cart_product_view.html', context)


@login_required(login_url='login')
def cart(request):
    current_user = request.user.id
    order_stat = "Returned"
    if  OrderSummary.objects.filter(user_id=current_user).exists():
        order_track = OrderSummary.objects.filter(user_id=current_user).last()
        order_stat = order_track.order_status

    all_cart_prods = []
    length = 0
    cart_prods = Cart.objects.values('delivery_date')
    carts = {item['delivery_date'] for item in cart_prods}

    for cart_p in carts:
        prod = Cart.objects.filter(user_id=current_user, delivery_date=cart_p).order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(prod, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        n = len(products)
        if n > 0:
            length = 1
        all_cart_prods.append([products, range(1, n)])

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women,
               'all_cart_prods': all_cart_prods, 'length': length, 'order_stat': order_stat}
    return render(request, 'shop/cart/cart.html', context)


@login_required(login_url='login')
def cart_update(request, rw, ds, dd, rd, pid, cid):
    current_user = request.user.id
    Cart.objects.filter(id=cid).delete()
    Cart.objects.filter(user_id=current_user, product_id=pid, renting_way=rw, product_size=ds, delivery_date=dd,
                        returning_date=rd).delete()
    slug_p = Product.objects.filter(id=pid).first()
    slug = slug_p.slug

    if request.method == "POST":
        slug = slug
        user_id = current_user
        product_id = pid
        product_name = request.POST.get('product_name', '')
        caste_type = request.POST.get('caste_type', '')
        gender = request.POST.get('gender', '')
        designer = request.POST.get('designer', '')
        dress_type = request.POST.get('element_type', '')
        renting_way = request.POST.get('renting_way', '')
        product_size = request.POST.get('product_size', '')
        quantity = request.POST.get('quantity', '')
        amount = request.POST.get('amount', '')
        refund = request.POST.get('refund', '')
        renting_days = request.POST.get('renting_days', '')
        delivery_date = request.POST.get('delivery_date', '')
        return_date = request.POST.get('return_date', '')
        image = request.POST.get('image', '')
        cart = Cart(slug=slug, user_id=user_id, product_id=product_id, product_name=product_name, gender=gender, caste_type=caste_type,
                    designer=designer, dress_type=dress_type, renting_way=renting_way, product_size=product_size,
                    quantity=quantity, amount=amount, refund=refund,
                    renting_days=renting_days, delivery_date=delivery_date, returning_date=return_date, image=image)
        cart.save()

    return HttpResponse()


@login_required(login_url='login')
def cart_delete(request, cid):
    current_user = request.user.id
    object = Cart.objects.get(user_id=current_user, id=cid)
    object.delete()

    return redirect('cart')


def cart_count(request):
    current_user = request.user.id

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))

    context = {'cart_item': cart_item}
    return render(request, 'shop/cart/cart_count.html', context)


@login_required(login_url='login')
def query(request, pid):
    if request.method == "POST":
        product_id = pid
        prod = Product.objects.filter(id=product_id).first()
        image = prod.main_image
        product_name = request.POST.get('product_name', '')
        user_name = request.POST.get('user_name', '')
        question = request.POST.get('question')

        query_set = ProductQuery(product_id=product_id, product_name=product_name, user_name=user_name,
                                 question=question, image=image)
        query_set.save()

    return HttpResponse()


def queryPage(request, pid):
    query_set = []
    question = ProductQuery.objects.filter(product_id=pid).order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(question, 10)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    n = len(questions)
    query_set.append([questions, range(1, n)])

    context = {'query_set': query_set}
    return render(request, 'shop/question.html', context)


@login_required(login_url='login')
def proceed_rent(request):
    current_user = request.user.id

    prod_ids = request.POST.getlist('prod_ids')
    request.session['prod_ids'] = prod_ids
    sub_total_amount = request.POST.get('sub_total_amount')
    request.session['sub_total_amount'] = sub_total_amount
    total_amount = request.POST.get('total_amount')
    request.session['total_amount'] = total_amount
    refund_amount = request.POST.get('refund_amount')
    request.session['refund_amount'] = refund_amount
    total_items = request.POST.get('t_items')
    request.session['total_items'] = total_items

    # SESSION_SAVE_EVERY_REQUEST

    list_items = Cart.objects.filter(id__in=request.session['prod_ids'])

    if len(list_items) != 0:
        city_list = ShippingCity.objects.all()

        cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
        dress_men = Dresse.objects.filter(gender='men').order_by('id')
        dress_women = Dresse.objects.filter(gender='women').order_by('id')

        if UserDetail.objects.filter(user_id=current_user).exists():
            user_d = UserDetail.objects.filter(user_id=current_user).first()
            u_first = user_d.first_name
            u_city = user_d.shipping_city
            u_verify = user_d.verification
            shipping_charge = ShippingCity.objects.filter(city=u_city).first()

            context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women,
                       'list_items': list_items, 'city_list': city_list, 'user_detail': user_d,
                       'u_first': u_first, 'u_city': u_city, 'u_verify': u_verify, 'total_amount': total_amount,
                       'refund_amount': refund_amount, 'total_items': total_items, 'shipping_charge': shipping_charge,
                       }

            return render(request, 'shop/proceed_rent.html', context)
        else:
            context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women,
                       'list_items': list_items,
                       'city_list': city_list}
            return render(request, 'shop/proceed_rent.html', context)
    else:
        return redirect('home')


def encrypt(hash_string):
    secret = b"30e4f3394c654d0b926d7e47c9b8d1ed33d325d82678486b8316a5d047677cdbe31b6e8cea924f7382a8875c6a0c0a626e21ce4db11b4171aafa1f722516ca62d4408dec27264fbfa27ead26d7fdd5e6682da543540948b9bac19d45ce1364a730618d1aab3f49cba548e9d466e58769780cfd8753b348cd9f892ed046224422"
    sha = hmac.new(secret, hash_string.encode(), hashlib.sha256)
    sha_signature = base64.b64encode(sha.digest()).decode()
    return sha_signature


@login_required(login_url='login')
def proceed_pay(request):
    current_user = request.user.id

    grand_total = request.POST.get('grand_total')
    request.session['grand_total'] = grand_total

    if grand_total:
        g_total = grand_total
        gt = str(grand_total)
        total_amount = request.session['total_amount']
        t_items = request.session['total_items']

        order_number = random.randint(123456789999, 987456321999)
        request.session['order_number'] = order_number
        order_num = str(order_number)

        sha_signature = 'none' #removed for security reasons
        request.session['sig'] = sha_signature

        user_d = UserDetail.objects.filter(user_id=current_user).first()
        u_city = user_d.shipping_city
        ship_charge = ShippingCity.objects.filter(city=u_city).first()

        cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
        dress_men = Dresse.objects.filter(gender='men').order_by('id')
        dress_women = Dresse.objects.filter(gender='women').order_by('id')

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 't_amount': total_amount,
                   'items': t_items, 'user_d': user_d,
                   'ship_charge': ship_charge, 'g_total': g_total, 'sha_signature': sha_signature}
        return render(request, 'shop/proceed_pay.html', context)
    else:
        return redirect('home')


def payment(request):
    
    return redirect('home')


def success_esewa_pay(request, oid, amt, refid):
    url ="https://uat.esewa.com.np/epay/transrec"
    data = {
        'amt': 100,
        'scd': 'epay_payment',
        'rid': refid,
        'pid':'pid8569',
    }
    resp = req.post(url, data)
    respond = resp.text
    if respond == 'Success':
        return redirect('order_update')
    else:
        return redirect('fail_esewa_pay')

    return HttpResponse()


def fail_esewa_pay(request):
    g_total = request.session['grand_total']

    context = {'g_total': g_total}
    return render(request, 'shop/fail_esewa_pay.html', context)



def verify_code(request):
    current_user = request.user.id

    if request.method == 'POST':
        code = request.POST.get('code')
        code_num = str(code)
        otp = request.session['otp']
        otp_num = str(otp)
        if code_num == otp_num:
            print(code_num)
            verify = 'verified'
            UserDetail.objects.filter(user_id=current_user).update(verification=verify)
            del request.session['otp']
            request.session.modified = True

    return HttpResponse()


def user_detail(request):
    current_user = request.user.id
    user_name = request.user.username
    user_email = request.user.email

    if request.method == 'POST':
        user_id = current_user
        user_name = user_name
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = user_email
        address = request.POST.get('address', '')
        contact = request.POST.get('contact', '')
        code = '+977'
        number = str(contact)
        user_num = code + number

        if contact == '9813702978':
            otp_number = random.randint(1234, 9999)
            otp = otp_number
            otp_code = str(otp)
            request.session['otp'] = otp
            verify = 'not verified'

            account_sid = 'AC950e1aa32ade454a1fd2144fb4b32109'
            auth_token = '5b5206fe18419c15d13262f1fe382902'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                     body='Your number verification code is: '+otp_code,
                     from_='+19374002805',
                     to=user_num
                 )

            #print(message.sid)
            detail = UserDetail(user_id=user_id, user_name=user_name, first_name=first_name, last_name=last_name,
                                email=email, address=address, contact=contact, verification=verify)
            detail.save()
        else:
            verify = 'verified'
            detail = UserDetail(user_id=user_id, user_name=user_name, first_name=first_name, last_name=last_name,
                                email=email, address=address, contact=contact, verification=verify)
            detail.save()

    return HttpResponse()


def user_update_shipping(request):
    current_user = request.user.id

    obj = UserDetail.objects.get(user_id=current_user)
    obj.shipping_city = request.POST.get('ship_city')
    obj.shipping_area = request.POST.get('ship_area')
    obj.shipping_address = request.POST.get('ship_address')
    obj.save()

    return HttpResponse()


@login_required(login_url='login')
def confirm_order(request):
    current_user = request.user.id

    if 'order_number' in request.session:
        order_number = request.session['order_number']

        order_prods = OrderDetail.objects.filter(customer_id=current_user, order_number=order_number)
        order_prods_sum = OrderSummary.objects.filter(user_id=current_user, order_number=order_number).first()
        payment_status = order_prods_sum.payment_status

        ids = request.session['prod_ids']
        recommend_rentals = OrderDetail.objects.filter(order_number=order_number).first()
        caste_cat_rental = recommend_rentals.dress_type
        idexclude = OrderDetail.objects.filter(order_number=order_number)
        idd = []
        for i in idexclude:
            iidd = i.product_id
            idd.append(iidd)

        recommend_products = []
        rental = Product.objects.filter(dress_type=caste_cat_rental).exclude(id__in=idd)
        page = request.GET.get('page', 1)
        paginator = Paginator(rental, 3)
        rentals = paginator.page(page)

        n = len(rentals)
        recommend_products.append([rentals, range(1, n)])

        sub_total = request.session['sub_total_amount']
        refund_total = request.session['refund_amount']
        grand_total = request.session['grand_total']
        user_d = UserDetail.objects.filter(user_id=current_user).first()
        u_city = user_d.shipping_city
        shipping_charge = ShippingCity.objects.filter(city=u_city).first()

        cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
        dress_men = Dresse.objects.filter(gender='men').order_by('id')
        dress_women = Dresse.objects.filter(gender='women').order_by('id')

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'sub_total': sub_total,
                   'charge': shipping_charge,
                   'refund': refund_total, 'g_total': grand_total, 'user_d': user_d, 'list': order_prods,
                   'order_num': order_number, 'recommend_rentals': recommend_products, 'payment':payment_status}
        return render(request, 'shop/confirm_order.html', context)
    else:
        return redirect('home')


def order_update(request):
    current_user = request.user.id
    user_name = request.user.username
    order_number = request.session['order_number']

    sub_total = request.session['sub_total_amount']
    refund_total = request.session['refund_amount']
    grand_total = request.session['grand_total']
    t_items = request.session['total_items']

    user_d = UserDetail.objects.filter(user_id=current_user).first()
    full_name = user_d.first_name + " " + user_d.last_name
    user_email = user_d.email
    user_address = user_d.address
    user_contact = user_d.contact
    ship_address = user_d.shipping_address + "," + user_d.shipping_area + "," + user_d.shipping_city
    shipping_city = user_d.shipping_city

    ship_charge = ShippingCity.objects.filter(city=shipping_city).first()
    shipping_charge = ship_charge.shipping_charge

    ids = request.session['prod_ids']

    items = Cart.objects.filter(id__in=ids).first()
    delivery = items.delivery_date

    list_items = Cart.objects.filter(id__in=ids)
    for i in list_items:
        prod_name = i.product_name
        prod_id = i.product_id
        c_type = i.caste_type
        gender = i.gender
        designer = i.designer
        e_type = i.dress_type
        rent_way = i.renting_way
        size = i.product_size
        prod_qty = i.quantity
        prod_amount = i.amount
        prod_refund = i.refund
        rent_days = i.renting_days
        deliver = i.delivery_date
        return_date = i.returning_date

        product = Product.objects.filter(id=prod_id).first()
        prod_img = product.main_image

        if 'payment' in request.session:
            payment = request.session['payment']
            method = request.session['method']
            orderDetail = OrderDetail(product_name=prod_name, gender=gender, order_number=order_number, product_id=prod_id,
                                      customer_name=full_name, customer_user_name=user_name, customer_id=current_user,
                                      customer_email=user_email,
                                      customer_contact=user_contact, customer_address=user_address, caste_type=c_type,
                                      designer=designer, dress_type=e_type, renting_way=rent_way, product_size=size,
                                      quantity=prod_qty,
                                      amount=prod_amount, refund=prod_refund, renting_days=rent_days, delivery_date=deliver,
                                      returning_date=return_date, shipping_address=ship_address,
                                      shipping_charge=shipping_charge, prod_image=prod_img, payment_status=payment, payment_method=method)
            orderDetail.save()
        else:
            orderDetail = OrderDetail(product_name=prod_name, gender=gender, order_number=order_number, product_id=prod_id,
                                      customer_name=full_name, customer_user_name=user_name, customer_id=current_user,
                                      customer_email=user_email,
                                      customer_contact=user_contact, customer_address=user_address, caste_type=c_type,
                                      designer=designer, dress_type=e_type, renting_way=rent_way, product_size=size,
                                      quantity=prod_qty,
                                      amount=prod_amount, refund=prod_refund, renting_days=rent_days, delivery_date=deliver,
                                      returning_date=return_date, shipping_address=ship_address,
                                      shipping_charge=shipping_charge, prod_image=prod_img)

            orderDetail.save()

        if size == 'S':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_s
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_s=stock_update)
        if size == 'M':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_m
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_m=stock_update)
        if size == 'L':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_l
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_l=stock_update)
        if size == 'XL':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_xl
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_xl=stock_update)
        if size == 'XXL':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_xxl
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_xxl=stock_update)
        if size == '3XL':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_3xl
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_3xl=stock_update)

    if 'payment' in request.session:
        payment = request.session['payment']
        method = request.session['method']
        orderSummary = OrderSummary(order_number=order_number, user_id=current_user, user_name=user_name,
                                    user_full_name=full_name, user_email=user_email, user_contact=user_contact,
                                    total_items=t_items, sub_total_amount=sub_total,
                                    total_refund=refund_total, shipping_charge=shipping_charge, grand_total=grand_total,
                                    delivery_date=delivery, shipping_address=ship_address, payment_status=payment, payment_method=method)
        orderSummary.save()
    else:
        orderSummary = OrderSummary(order_number=order_number, user_id=current_user, user_name=user_name,
                                    user_full_name=full_name, user_email=user_email, user_contact=user_contact,
                                    total_items=t_items, sub_total_amount=sub_total,
                                    total_refund=refund_total, shipping_charge=shipping_charge, grand_total=grand_total,
                                    delivery_date=delivery, shipping_address=ship_address)
        orderSummary.save()


    # order_prods = OrderDetail.objects.filter(customer_id=current_user, order_number=order_number)
    # order_invoice = OrderSummary.objects.filter(user_id=current_user, order_number=order_number).first()
    # current_site = get_current_site(request)
    # mail_subject = 'New Order'
    # html_message = render_to_string('shop/mail/ordermail.html', {
    #     'order_prods': order_prods,
    #     'invoice': order_invoice,
    #     'domain': current_site

    #     })
    # plain_message = strip_tags(html_message)
    # from_email = EMAIL_HOST_USER
    # to = EMAIL_HOST_USER
    # mail.send_mail(mail_subject, plain_message, from_email, [to], fail_silently=False, html_message=html_message)

    Cart.objects.filter(id__in=ids).delete()
    if 'payment' in request.session:
        del request.session['payment']
        request.session.modified = True
    if 'method' in request.session:
        del request.session['method']
        request.session.modified = True

    return redirect('confirm_order')


def order_credit_update(request):
    current_user = request.user.id
    user_name = request.user.username
    order_number = request.session['order_number']

    sub_total = request.session['sub_total_amount']
    refund_total = request.session['refund_amount']
    grand_total = request.session['grand_total']
    t_items = request.session['total_items']

    user_d = UserDetail.objects.filter(user_id=current_user).first()
    full_name = user_d.first_name + " " + user_d.last_name
    user_email = user_d.email
    user_address = user_d.address
    user_contact = user_d.contact
    ship_address = user_d.shipping_address + "," + user_d.shipping_area + "," + user_d.shipping_city
    shipping_city = user_d.shipping_city

    ship_charge = ShippingCity.objects.filter(city=shipping_city).first()
    shipping_charge = ship_charge.shipping_charge

    ids = request.session['prod_ids']

    items = Cart.objects.filter(id__in=ids).first()
    delivery = items.delivery_date

    list_items = Cart.objects.filter(id__in=ids)
    for i in list_items:
        prod_name = i.product_name
        prod_id = i.product_id
        c_type = i.caste_type
        gender = i.gender
        designer = i.designer
        e_type = i.dress_type
        rent_way = i.renting_way
        size = i.product_size
        prod_qty = i.quantity
        prod_amount = i.amount
        prod_refund = i.refund
        rent_days = i.renting_days
        deliver = i.delivery_date
        return_date = i.returning_date

        product = Product.objects.filter(id=prod_id).first()
        prod_img = product.main_image

        orderDetail = OrderDetail(product_name=prod_name, gender=gender, order_number=order_number, product_id=prod_id,
                                      customer_name=full_name, customer_user_name=user_name, customer_id=current_user,
                                      customer_email=user_email,
                                      customer_contact=user_contact, customer_address=user_address, caste_type=c_type,
                                      designer=designer, dress_type=e_type, renting_way=rent_way, product_size=size,
                                      quantity=prod_qty,
                                      amount=prod_amount, refund=prod_refund, renting_days=rent_days, delivery_date=deliver,
                                      returning_date=return_date, shipping_address=ship_address,
                                      shipping_charge=shipping_charge, prod_image=prod_img, payment_status='Paid With Card', payment_method='Paid With Card')

        orderDetail.save()

        if size == 'S':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_s
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_s=stock_update)
        if size == 'M':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_m
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_m=stock_update)
        if size == 'L':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_l
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_l=stock_update)
        if size == 'XL':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_xl
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_xl=stock_update)
        if size == 'XXL':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_xxl
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_xxl=stock_update)
        if size == '3XL':
            prod_id = i.product_id
            prod_qty = i.quantity
            prods = Product.objects.filter(id=prod_id).first()
            product_stock = prods.stock_size_3xl
            stock_update = product_stock - prod_qty
            Product.objects.filter(id=prod_id).update(stock_size_3xl=stock_update)

    orderSummary = OrderSummary(order_number=order_number, user_id=current_user, user_name=user_name,
                                    user_full_name=full_name, user_email=user_email, user_contact=user_contact,
                                    total_items=t_items, sub_total_amount=sub_total,
                                    total_refund=refund_total, shipping_charge=shipping_charge, grand_total=grand_total,
                                    delivery_date=delivery, shipping_address=ship_address, payment_status='Paid', payment_method='Paid With Card')
    orderSummary.save()

    Cart.objects.filter(id__in=ids).delete()
    if 'payment' in request.session:
        del request.session['payment']
        request.session.modified = True
    if 'method' in request.session:
        del request.session['method']
        request.session.modified = True

    return redirect('confirm_order')


def paid_esewa(request):
    payment = 'Paid With Esewa'
    method = 'Esewa' 
    request.session['payment'] = payment
    request.session['method'] = method

    return redirect('order_update')


def paid_khalti(request):
    payment = 'Paid With Khalti'
    method = 'Khalti'
    request.session['payment'] = payment
    request.session['method'] = method

    return redirect('order_update')


@login_required(login_url='login')
def manage_account_personal(request):
    current_user = request.user.id

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    try:
        user_personal = UserDetail.objects.filter(user_id=current_user).first()
        u_name = user_personal.first_name

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'user_p': user_personal,
                   'u_name': u_name}
        return render(request, 'account/manage_account_personal.html', context)
    except(ValueError, Exception):

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women}
        return render(request, 'account/manage_account_personal.html', context)


@login_required(login_url='login')
def account_personal_edit(request):
    current_user = request.user.id
    pathnext = request.POST.get('pathnext')

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    try:
        user_personal = UserDetail.objects.filter(user_id=current_user).first()
        u_name = user_personal.first_name

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'user_p': user_personal,
                   'u_name': u_name, 'pathnext': pathnext}
        return render(request, 'account/personal_edit.html', context)
    except(ValueError, Exception):

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'pathnext': pathnext}
        return render(request, 'account/personal_edit.html', context)


@login_required(login_url='login')
def personal_update(request):
    current_user = request.user.id
    user_name = request.user.username
    user_email = request.user.email
    pathnext = request.POST.get('pathnext')

    if request.method == 'POST':
        user_id = current_user
        user_name = user_name
        email = user_email
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_num = request.POST.get('contact')
        address = request.POST.get('address')

        if first_name == '' or last_name == '' or contact_num == '' or address == '':
            messages.info(request, 'All fields are required')
        else:
            if UserDetail.objects.filter(user_id=current_user).exists():
                UserDetail.objects.filter(user_id=current_user).update(first_name=first_name, last_name=last_name,
                                                                       contact=contact_num, address=address)
                if pathnext != '':
                    if pathnext == 'None':
                        return redirect('manage_account_personal')
                    else:
                        return redirect(pathnext)
                else:
                    return redirect('manage_account_personal')
            else:
                detail = UserDetail(user_id=user_id, user_name=user_name, first_name=first_name, last_name=last_name,
                                    email=email, address=address, contact=contact_num)
                detail.save()

                if pathnext != '':
                    if pathnext == 'None':
                        return redirect('manage_account_personal')
                    else:
                        return redirect(pathnext)
                else:
                    return redirect('manage_account_personal')

        user_personal = UserDetail.objects.filter(user_id=current_user).first()
        u_name = user_personal.first_name

        cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
        dress_men = Dresse.objects.filter(gender='men').order_by('id')
        dress_women = Dresse.objects.filter(gender='women').order_by('id')

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'pathnext': pathnext,
                   'user_p': user_personal, 'u_name': u_name}
        return render(request, 'account/personal_edit.html', context)


@login_required(login_url='login')
def manage_account_shipping(request):
    current_user = request.user.id

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    try:
        user_shipping = UserDetail.objects.filter(user_id=current_user).first()
        u_ship = user_shipping.shipping_city

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'user_s': user_shipping,
                   'u_ship': u_ship}
        return render(request, 'account/manage_account_shipping.html', context)
    except(ValueError, Exception):

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women}
        return render(request, 'account/manage_account_shipping.html', context)


@login_required(login_url='login')
def account_shipping_edit(request):
    current_user = request.user.id
    pathnext = request.POST.get('pathnext')

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    city_list = ShippingCity.objects.all()

    try:
        user_shipping = UserDetail.objects.filter(user_id=current_user).first()
        u_ship = user_shipping.first_name

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'user_s': user_shipping,
                   'u_ship': u_ship, 'pathnext': pathnext,
                   'city_list': city_list}
        return render(request, 'account/shipping_edit.html', context)
    except(ValueError, Exception):

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'pathnext': pathnext,
                   'city_list': city_list}
        return render(request, 'account/shipping_edit.html', context)


def shipping_update(request):
    current_user = request.user.id
    user_name = request.user.username
    user_email = request.user.email

    if request.method == 'POST':
        user_id = current_user
        user_name = user_name
        email = user_email
        ship_city = request.POST.get('ship_city')
        ship_area = request.POST.get('ship_area')
        ship_address = request.POST.get('ship_address')

        if UserDetail.objects.filter(user_id=current_user).exists():
            UserDetail.objects.filter(user_id=current_user).update(shipping_city=ship_city, shipping_area=ship_area,
                                                                   shipping_address=ship_address)
        else:
            ship = UserDetail(user_id=user_id, user_name=user_name, email=email, shipping_city=ship_city,
                              shipping_area=ship_area,
                              shipping_address=ship_address)
            ship.save()

    return HttpResponse()


@login_required(login_url='login')
def my_order(request):
    current_user = request.user.id

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    try:
        order_d = OrderSummary.objects.filter(Q(user_id=current_user), Q(order_status='Processing') |
                                              Q(order_status='Shipping') | Q(order_status='Delivered')).last()

        order_s = order_d.order_status
        order_num = order_d.order_number

        orders = OrderDetail.objects.filter(order_number=order_num)

        all_order = []
        order_return = OrderDetail.objects.filter(customer_id=current_user, order_status='Rental Returned'). \
            exclude(order_number=order_num).order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(order_return, 7)
        try:
            rentals = paginator.page(page)
        except PageNotAnInteger:
            rentals = paginator.page(1)
        except EmptyPage:
            rentals = paginator.page(paginator.num_pages)

        n = len(rentals)
        all_order.append([rentals, range(1, n)])

        cancel_order = OrderSummary.objects.filter(user_id=current_user, order_number=order_num).last()
        o_date = cancel_order.ordered_date
        today_date = datetime.now(timezone.utc)
        cancel_time = today_date - o_date
        cancel_expire = cancel_time.total_seconds()

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'order_d': order_d,
                   'order_s': order_s, 'orders': orders,
                   'all_order': all_order, 'cancel_expire': cancel_expire}
        return render(request, 'account/my_order.html', context)

    except (ValueError, Exception):
        all_order = []
        order_return = OrderDetail.objects.filter(customer_id=current_user, order_status='Rental Returned'). \
            order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(order_return, 7)
        try:
            rentals = paginator.page(page)
        except PageNotAnInteger:
            rentals = paginator.page(1)
        except EmptyPage:
            rentals = paginator.page(paginator.num_pages)

        n = len(rentals)
        all_order.append([rentals, range(1, n)])

        context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'all_order': all_order}
        return render(request, 'account/my_order.html', context)


@login_required(login_url='login')
def my_wishlist(request):
    current_user = request.user.id

    all_wishlist = []
    wishlist = Wishlist.objects.filter(user_id=current_user).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(wishlist, 7)
    try:
        wishlists = paginator.page(page)
    except PageNotAnInteger:
        wishlists = paginator.page(1)
    except EmptyPage:
        wishlists = paginator.page(paginator.num_pages)

    n = len(wishlists)
    all_wishlist.append([wishlists, range(1, n)])

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'all_wishlist': all_wishlist}
    return render(request, 'account/my_wishlist.html', context)


def delete_wishlist(request, wid):
    current_user = request.user.id

    Wishlist.objects.filter(user_id=current_user, id=wid).delete()

    return redirect('my_wishlist')


@login_required(login_url='login')
def notifications(request):
    current_user = request.user.id

    order_prod = OrderSummary.objects.filter(user_id=current_user)
    for prod in order_prod:
        order_n = prod.order_number
        order_item = prod.total_items
        order_status = prod.order_status
        order_st_dt = prod.order_status_date

        if Notification.objects.filter(user_id=current_user, order_number=order_n).exists():
            note = Notification.objects.filter(user_id=current_user, order_number=order_n).last()
            status = note.order_status
            if status != order_status:
                notice = Notification(user_id=current_user, order_number=order_n, total_items=order_item,
                                      order_status=order_status, order_status_date=order_st_dt)
                notice.save()
        else:
            notice = Notification(user_id=current_user, order_number=order_n, total_items=order_item,
                                  order_status=order_status, order_status_date=order_st_dt)
            notice.save()

    all_notice = []
    notices = Notification.objects.filter(user_id=current_user).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(notices, 7)
    try:
        notice_list = paginator.page(page)
    except PageNotAnInteger:
        notice_list = paginator.page(1)
    except EmptyPage:
        notice_list = paginator.page(paginator.num_pages)

    n = len(notice_list)
    all_notice.append([notice_list, range(1, n)])

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'notification': all_notice}
    return render(request, 'account/notifications.html', context)


def cancel(request, pid, on, ps, qty):
    current_user = request.user.id
    user_name = request.user.username

    cancel_order = OrderSummary.objects.filter(user_id=current_user, order_number=on).last()
    o_date = cancel_order.ordered_date
    today_date = datetime.now(timezone.utc)
    cancel_time = today_date - o_date
    cancel_expire = cancel_time.total_seconds()

    if cancel_expire < 7200:

        cancel_d = OrderDetail.objects.filter(customer_id=current_user, order_number=on, product_id=pid,
                                              product_size=ps,
                                              quantity=qty).first()
        cancel_p = cancel_d.amount
        cancel_r = cancel_d.refund
        prod_name = cancel_d.product_name
        prod_cat = cancel_d.caste_type
        prod_element = cancel_d.dress_type
        prod_image = cancel_d.prod_image

        cancel_update = OrderSummary.objects.filter(user_id=current_user, order_number=on).first()
        cancel_t_u = cancel_update.sub_total_amount
        cancel_rf_u = cancel_update.total_refund
        cancel_gt_u = cancel_update.grand_total
        cancel_item_u = cancel_update.total_items

        new_sub_total = cancel_t_u - cancel_p
        new_total_refund = cancel_rf_u - cancel_r
        new_grand_total = cancel_gt_u - cancel_p - cancel_r
        new_total_items = cancel_item_u - qty

        OrderSummary.objects.filter(user_id=current_user, order_number=on).update(sub_total_amount=new_sub_total,
                                                                                  total_refund=new_total_refund,
                                                                                  grand_total=new_grand_total,
                                                                                  total_items=new_total_items)

        cancel_prod = Product.objects.filter(id=pid).first()
        link = cancel_prod.slug
        if ps == 'S':
            prod_s = cancel_prod.stock_size_s
            prod_size_update = prod_s + qty
            Product.objects.filter(id=pid).update(stock_size_s=prod_size_update)
        if ps == 'M':
            prod_s = cancel_prod.stock_size_m
            prod_size_update = prod_s + qty
            Product.objects.filter(id=pid).update(stock_size_m=prod_size_update)
        if ps == 'L':
            prod_s = cancel_prod.stock_size_l
            prod_size_update = prod_s + qty
            Product.objects.filter(id=pid).update(stock_size_l=prod_size_update)
        if ps == 'XL':
            prod_s = cancel_prod.stock_size_xl
            prod_size_update = prod_s + qty
            Product.objects.filter(id=pid).update(stock_size_xl=prod_size_update)
        if ps == 'XXL':
            prod_s = cancel_prod.stock_size_xxl
            prod_size_update = prod_s + qty
            Product.objects.filter(id=pid).update(stock_size_xxl=prod_size_update)
        if ps == '3XL':
            prod_s = cancel_prod.stock_size_3xl
            prod_size_update = prod_s + qty
            Product.objects.filter(id=pid).update(stock_size_3xl=prod_size_update)

        cancel_record = Cancellation(user_id=current_user, user_name=user_name, product_name=prod_name, product_id=pid,
                                     product_link=link, product_category=prod_cat, product_dress_type=prod_element,
                                     image=prod_image)
        cancel_record.save()

        OrderDetail.objects.filter(customer_id=current_user, order_number=on, product_id=pid, product_size=ps,
                                   quantity=qty).delete()

        order_del = OrderSummary.objects.filter(user_id=current_user, order_number=on).first()
        total_items = order_del.total_items

        if total_items == 0:
            OrderSummary.objects.filter(user_id=current_user, order_number=on).delete()
        else:
            messages.info(request, 'Order Updated!')
    else:
        messages.info(request,
                      'Cancellation period has expired. You can only cancel order in 2hrs after order has placed.')

    return redirect('my_order')


@login_required(login_url='login')
def my_cancellations(request):
    current_user = request.user.id

    all_cancels = []
    cancels = Cancellation.objects.filter(user_id=current_user).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(cancels, 7)
    try:
        cancellation = paginator.page(page)
    except PageNotAnInteger:
        cancellation = paginator.page(1)
    except EmptyPage:
        cancellation = paginator.page(paginator.num_pages)

    n = len(cancellation)
    all_cancels.append([cancellation, range(1, n)])

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')

    context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women, 'all_cancels': all_cancels}
    return render(request, 'account/my_cancellation.html', context)


def products_display(request):
    current_user = request.user.id
    if 'filter_tradition' in request.session:
        filter_prod = request.session['filter_prod']
        filter_gender = request.session['filter_gender']
        filter_tradition = request.session['filter_tradition']

        products = []
        prod = Product.objects.filter(dress_type=filter_tradition, caste_category=filter_prod,
                                      person_category=filter_gender)
        page = request.GET.get('page', 1)
        paginator = Paginator(prod, 12)
        try:
            prods = paginator.page(page)
        except PageNotAnInteger:
            prods = paginator.page(1)
        except EmptyPage:
            prods = paginator.page(paginator.num_pages)

        n = len(prods)
        products.append([prods, range(1, n)])
    else:
        if 'filter_gender' in request.session:
            filter_prod = request.session['filter_prod']
            p = filter_prod.split(' ', 1)[0]
            print(p)
            filter_gender = request.session['filter_gender']
            filter_tradition = 'none'

            products = []
            prod = Product.objects.filter(dress_type=filter_prod, person_category=filter_gender).order_by(
                '-id')
            page = request.GET.get('page', 1)
            paginator = Paginator(prod, 12)
            try:
                prods = paginator.page(page)
            except PageNotAnInteger:
                prods = paginator.page(1)
            except EmptyPage:
                prods = paginator.page(paginator.num_pages)

            n = len(prods)
            products.append([prods, range(1, n)])
        else:
            if 'filter_prod' in request.session:
                filter_gender = 'none'
                filter_tradition = 'none'
                filter_prod = request.session['filter_prod']

                products = []
                prod = Product.objects.filter(person_category=filter_prod).order_by('-id')
                page = request.GET.get('page', 1)
                paginator = Paginator(prod, 12)
                try:
                    prods = paginator.page(page)
                except PageNotAnInteger:
                    prods = paginator.page(1)
                except EmptyPage:
                    prods = paginator.page(paginator.num_pages)

                n = len(prods)
                products.append([prods, range(1, n)])
            else:
                filter_gender = 'none'
                filter_prod = 'any category'
                filter_tradition = 'none'
                products = []
                prod = Product.objects.all().order_by('-id')
                page = request.GET.get('page', 1)
                paginator = Paginator(prod, 12)
                try:
                    prods = paginator.page(page)
                except PageNotAnInteger:
                    prods = paginator.page(1)
                except EmptyPage:
                    prods = paginator.page(paginator.num_pages)

                n = len(prods)
                products.append([prods, range(1, n)])

    cart_item = Cart.objects.filter(user_id=current_user).aggregate(Sum('quantity'))
    dress_men = Dresse.objects.filter(gender='men').order_by('id')
    dress_women = Dresse.objects.filter(gender='women').order_by('id')
    caste = Caste.objects.all().order_by('id')

    context = {'cart_item': cart_item, 'dress_men': dress_men, 'dress_women': dress_women,
               'filter_gender': filter_gender, 'filter_prod': filter_prod, 'products': products,
               'caste': caste, 'filter_tradition': filter_tradition}
    return render(request, 'shop/products.html', context)


def filter_product(request, fp):
    request.session['filter_prod'] = fp

    if 'filter_gender' in request.session:
        del request.session['filter_gender']
        request.session.modified = True

    if 'filter_tradition' in request.session:
        del request.session['filter_tradition']
        request.session.modified = True

    return redirect('products')


def filter_product_gender(request, fg, fp):
    request.session['filter_prod'] = fp
    request.session['filter_gender'] = fg

    if 'filter_tradition' in request.session:
        del request.session['filter_tradition']
        request.session.modified = True

    return redirect('products')


def filter_product_tradition(request, ft, fg, fp):
    request.session['filter_prod'] = fp
    request.session['filter_gender'] = fg
    request.session['filter_tradition'] = ft

    return redirect('products')


def rent_dress(request):
    if 'filter_prod' in request.session:
        del request.session['filter_prod']
        request.session.modified = True
    if 'filter_gender' in request.session:
        del request.session['filter_gender']
        request.session.modified = True
    if 'filter_tradition' in request.session:
        del request.session['filter_tradition']
        request.session.modified = True

    return redirect('products')

# thank = True
# ord_id = 0

# def checkout(request):
#     if request.method == "POST":
#         items_json = request.POST.get('itemsJson', '')
#         name = request.POST.get('name', '')
#         email = request.POST.get('email', '')
#         address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
#         city = request.POST.get('city', '')
#         state = request.POST.get('state', '')
#         zip_code = request.POST.get('zip_code', '')
#         phone = request.POST.get('phone', '')
#         order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
#                       state=state, zip_code=zip_code, phone=phone)
#         order.save()
#         global thank
#         thank = True
#         global ord_id
#         ord_id = order.id
#         return redirect('home')
#
#     return render(request, 'shop/checkout.html', {'thank': thank, 'ord_id': ord_id})
