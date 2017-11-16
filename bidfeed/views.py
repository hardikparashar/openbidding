
#BID VALIDATION ON LINE 44
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from datetime import datetime, timedelta
from .forms import ProductForm, BidForm, UserForm
from .models import Product, Bid
from django.conf import settings
import csv
from django.core.files.storage import FileSystemStorage
import pytz

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_product(request):
	if not request.user.is_authenticated():
		return render(request, 'bidfeed/login.html')	
	else:
		form = ProductForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			product = form.save(commit=False)
			product.user = request.user
			product.product_image = request.FILES['product_image']
			product.end_date = datetime.now() + timedelta(days=product.days)
			product.rem_days = product.days
			product.product_name = form.cleaned_data.get("product_name").upper()
			time1 = datetime.now()
			tz = pytz.timezone('Asia/Kolkata')
			time1 = tz.localize(time1)
			product.end_date = tz.localize(product.end_date)
			product.rem_days = (product.end_date - time1)
			product.rem_days = product.rem_days.total_seconds()
			if product.rem_days < 1:
				product.status = 'sold'
			file_type = product.product_image.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMAGE_FILE_TYPES:
				context={
					'product': product,
					'form': form,
					'error_message': 'Image file must be PNG, JPG, or JPEG',
				}
				return render(request, 'bidfeed/create_product.html', context)
			product.current_price = product.start_price
			product.save()
			bids = Bid.objects.filter(product = product).order_by('-bid_value')
			return render(request, 'bidfeed/detail.html', {'product': product,'bids':bids})
		context = {
			"form": form,
		}
		return render(request, 'bidfeed/create_product.html', context)

def	uploadcsv(request):
	if request.method == 'POST' and request.FILES['csv_file']:
		myfile = request.FILES['csv_file']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		file_url = fs.url(filename)
		csvread = csv.reader(open(settings.BASE_DIR + settings.MEDIA_URL + filename), delimiter=',', quotechar='"')
		
		for row in csvread:
			end_date = datetime.now() + timedelta(days=int(row[3]))
			rem_days = row[3]
			time1 = datetime.now()
			tz = pytz.timezone('Asia/Kolkata')
			time1 = tz.localize(time1)
			end_date = tz.localize(end_date)
			rem_days = (end_date - time1)
			user=request.user
			rem_days = rem_days.total_seconds()
			Product.objects.create(product_name=row[0],end_date=end_date,days = int(row[3]),user=user,start_price=int(row[1]),min_increase=int(row[2]),description=row[4])
			success = "Your products are added for auction!"
	form = ProductForm()
	context = {
	'form':form,
	'success':success
	}
	return render(request, 'bidfeed/create_product.html',context)
def rem_time(product):
	
	time1 = datetime.now()
	tz = pytz.timezone('Asia/Kolkata')
	time1 = tz.localize(time1)
	rem = (product.end_date - time1)
	rem = rem.total_seconds()
	return int(rem)
	
def place_bid(request, product_id):
    form = BidForm(request.POST or None)
    product = get_object_or_404(Product, pk=product_id)
    product.rem_days = rem_time(product)
    bids = Bid.objects.filter(product = product).order_by('-bid_value')
    if product.rem_days < 1:
        product.status = 'sold'
        return render(request, 'bidfeed/detail.html', {'product': product,'bids':bids})
    product.save()
    if form.is_valid():
        bidiff =  form.cleaned_data.get("bid_value") - product.current_price
        if product.current_price > form.cleaned_data.get("bid_value") or bidiff < product.min_increase:
            error_message = "Your bid needs to be at least " + str(product.min_increase) + " points greater than the current bid"
            context = {
                'product': product,
                'form': form,
                'error_message': error_message
            }
            return render(request, 'bidfeed/place_bid.html', context)
        bidsie = Bid.objects.filter(user=request.user,product=product)
        if bidsie:
            for bidd in bidsie:
                bid = bidd 
                bid.bid_value = form.cleaned_data.get("bid_value")
        else:
            bid = form.save(commit=False)
            bid.product = product
            bid.user = request.user
        bid.save()
        product.current_price = bid.bid_value
        product.customer = bid.user.username
        product.save()
        bids = Bid.objects.filter(product=product).order_by('-bid_value')
        return render(request, 'bidfeed/detail.html', {'product': product,'bids':bids})
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'bidfeed/place_bid.html', context)


def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    products = Product.objects.filter(status='live')
    return render(request, 'bidfeed/index.html', {'products': products})




def detail(request, product_id):
	if not request.user.is_authenticated():
		return render(request, 'bidfeed/login.html')
	else:
		user = request.user
		product = get_object_or_404(Product, pk=product_id)
		time1 = datetime.now()
		tz = pytz.timezone('Asia/Kolkata')
		time1 = tz.localize(time1)
		product.rem_days = (product.end_date - time1)
		product.rem_days = product.rem_days.total_seconds()
		if product.rem_days < 1:
			product.status = 'sold'
		product = get_object_or_404(Product, pk=product_id)
		bids = Bid.objects.filter(product = product).order_by('-bid_value')
        return render(request, 'bidfeed/detail.html', {'product': product, 'user': user, 'bids':bids})
		
def user_bids(request):
	if not request.user.is_authenticated():
		return render(request, 'bidfeed/login.html')
	else:
		User = request.user
		user_bids = Bid.objects.filter(user = User)
		products = Product.objects.filter(status = 'live')
		if products:
			for product in products:
				product.rem_days = rem_time(product)
				if int(product.rem_days) < 1:
					product.status = 'sold'
			product.save()
        return render(request, 'bidfeed/user_bids.html', { 'user': User, 'bids':user_bids})
		
def user_purchases(request):
	if not request.user.is_authenticated():
		return render(request, 'bidfeed/login.html')
	else:
		User = request.user
		products = Product.objects.filter(status = 'sold',customer = User.username,bought=True)
		return render(request, 'bidfeed/purchases.html', { 'user': User, 'products':products})
			
			
def pending_purchases(request):
	if not request.user.is_authenticated():
		return render(request, 'bidfeed/login.html')
	else:
		User = request.user
		products = Product.objects.filter(status = 'live')
		if products:
			for product in products:
				product.rem_days = rem_time(product)
				if int(product.rem_days) < 1:
					product.status = 'sold'
			product.save()
		products = Product.objects.filter(status = 'sold',customer = User.username,bought=False)
		if products:
			return render(request, 'bidfeed/purchases.html', { 'user': User, 'products':products})

def sale_products(request):
	if not request.user.is_authenticated():
		return render(request, 'bidfeed/login.html')
	else:
		User = request.user
		products = Product.objects.filter(status = 'live',user=User)
		if products:
			for product in products:
				product.rem_days = rem_time(product)
				if int(product.rem_days) < 1:
					product.status = 'sold'
			product.save()
		products = Product.objects.filter(user = User)
		return render(request, 'bidfeed/sale_products.html', { 'user': User, 'products':products})
			



def favorite(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)
    try:
        if bid.is_favorite:
            bid.is_favorite = False
        else:
            bid.is_favorite = True
        bid.save()
    except (KeyError, Bid.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        if product.is_favorite:
            product.is_favorite = False
        else:
            product.is_favorite = True
        product.save()
    except (KeyError, Product.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})
	
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'bidfeed/login.html')
    else:
		products = Product.objects.filter(status = 'live')
		if products:
			for product in products:
				product.rem_days = rem_time(product)
				if int(product.rem_days) < 1:
					product.status = 'sold'
			product.save()
			products = Product.objects.filter(status = 'live')
			bid_results = Bid.objects.all()
			query = request.GET.get("q")
			if query:
				products = products.filter(
					Q(product_name__icontains=query) |
					Q(category__icontains=query)
				).distinct()
				return render(request, 'bidfeed/index.html', {
					'products': products
				})
			else:
				return render(request, 'bidfeed/index.html', {'products': products})
			return render(request, 'bidfeed/index.html', {'products': products})
		else:
			return render(request, 'bidfeed/index.html', {'products': products})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'bidfeed/login.html', context)


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				products = Product.objects.filter(status = 'live')
				for product in products:
					product.rem_days = rem_time(product)
					if product.rem_days < 1:
						product.status = 'sold'
				products = Product.objects.filter(status = 'live')
				return render(request, 'bidfeed/index.html', {'products': products})
			else:
				return render(request, 'bidfeed/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'bidfeed/login.html', {'error_message': 'Invalid login'})
	return render(request, 'bidfeed/login.html')


def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				products = Product.objects.filter(user=request.user)
				for product in products:
					product.rem_days = rem_time(product)
					if product.rem_days < 1:
						product.status = 'sold'
				products = Product.objects.filter(status = 'live')
				return render(request, 'bidfeed/index.html', {'products': products})
	context = {
		"form": form,
	}
	return render(request, 'bidfeed/register.html', context)

