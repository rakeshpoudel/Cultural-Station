import re
from abc import ABC
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Q, Func, Avg
from django.contrib import messages
from django.contrib.auth.models import User
from shop.models import Product, OrderDetail, Rating, OrderSummary, ProductQuery, Cancellation, Event


def log_dashboard(request):
	if request.user.is_staff:
		return redirect('dashboard')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				if user.is_staff:
					login(request, user)
					return redirect('dashboard')
				else:
					messages.info(request, 'Authentication Error')
			else:
				messages.info(request, 'Authentication Error')

	context = {}
	return render(request, 'log_dashboard.html', context)


def logout_dashboard(request):
	logout(request)
	return redirect('log_dashboard')


@login_required(login_url='log_dashboard')
def dashboard(request):
	if request.user.is_staff:
		event = Event.objects.last()
		e_post = event.event_posted
		e_day = event.event_days
		e_status = event.event_status
		expire_d = e_post + timedelta(days=e_day)
		expire_t = datetime.now().date()
		if expire_d == expire_t:
			expire = 1
		else:
			expire = 0

		products = Product.objects.all()
		prod_len = len(products)

		users = User.objects.all()
		user_len = len(users)

		reservation = OrderDetail.objects.all().exclude(order_status='Rental Returned')
		reservation_len = len(reservation)

		order_len = OrderDetail.objects.all().aggregate(Sum('quantity'))

		year = 2021
		if 'year' in request.session:
			year = request.session['year']

		prod_rent_len = OrderDetail.objects.filter(ordered_date__year=year).aggregate(Sum('quantity'))

		prod_men_jan_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=1).aggregate(Sum('quantity'))
		prod_women_jan_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=1).aggregate(Sum('quantity'))
		prod_women_feb_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=2).aggregate(Sum('quantity'))
		prod_men_feb_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=2).aggregate(Sum('quantity'))
		prod_men_mar_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=3).aggregate(Sum('quantity'))
		prod_women_mar_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=3).aggregate(Sum('quantity'))
		prod_women_apr_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=4).aggregate(Sum('quantity'))
		prod_men_apr_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=4).aggregate(Sum('quantity'))
		prod_women_may_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=5).aggregate(Sum('quantity'))
		prod_men_may_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=5).aggregate(Sum('quantity'))
		prod_men_jun_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=6).aggregate(Sum('quantity'))
		prod_women_jun_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=6).aggregate(Sum('quantity'))
		prod_women_jul_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=7).aggregate(Sum('quantity'))
		prod_men_jul_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=7).aggregate(Sum('quantity'))
		prod_men_aug_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=8).aggregate(Sum('quantity'))
		prod_women_aug_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=8).aggregate(Sum('quantity'))
		prod_women_sep_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=9).aggregate(Sum('quantity'))
		prod_men_sep_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=9).aggregate(Sum('quantity'))
		prod_men_oct_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=10).aggregate(Sum('quantity'))
		prod_women_oct_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=10).aggregate(Sum('quantity'))
		prod_women_nov_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=11).aggregate(Sum('quantity'))
		prod_men_nov_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=11).aggregate(Sum('quantity'))
		prod_men_dec_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=12).aggregate(Sum('quantity'))
		prod_women_dec_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=12).aggregate(Sum('quantity'))

		last_month = datetime.today() - timedelta(days=30)
		recent_reviews = Rating.objects.filter(posted_date__gte=last_month).exclude(review='').order_by('-id')
		recent_queries = ProductQuery.objects.filter(publish_date__gte=last_month).order_by('-id')

		recent_order = OrderSummary.objects.filter(ordered_date__gte=last_month, order_status='Returned').order_by('-id')

		noti_order = OrderSummary.objects.all().exclude(check_status='not checked').order_by('-id')
		noti_review = Rating.objects.all().exclude(Q(review='') | Q(check_status='not checked')).order_by('-id')
		noti_query = ProductQuery.objects.all().exclude(answer='').order_by('-id')
		zip_noti =zip(noti_review, noti_query)
		ll = len(list(zip_noti))
		zip_noti =zip(noti_review, noti_query)

		noti_check_order = OrderSummary.objects.filter(check_status='not checked').order_by('-id')
		noti_check_review = Rating.objects.filter(check_status='not checked').exclude(review='').order_by('-id')
		noti_check_query = ProductQuery.objects.filter(answer='').order_by('-id')

		noti_order_count = OrderSummary.objects.filter(check_status='not checked').count()
		noti_review_count = Rating.objects.filter(check_status='not checked').exclude(review='').count()
		noti_query_count = ProductQuery.objects.filter(answer='').count()
		total_noti = noti_review_count + noti_query_count

		context = {
					'prod_len': prod_len, 'user_len': user_len, 'reservation_len': reservation_len, 'order_len': order_len, 'prod_rent_len': prod_rent_len,
					'prod_men_jan_len': prod_men_jan_len, 'prod_women_jan_len': prod_women_jan_len, 'prod_men_feb_len': prod_men_feb_len, 'prod_women_feb_len': prod_women_feb_len,
					'prod_men_mar_len': prod_men_mar_len, 'prod_women_mar_len': prod_women_mar_len, 'prod_men_apr_len': prod_men_apr_len, 'prod_women_apr_len': prod_women_apr_len,
					'prod_men_may_len': prod_men_may_len, 'prod_women_may_len': prod_women_may_len, 'prod_men_jun_len': prod_men_jun_len, 'prod_women_jun_len': prod_women_jun_len,
					'prod_men_jul_len': prod_men_jul_len, 'prod_women_jul_len': prod_women_jul_len, 'prod_men_aug_len': prod_men_aug_len, 'prod_women_aug_len': prod_women_aug_len,
					'prod_men_sep_len': prod_men_sep_len, 'prod_women_sep_len': prod_women_sep_len, 'prod_men_oct_len': prod_men_oct_len, 'prod_women_oct_len': prod_women_oct_len,
					'prod_men_nov_len': prod_men_nov_len, 'prod_women_nov_len': prod_women_nov_len, 'prod_men_dec_len': prod_men_dec_len, 'prod_women_dec_len': prod_women_dec_len,
					'recent_reviews': recent_reviews, 'recent_queries': recent_queries, 'recent_order': recent_order, 'noti_order': noti_order, 'noti_review': noti_review, 'noti_query': noti_query, 
					'zip_noti': zip_noti, 'noti_check_review': noti_check_review, 'noti_check_query': noti_check_query, 'noti_check_order': noti_check_order, 'll': ll, 
					'noti_order_count': noti_order_count, 'total_noti': total_noti, 'event': event, 'expire': expire, 'e_status': e_status, 'year': year
				}
		return render(request, 'dashboard.html', context)
	else:
		return redirect('log_dashboard')


def year_change(request, yr):
	request.session['year'] = yr
	return redirect('dashboard')


def prod_rent_refresh(request):
	year = 2021
	if 'year' in request.session:
		year = request.session['year']

	prod_rent_len = OrderDetail.objects.filter(ordered_date__year=year).aggregate(Sum('quantity'))

	prod_men_jan_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=1).aggregate(Sum('quantity'))
	prod_women_jan_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=1).aggregate(Sum('quantity'))
	prod_women_feb_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=2).aggregate(Sum('quantity'))
	prod_men_feb_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=2).aggregate(Sum('quantity'))
	prod_men_mar_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=3).aggregate(Sum('quantity'))
	prod_women_mar_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=3).aggregate(Sum('quantity'))
	prod_women_apr_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=4).aggregate(Sum('quantity'))
	prod_men_apr_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=4).aggregate(Sum('quantity'))
	prod_women_may_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=5).aggregate(Sum('quantity'))
	prod_men_may_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=5).aggregate(Sum('quantity'))
	prod_men_jun_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=6).aggregate(Sum('quantity'))
	prod_women_jun_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=6).aggregate(Sum('quantity'))
	prod_women_jul_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=7).aggregate(Sum('quantity'))
	prod_men_jul_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=7).aggregate(Sum('quantity'))
	prod_men_aug_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=8).aggregate(Sum('quantity'))
	prod_women_aug_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=8).aggregate(Sum('quantity'))
	prod_women_sep_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=9).aggregate(Sum('quantity'))
	prod_men_sep_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=9).aggregate(Sum('quantity'))
	prod_men_oct_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=10).aggregate(Sum('quantity'))
	prod_women_oct_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=10).aggregate(Sum('quantity'))
	prod_women_nov_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=11).aggregate(Sum('quantity'))
	prod_men_nov_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=11).aggregate(Sum('quantity'))
	prod_men_dec_len = OrderDetail.objects.filter(gender='men', ordered_date__year=year, ordered_date__month=12).aggregate(Sum('quantity'))
	prod_women_dec_len = OrderDetail.objects.filter(gender='women', ordered_date__year=year, ordered_date__month=12).aggregate(Sum('quantity'))

	context = {
				'prod_rent_len': prod_rent_len,
				'prod_men_jan_len': prod_men_jan_len, 'prod_women_jan_len': prod_women_jan_len, 'prod_men_feb_len': prod_men_feb_len, 'prod_women_feb_len': prod_women_feb_len,
				'prod_men_mar_len': prod_men_mar_len, 'prod_women_mar_len': prod_women_mar_len, 'prod_men_apr_len': prod_men_apr_len, 'prod_women_apr_len': prod_women_apr_len,
				'prod_men_may_len': prod_men_may_len, 'prod_women_may_len': prod_women_may_len, 'prod_men_jun_len': prod_men_jun_len, 'prod_women_jun_len': prod_women_jun_len,
				'prod_men_jul_len': prod_men_jul_len, 'prod_women_jul_len': prod_women_jul_len, 'prod_men_aug_len': prod_men_aug_len, 'prod_women_aug_len': prod_women_aug_len,
				'prod_men_sep_len': prod_men_sep_len, 'prod_women_sep_len': prod_women_sep_len, 'prod_men_oct_len': prod_men_oct_len, 'prod_women_oct_len': prod_women_oct_len,
				'prod_men_nov_len': prod_men_nov_len, 'prod_women_nov_len': prod_women_nov_len, 'prod_men_dec_len': prod_men_dec_len, 'prod_women_dec_len': prod_women_dec_len,
			}
	return render(request, 'dash/p_rent.html', context)


def review_refresh(request):
	last_month = datetime.today() - timedelta(days=30)
	recent_reviews = Rating.objects.filter(posted_date__gte=last_month).exclude(review='').order_by('-id')

	context = {
				'recent_reviews': recent_reviews,
			}
	return render(request, 'dash/review_refresh.html', context)


def query_refresh(request):
	last_month = datetime.today() - timedelta(days=30)
	recent_queries = ProductQuery.objects.filter(publish_date__gte=last_month).order_by('-id')

	context = {
				'recent_queries': recent_queries,
			}
	return render(request, 'dash/query_refresh.html', context)


def order_refresh(request):
	last_month = datetime.today() - timedelta(days=30)

	recent_order = OrderSummary.objects.filter(ordered_date__gte=last_month).order_by('-id')

	context = {
				'recent_order': recent_order,
			}
	return render(request, 'dash/order_refresh.html', context)


def message_notification(request):
	noti_review = Rating.objects.all().exclude(Q(review='') | Q(check_status='not checked')).order_by('-id')
	noti_query = ProductQuery.objects.all().exclude(answer='').order_by('-id')
	zip_noti =zip(noti_review, noti_query)
	ll = len(list(zip_noti))
	zip_noti =zip(noti_review, noti_query)

	noti_check_review = Rating.objects.filter(check_status='not checked').exclude(review='').order_by('-id')
	noti_check_query = ProductQuery.objects.filter(answer='').order_by('-id')

	noti_review_count = Rating.objects.filter(check_status='not checked').exclude(review='').count()
	noti_query_count = ProductQuery.objects.filter(answer='').count()
	total_noti = noti_review_count + noti_query_count

	context = { 
				'noti_review': noti_review, 'noti_query': noti_query, 
				'zip_noti': zip_noti, 'noti_check_review': noti_check_review, 'noti_check_query': noti_check_query, 'll': ll,
				'noti_review_count': noti_review_count,
				'noti_query_count': noti_query_count,
				'total_noti': total_noti
			}
	return render(request, 'dash/message_notification.html', context)


def m_notification(request):
	noti_review = Rating.objects.all().exclude(Q(review='') | Q(check_status='not checked')).order_by('-id')
	noti_query = ProductQuery.objects.all().exclude(answer='').order_by('-id')
	zip_noti =zip(noti_review, noti_query)
	ll = len(list(zip_noti))
	zip_noti =zip(noti_review, noti_query)

	noti_check_review = Rating.objects.filter(check_status='not checked').exclude(review='').order_by('-id')
	noti_check_query = ProductQuery.objects.filter(answer='').order_by('-id')

	noti_review_count = Rating.objects.filter(check_status='not checked').exclude(review='').count()
	noti_query_count = ProductQuery.objects.filter(answer='').count()
	total_noti = noti_review_count + noti_query_count

	context = { 
				'noti_review': noti_review, 'noti_query': noti_query, 
				'zip_noti': zip_noti, 'noti_check_review': noti_check_review, 'noti_check_query': noti_check_query, 'll': ll,
				'noti_review_count': noti_review_count,
				'noti_query_count': noti_query_count,
				'total_noti': total_noti
			}
	return render(request, 'dash/m_notification.html', context)


def order_notification(request):
	noti_order = OrderSummary.objects.all().exclude(check_status='not checked').order_by('-id')
	noti_order_count = OrderSummary.objects.filter(check_status='not checked').count()

	noti_check_order = OrderSummary.objects.filter(check_status='not checked').order_by('-id')

	context = {
				'noti_check_order': noti_check_order, 'noti_order_count': noti_order_count, 'noti_order': noti_order, 
			}
	return render(request, 'dash/order_notification.html', context)


def o_notification(request):
	noti_order = OrderSummary.objects.all().exclude(check_status='not checked').order_by('-id')
	noti_order_count = OrderSummary.objects.filter(check_status='not checked').count()

	noti_check_order = OrderSummary.objects.filter(check_status='not checked').order_by('-id')

	context = {
				'noti_check_order': noti_check_order, 'noti_order_count': noti_order_count, 'noti_order': noti_order, 
			}
	return render(request, 'dash/o_notification.html', context)


def order_noti_count(request):
	noti_order_count = OrderSummary.objects.filter(check_status='not checked').count()

	context = {
				'noti_order_count': noti_order_count
			}
	return render(request, 'dash/order_noti_count.html', context)


def message_noti_count(request):
	noti_review_count = Rating.objects.filter(check_status='not checked').exclude(review='').count()
	noti_query_count = ProductQuery.objects.filter(answer='').count()
	total_noti = noti_review_count + noti_query_count

	context = {
				'total_noti': total_noti
			}
	return render(request, 'dash/message_noti_count.html', context)


@login_required(login_url='log_dashboard')
def order_dashboard(request):
	if request.user.is_staff:
		last_month = datetime.today() - timedelta(days=30)
		order_processing = OrderSummary.objects.all().exclude(Q(order_status='Returned') | Q(check_status='not checked')).order_by('-id')
		new_orders = OrderSummary.objects.filter(check_status='not checked').order_by('-id')

		all_order_details = []
		order_prod = OrderDetail.objects.values('order_number')
		orders = {item['order_number'] for item in order_prod}
		for o in orders:
			order_list = OrderDetail.objects.filter(order_number=o).order_by('-id')
			order_list_sum = OrderSummary.objects.filter(order_number=o).order_by('-id')
			n = len(order_list)
			all_order_details.append([order_list, order_list_sum, range(1, n)])

		recent_order = OrderSummary.objects.filter(ordered_date__gte=last_month, order_status='Returned').exclude(check_status='not checked').order_by('-id')
		cancels = Cancellation.objects.all().order_by('-id')
		recent_returns = OrderDetail.objects.filter(order_status='Rental Returned', order_status_date__gte=last_month).order_by('-id')
		order_history = OrderSummary.objects.filter(order_status='Returned').exclude(Q(check_status='not checked') | Q(ordered_date__gte=last_month)).order_by('-id')

		noti_order = OrderSummary.objects.all().exclude(check_status='not checked').order_by('-id')
		noti_review = Rating.objects.all().exclude(Q(review='') | Q(check_status='not checked')).order_by('-id')
		noti_query = ProductQuery.objects.all().exclude(answer='').order_by('-id')
		zip_noti =zip(noti_review, noti_query)
		ll = len(list(zip_noti))
		zip_noti =zip(noti_review, noti_query)

		noti_check_order = OrderSummary.objects.filter(check_status='not checked').order_by('-id')
		noti_check_review = Rating.objects.filter(check_status='not checked').exclude(review='').order_by('-id')
		noti_check_query = ProductQuery.objects.filter(answer='').order_by('-id')

		noti_order_count = OrderSummary.objects.filter(check_status='not checked').count()
		noti_review_count = Rating.objects.filter(check_status='not checked').exclude(review='').count()
		noti_query_count = ProductQuery.objects.filter(answer='').count()
		total_noti = noti_review_count + noti_query_count

		context = {
					'noti_order': noti_order, 'noti_review': noti_review, 'noti_query': noti_query, 
					'zip_noti': zip_noti, 'noti_check_review': noti_check_review, 'noti_check_query': noti_check_query, 'noti_check_order': noti_check_order, 'll': ll, 
					'noti_order_count': noti_order_count, 'total_noti': total_noti, 
					'order_processing': order_processing, 'all_order_details': all_order_details, 'recent_order': recent_order, 'cancels':cancels, 'recent_returns':recent_returns,
					'order_history': order_history, 'new_orders': new_orders,
				}
		return render(request, 'order_dashboard.html', context)
	else:
		return redirect('log_dashboard')


def search_order(request):
	ctx = {}
	query = request.GET.get('q')

	if query:
		lookups = Q(order_number__icontains=query) | Q(user_name__icontains=query) | Q(user_full_name__icontains=query) | Q(user_email__icontains=query)| Q(user_contact__icontains=query)
		prodquery = OrderSummary.objects.filter(lookups).exclude(order_status='Returned').distinct()
	else:
		prodquery = ''

	ctx["prodquery"] = prodquery

	if request.is_ajax():
		html = render_to_string(
				template_name = "dash/order_result.html",
				context = {"prodquery":prodquery}
			)

		data_dict = {"html_from_view": html}

		return JsonResponse(data=data_dict, safe=False)


def search_order_complete(request):
	ctx = {}
	query = request.GET.get('q')

	if query:
		lookups = Q(order_number__icontains=query) | Q(user_name__icontains=query) | Q(user_full_name__icontains=query) | Q(user_email__icontains=query)| Q(user_contact__icontains=query)
		prodquery = OrderSummary.objects.filter(Q(order_status='Returned'), lookups).distinct()
	else:
		prodquery = ''

	ctx["prodquery"] = prodquery

	if request.is_ajax():
		html = render_to_string(
				template_name = "dash/order_result.html",
				context = {"prodquery":prodquery}
			)

		data_dict = {"html_from_view": html}

		return JsonResponse(data=data_dict, safe=False)

def order_detail(request):
	all_order_details = []
	order_prod = OrderDetail.objects.values('order_number')
	orders = {item['order_number'] for item in order_prod}
	for o in orders:
		order_list = OrderDetail.objects.filter(order_number=o).order_by('-id')
		order_list_sum = OrderSummary.objects.filter(order_number=o).order_by('-id')
		n = len(order_list)
		all_order_details.append([order_list, order_list_sum, range(1, n)])

	on = 0
	if 'on' in request.session:
		on = request.session['on']
		del request.session['on']
		request.session.modified = True
	error = ''
	if 'error' in request.session:
		error = request.session['error']
		del request.session['error']
		request.session.modified = True

	context = {
				'all_order_details': all_order_details, 'on': on, 'error':error
			}
	return render(request, 'dash/order_detail.html', context)


def rental_update(request, on, pid, ps):
	status = request.POST.get('status')
	qty = request.POST.get('qty')
	today = datetime.today()
	OrderDetail.objects.filter(order_number=on, product_id=pid, product_size=ps).update(order_status=status, order_status_date=today)
	request.session['on'] = on
	prod = Product.objects.filter(id=pid).first()
	if ps=='S':
		size = prod.stock_size_s + int(qty)
		Product.objects.filter(id=pid).update(stock_size_s=size)
	if ps=='M':
		size = prod.stock_size_m + int(qty)
		Product.objects.filter(id=pid).update(stock_size_m=size)
	if ps=='L':
		size = prod.stock_size_l + int(qty)
		Product.objects.filter(id=pid).update(stock_size_l=size)
	if ps=='XL':
		size = prod.stock_size_xl + int(qty)
		Product.objects.filter(id=pid).update(stock_size_xl=size)
	if ps=='XXL':
		size = prod.stock_size_xxl + int(qty)
		Product.objects.filter(id=pid).update(stock_size_xxl=size)
	if ps=='3XL':
		size = prod.stock_size_3xl + int(qty)
		Product.objects.filter(id=pid).update(stock_size_3xl=size)

	return HttpResponse()


def order_update(request, on):
	status = request.POST.get('status')
	today = datetime.today()
	if status == 'Returned':
		count = 0
		orders = OrderDetail.objects.filter(order_number=on)
		for o in orders:
			stat = o.order_status
			if stat == 'Rental Reserved':
				count = 1;
		if count == 0:
			OrderSummary.objects.filter(order_number=on).update(order_status=status, order_status_date=today)
		else:
			error = 'Failed, your rental(s) are still reserved'
			request.session['error'] = error
	else:
		if status == 'Delivered':
			orders = OrderDetail.objects.filter(order_number=on)
			for o in orders:
				stat = o.payment_status
				if stat == 'Pending':
					OrderDetail.objects.filter(order_number=on).update(payment_status='Paid')

			os = OrderSummary.objects.filter(order_number=on).first()
			stat = os.payment_status
			if stat == 'Pending':
				OrderSummary.objects.filter(order_number=on).update(order_status=status, order_status_date=today, payment_status='Paid')
			else:
				OrderSummary.objects.filter(order_number=on).update(order_status=status, order_status_date=today)
		else:
			OrderSummary.objects.filter(order_number=on).update(order_status=status, order_status_date=today)
	request.session['on'] = on

	return HttpResponse()


def processing_order(request):
	order_processing = OrderSummary.objects.all().exclude(Q(order_status='Returned') | Q(check_status='not checked')).order_by('-id')
	new_orders = OrderSummary.objects.filter(check_status='not checked').order_by('-id')

	context = {
				'order_processing': order_processing,
				'new_orders': new_orders,
			}
	return render(request, 'dash/processing_order.html', context)


def recent_order_dash(request):
	last_month = datetime.today() - timedelta(days=30)
	recent_order = OrderSummary.objects.filter(ordered_date__gte=last_month, order_status='Returned').exclude(check_status='not checked').order_by('-id')

	context = {
				'recent_order': recent_order,
			}
	return render(request, 'dash/recent_order_dash.html', context)


def recent_returns(request):
	last_month = datetime.today() - timedelta(days=30)
	recent_returns = OrderDetail.objects.filter(order_status='Rental Returned', order_status_date__gte=last_month).order_by('-id')

	context = {
				'recent_returns': recent_returns,
			}
	return render(request, 'dash/recent_returns.html', context)


def cancel_refresh(request):
	cancels = Cancellation.objects.all().order_by('-id')

	context = {
				'cancels': cancels,
			}
	return render(request, 'dash/cancel_refresh.html', context)


def history_refresh(request):
	last_month = datetime.today() - timedelta(days=30)
	order_history = OrderSummary.objects.filter(order_status='Returned').exclude(Q(check_status='not checked') | Q(ordered_date__gte=last_month)).order_by('-id')

	context = {
				'order_history': order_history,
			}
	return render(request, 'dash/history_refresh.html', context)


def check_status(request, on):
	check = request.POST.get('check')
	OrderSummary.objects.filter(order_number=on).update(check_status=check)

	return HttpResponse()



def review_cal(review):
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
	review = review
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

	return rate


class Round(Func, ABC):
    function = 'ROUND'
    arity = 2


@login_required(login_url='log_dashboard')
def review_dashboard(request):
	if request.user.is_staff:
		if Rating.objects.filter(check_status='not checked').exclude(review='').exists():
			Rating.objects.filter(check_status='not checked').exclude(review='').update(check_status='checked')

		last_month = datetime.today() - timedelta(days=30)
		recent_reviews = Rating.objects.filter(posted_date__gte=last_month).exclude(review='').order_by('-id')
		all_reviews= []
		rr = Rating.objects.all().exclude(review='').order_by('-id')
		nr = len(rr)
		all_reviews.append([rr, range(1, nr)])
		review_count = Rating.objects.all()
		all_prods = Product.objects.all().order_by('-id')
		review_rates = []
		for r in rr:
			review = r.review
			ids = r.id
			r_cal = review_cal(review)
			review_rates.append([r_cal, ids])
		rid = []
		avg_rating = []
		ent = Rating.objects.values_list('product_id', flat=True).distinct()
		for r in ent:
			rrid = r
			rating = Rating.objects.filter(product_id=r).aggregate(average_rates=Round(Avg('ratings'), 1))
			avg_rating.append([rating, rrid])
		print(avg_rating)

		noti_order = OrderSummary.objects.all().exclude(check_status='not checked').order_by('-id')
		noti_review = Rating.objects.all().exclude(Q(review='') | Q(check_status='not checked')).order_by('-id')
		noti_query = ProductQuery.objects.all().exclude(answer='').order_by('-id')
		zip_noti =zip(noti_review, noti_query)
		ll = len(list(zip_noti))
		zip_noti =zip(noti_review, noti_query)

		noti_check_order = OrderSummary.objects.filter(check_status='not checked').order_by('-id')
		noti_check_review = Rating.objects.filter(check_status='not checked').exclude(review='').order_by('-id')
		noti_check_query = ProductQuery.objects.filter(answer='').order_by('-id')

		noti_order_count = OrderSummary.objects.filter(check_status='not checked').count()
		noti_review_count = Rating.objects.filter(check_status='not checked').exclude(review='').count()
		noti_query_count = ProductQuery.objects.filter(answer='').count()
		total_noti = noti_review_count + noti_query_count

		context = {
					'noti_order': noti_order, 'noti_review': noti_review, 'noti_query': noti_query, 
					'zip_noti': zip_noti, 'noti_check_review': noti_check_review, 'noti_check_query': noti_check_query, 'noti_check_order': noti_check_order, 'll': ll, 
					'noti_order_count': noti_order_count, 'total_noti': total_noti, 
					'recent_reviews': recent_reviews, 'all_reviews': all_reviews, 'all_prods': all_prods, 'review_rates': review_rates, 'avg_rating': avg_rating
				}
		return render(request, 'review_dashboard.html', context)
	else:
		return redirect('log_dashboard')


@login_required(login_url='log_dashboard')
def query_dashboard(request):
	if request.user.is_staff:
		last_month = datetime.today() - timedelta(days=30)
		recent_queries = ProductQuery.objects.filter(publish_date__gte=last_month).exclude(answer='').order_by('-id')
		all_queries_front = ProductQuery.objects.all().exclude(answer='').order_by('-id') 
		all_queries = ProductQuery.objects.all().order_by('-id') 
		all_prods = Product.objects.all().order_by('-id')
		not_ans_query = ProductQuery.objects.filter(answer='').order_by('-id') 

		noti_order = OrderSummary.objects.all().exclude(check_status='not checked').order_by('-id')
		noti_review = Rating.objects.all().exclude(Q(review='') | Q(check_status='not checked')).order_by('-id')
		noti_query = ProductQuery.objects.all().exclude(answer='').order_by('-id')
		zip_noti =zip(noti_review, noti_query)
		ll = len(list(zip_noti))
		zip_noti =zip(noti_review, noti_query)

		noti_check_order = OrderSummary.objects.filter(check_status='not checked').order_by('-id')
		noti_check_review = Rating.objects.filter(check_status='not checked').exclude(review='').order_by('-id')
		noti_check_query = ProductQuery.objects.filter(answer='').order_by('-id')

		noti_order_count = OrderSummary.objects.filter(check_status='not checked').count()
		noti_review_count = Rating.objects.filter(check_status='not checked').exclude(review='').count()
		noti_query_count = ProductQuery.objects.filter(answer='').count()
		total_noti = noti_review_count + noti_query_count

		context = {
					'noti_order': noti_order, 'noti_review': noti_review, 'noti_query': noti_query, 
					'zip_noti': zip_noti, 'noti_check_review': noti_check_review, 'noti_check_query': noti_check_query, 'noti_check_order': noti_check_order, 'll': ll, 
					'noti_order_count': noti_order_count, 'total_noti': total_noti, 
					'recent_queries': recent_queries, 'all_queries': all_queries, 'all_prods': all_prods, 'not_ans_query': not_ans_query, 'all_queries_front': all_queries_front
				}
		return render(request, 'query_dashboard.html', context)
	else:
		return redirect('log_dashboard')


def recent_query_dash(request):
	last_month = datetime.today() - timedelta(days=30)
	recent_queries = ProductQuery.objects.filter(publish_date__gte=last_month).exclude(answer='').order_by('-id')
	not_ans_query = ProductQuery.objects.filter(answer='').order_by('-id') 

	context = {
				'recent_queries': recent_queries,
				'not_ans_query': not_ans_query
			}
	return render(request, 'dash/recent_query_dash.html', context)


def query_dash(request):
	all_queries_front = ProductQuery.objects.all().exclude(answer='').order_by('-id') 

	context = {
				'all_queries_front': all_queries_front,
			}
	return render(request, 'dash/query_dash.html', context)


def query_filter(request):
	all_queries = ProductQuery.objects.all().order_by('-id') 

	context = {
				'all_queries': all_queries,
			}
	return render(request, 'dash/query_filter.html', context)


def recent_review_dash(request):
	last_month = datetime.today() - timedelta(days=30)
	recent_reviews = Rating.objects.filter(posted_date__gte=last_month).exclude(review='').order_by('-id')

	context = {
				'recent_reviews': recent_reviews,
			}
	return render(request, 'dash/recent_reveiw_dash.html', context)


def review_dash(request):
	all_reviews = Rating.objects.all().exclude(review='').order_by('-id') 

	context = {
				'all_reviews': all_reviews,
			}
	return render(request, 'dash/reveiw_dash.html', context)


def review_filter(request):
	all_reviews = Rating.objects.all().exclude(review='').order_by('-id') 

	context = {
				'all_reviews': all_reviews,
			}
	return render(request, 'dash/review_filter.html', context)


def answer_update(request, rid):
	answer = request.POST.get('answer')
	ProductQuery.objects.filter(id=rid).update(answer=answer)

	return HttpResponse()


@login_required(login_url='log_dashboard')
def event_dashboard(request):
	if request.user.is_staff:
		event = Event.objects.last()
		e_post = event.event_posted
		e_day = event.event_days
		e_status = event.event_status
		expire_d = e_post + timedelta(days=e_day)
		expire_t = datetime.now().date()
		print(expire_d)
		print(expire_t)
		if expire_d <= expire_t:
			expire = 1
		else:
			expire = 0

		noti_order = OrderSummary.objects.all().exclude(check_status='not checked').order_by('-id')
		noti_review = Rating.objects.all().exclude(Q(review='') | Q(check_status='not checked')).order_by('-id')
		noti_query = ProductQuery.objects.all().exclude(answer='').order_by('-id')
		zip_noti =zip(noti_review, noti_query)
		ll = len(list(zip_noti))
		zip_noti =zip(noti_review, noti_query)

		noti_check_order = OrderSummary.objects.filter(check_status='not checked').order_by('-id')
		noti_check_review = Rating.objects.filter(check_status='not checked').exclude(review='').order_by('-id')
		noti_check_query = ProductQuery.objects.filter(answer='').order_by('-id')

		noti_order_count = OrderSummary.objects.filter(check_status='not checked').count()
		noti_review_count = Rating.objects.filter(check_status='not checked').exclude(review='').count()
		noti_query_count = ProductQuery.objects.filter(answer='').count()
		total_noti = noti_review_count + noti_query_count

		context = {
					'noti_order': noti_order, 'noti_review': noti_review, 'noti_query': noti_query, 
					'zip_noti': zip_noti, 'noti_check_review': noti_check_review, 'noti_check_query': noti_check_query, 'noti_check_order': noti_check_order, 'll': ll, 
					'noti_order_count': noti_order_count, 'total_noti': total_noti, 
					'event': event, 'expire': expire, 'expire_d': expire_d, 'event_status': e_status,
				}
		return render(request, 'event_dashboard.html', context)
	else:
		return redirect('log_dashboard')


def event_update(request):
	if request.method == "POST":
		text = request.POST.get('etext')
		days = request.POST.get('eday')
		image = request.FILES.get('eimage')
		if text != '':
			if days != '':
				if image != '' and image is not None:
					event = Event(event_text=text, event_days=days, event_status='active', event_image=image)
					event.save()
					
				else:
					messages.info(request, 'Please select event image!')
			else:
				messages.info(request, 'Please provide event active days!')
		else:
			messages.info(request, 'Please provide event text!')

	return redirect('event_dashboard')


def active_event(request, idx, day):
	today = datetime.now().date()
	Event.objects.filter(id=idx).update(event_days=day, event_posted=today, event_status='active')

	return redirect('event_dashboard')


def deactive_event(request, idx):
	Event.objects.filter(id=idx).update(event_status='inactive')

	return redirect('event_dashboard')


@login_required(login_url='log_dashboard')
def stock_dashboard(request):
	if request.user.is_staff:

		last_month = datetime.today() - timedelta(days=30)
		all_prods = Product.objects.all().order_by('-id')

		noti_order = OrderSummary.objects.all().exclude(check_status='not checked').order_by('-id')
		noti_review = Rating.objects.all().exclude(Q(review='') | Q(check_status='not checked')).order_by('-id')
		noti_query = ProductQuery.objects.all().exclude(answer='').order_by('-id')
		zip_noti =zip(noti_review, noti_query)
		ll = len(list(zip_noti))
		zip_noti =zip(noti_review, noti_query)

		noti_check_order = OrderSummary.objects.filter(check_status='not checked').order_by('-id')
		noti_check_review = Rating.objects.filter(check_status='not checked').exclude(review='').order_by('-id')
		noti_check_query = ProductQuery.objects.filter(answer='').order_by('-id')

		noti_order_count = OrderSummary.objects.filter(check_status='not checked').count()
		noti_review_count = Rating.objects.filter(check_status='not checked').exclude(review='').count()
		noti_query_count = ProductQuery.objects.filter(answer='').count()
		total_noti = noti_review_count + noti_query_count

		prod = Product.objects.all()
		prodids = []
		for p in prod:
			pid = p.id
			stock1 = p.stock_size_s
			stock2 = p.stock_size_m
			stock3 = p.stock_size_l
			stock4 = p.stock_size_xl
			stock5 = p.stock_size_xxl
			stock6 = p.stock_size_3xl

			if stock1 <= 5: 
				prodids.append(pid)
			if stock2 <= 5: 
				prodids.append(pid)
			if stock3 <= 5: 
				prodids.append(pid)
			if stock4 <= 5: 
				prodids.append(pid)
			if stock5 <= 5: 
				prodids.append(pid)
			if stock6 <= 5: 
				prodids.append(pid)
		prodids = list(set(prodids))
		stock_prod = Product.objects.filter(id__in=prodids).order_by('-id')
		session_prod = []
		if 'stockid' in request.session:
			stid = request.session['stockid']
			session_prod = Product.objects.filter(id=stid).first()

			del request.session['stockid']
			request.session.modified = True

		context = {
					'noti_order': noti_order, 'noti_review': noti_review, 'noti_query': noti_query, 
					'zip_noti': zip_noti, 'noti_check_review': noti_check_review, 'noti_check_query': noti_check_query, 'noti_check_order': noti_check_order, 'll': ll, 
					'noti_order_count': noti_order_count, 'total_noti': total_noti,'all_prods': all_prods, 'stock_prod': stock_prod, 'sprod': session_prod
				}
		return render(request, 'stock_dashboard.html', context)
	else:
		return redirect('log_dashboard')


def search_stock(request):
	ctx = {}
	query = request.GET.get('q')

	if query:
		lookups = Q(name__icontains=query) | Q(dress_type__dress__icontains=query) | Q(designer__designer__icontains=query) | Q(element_category__icontains=query)
		prodquery = Product.objects.filter(lookups).distinct()
	else:
		prodquery = Product.objects.all().order_by('-id')

	ctx["prodquery"] = prodquery

	if request.is_ajax():
		html = render_to_string(
				template_name = "dash/stock_result.html",
				context = {"prodquery":prodquery}
			)

		data_dict = {"html_from_view": html}

		return JsonResponse(data=data_dict, safe=False)


def stock_session(request, idx):
	request.session['stockid'] = idx

	return redirect('stock_dashboard')


def stock_update(request):
	if request.method == "POST":
		pid = request.POST.get('pid')
		if request.POST.get('stocks') != '' and request.POST.get('stockm') != '' and request.POST.get('stockl') != '' and request.POST.get('stockxl') != '' and request.POST.get('stockxxl') != '' and request.POST.get('stock3xl') != '':
			stock1 = int(request.POST.get('stocks'))
			stock2 = int(request.POST.get('stockm'))
			stock3 = int(request.POST.get('stockl'))
			stock4 = int(request.POST.get('stockxl'))
			stock5 = int(request.POST.get('stockxxl'))
			stock6 = int(request.POST.get('stock3xl'))
			if stock1 >= 0 and stock2 >= 0 and stock3 >= 0 and stock4 >= 0 and stock5 >= 0 and stock6 >= 0:
				Product.objects.filter(id=pid).update(stock_size_s=stock1, stock_size_m=stock2, stock_size_l=stock3, stock_size_xl=stock4, stock_size_xxl=stock5, stock_size_3xl=stock6)
				messages.info(request, 'Stock updated Successfully')
				request.session['stockid'] = pid
			else:
				messages.info(request, 'Error! Request with invalid stock values')
				request.session['stockid'] = pid
		else:
			messages.info(request, 'Error! Request with invalid stock values')
			request.session['stockid'] = pid

		return redirect('stock_dashboard')
	else:
		return redirect('log_dashboard')