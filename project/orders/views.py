from django.shortcuts import render, redirect,HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from cart.models import Cart
from django.urls import reverse
from django.contrib import messages
from .models import Order, OrderItem, Coupon, Wallet, CancellationRequest, Razorpay_Order, Order_Address, Transaction
from home.models import Address, Product
from django.db import transaction
from django.views.decorators.cache import never_cache
from django.db.models import F, Sum
from home.forms import AddressForm
from .forms import CouponApplyForm, CancellationRequestForm
from django.utils import timezone
from django.db import transaction
from django.apps import apps
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay # type: ignore
from django.core.paginator import Paginator


def is_not_superuser(user):
    return not user.is_superuser


def orders(request):
    
    current_user_orders = Order.objects.filter(user=request.user).select_related('user').prefetch_related('items__product').order_by('-order_date')
    
    return render(request, 'orders.html', {'orders': current_user_orders})


@user_passes_test(is_not_superuser, login_url='user_login')
@never_cache
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.select_related('user', 'shipping_address').prefetch_related('items__product'), pk=order_id)
    refund_amount = Transaction.objects.filter(order=order, transaction_type='Refund').aggregate(total=Sum('amount'))['total']
    cancellation_amount = Transaction.objects.filter(order=order, transaction_type='Cancellation').aggregate(total=Sum('amount'))['total']
    
    transaction_amount = refund_amount if refund_amount else None
    cancellation_transaction_amount = cancellation_amount if cancellation_amount else None
    
    form = CancellationRequestForm()
    
    # Determine payment status
    if order.payment_method.lower() == 'wallet':
        is_paid = True
    elif order.payment_method.lower() in ['cash_on_delivery', 'cod']:
        is_paid = any(item.status == 'Delivered' for item in order.items.all()) or (transaction_amount is not None)
    else:
        razorpay_order = order.razorpay_order
        is_paid = razorpay_order.paid if razorpay_order else False
    
    return render(request, 'order_detail.html', {'order': order,  'transaction_amount': transaction_amount, 'cancellation_transaction_amount': cancellation_transaction_amount, 'form': form, 'is_paid': is_paid, 
                                                 'order_items': order.items.all()})



@user_passes_test(is_not_superuser, login_url='user_login')
@never_cache
def generate_invoice(request, order_id):
    
    order = get_object_or_404(
        Order.objects.select_related('shipping_address').prefetch_related('items', 'shipping_address__user'),
        pk=order_id
    )
    
    razorpay_order = order.razorpay_order
    is_paid = razorpay_order.paid if razorpay_order else False
    return render(request, 'invoice.html', {'order': order,  'is_paid': is_paid})


@user_passes_test(is_not_superuser, login_url='user_login')
@never_cache
def request_item_cancellation(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    
    existing_request = CancellationRequest.objects.filter(order_item=order_item).exists()
    
    if existing_request:
        return render(request, 'order_detail.html', {'existing_request': True, 'order_item': order_item, 'order': order_item.order})
    
    if request.method == 'POST':
        form = CancellationRequestForm(request.POST)
        if form.is_valid():
            cancellation_request = form.save(commit=False)
            cancellation_request.order_item = order_item
            cancellation_request.user = request.user
            cancellation_request.save()
            return redirect('order_detail', order_id=order_item.order.id)
    else:
        form = CancellationRequestForm()

    return render(request, 'order_detail.html', {'form': form, 'order_item': order_item, 'order': order_item.order})


@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
@never_cache
def retry_razorpay(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            order = get_object_or_404(Order, id=order_id)
            razorpay_order = get_object_or_404(Razorpay_Order, order=order)
            razorpay_id = razorpay_order.payment_id

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            payment = client.order.create({'amount': int(order.total_cost)*100, 'currency': 'INR', 'payment_capture': '1'})

            razorpay_order.payment_id = payment['id']
            razorpay_order.save()

            request.session['razorpay_order_id'] = payment['id']
            razor_key_id = settings.RAZOR_KEY_ID

            save_order(request)
            return render(request, "razorpay.html", {'payment': payment, 'razor_key_id': razor_key_id, 'razorpay_id': razorpay_id})
    else:
        return redirect('home')


@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
def remove_coupon(request):
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
    return redirect('checkout')


@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
def apply_coupon(request):
    if request.method == 'POST':
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            now = timezone.now()
            CouponModel = apps.get_model('orders', 'Coupon') 
            try:
                coupon = CouponModel.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, is_active=True)
                request.session['coupon_id'] = coupon.id
            except CouponModel.DoesNotExist:
                request.session['coupon_error'] = "Invalid coupon code or the coupon is inactive."
                request.session['coupon_id'] = None
    return redirect('checkout')


@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
def remove_wallet(request):
    if 'use_wallet' in request.session:
        del request.session['use_wallet']
    return redirect('checkout')


@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
def apply_wallet(request):
    if request.method == 'POST':
        request.session['use_wallet'] = True
    return redirect('checkout')

@never_cache
@user_passes_test(is_not_superuser, login_url='user_login')
def add_address_checkout(request):

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('checkout')    
    else:
        form = AddressForm()
    return render(request, 'add_address_checkout.html', {'form': form})


@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
@never_cache
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user, product__is_listed=True)

    out_of_stock_items = [item for item in cart_items if item.product.stock <= 0]
    if out_of_stock_items:
        return redirect('cart')

    subtotal = Decimal(0)
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        subtotal += item.subtotal

    total_cost = subtotal

    coupon_id = request.session.get('coupon_id')
    discount_amount = Decimal(0)
    coupon = None
    error_message = request.session.pop('coupon_error', None)

    if coupon_id:
        CouponModel = apps.get_model('orders', 'Coupon') 
        try:
            coupon = CouponModel.objects.get(id=coupon_id, is_active=True)
            if coupon.valid_from <= timezone.now() <= coupon.valid_to:
                if coupon.minimum_required is None or total_cost >= coupon.minimum_required:  
                    discount_amount = coupon.discount_amount
                    total_cost -= discount_amount
                else:
                    error_message = "The total cost does not meet the minimum required amount for this coupon."
                    coupon = None  
            else:
                error_message = "This coupon is no longer valid."
                coupon = None  
        except CouponModel.DoesNotExist:
            if 'error_message' not in locals():
                error_message = "Invalid coupon code or the coupon is inactive."


    shipping_addresses = request.user.address_set.all()
    
    wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'balance': 0})

    use_wallet = request.session.get('use_wallet', False)
    wallet_discount = Decimal(0)
    
    if use_wallet:
        if wallet.balance > 0:
            wallet_discount = min(wallet.balance, total_cost)
            total_cost -= wallet_discount
        else:
            request.session.pop('use_wallet', None)
            use_wallet = False

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'shipping_addresses': shipping_addresses,
        'total_cost': total_cost,
        'subtotal': subtotal,
        'coupon': coupon,
        'discount_amount': discount_amount,
        'form': CouponApplyForm(),
        'error_message': error_message,  
        'wallet': wallet,
        'use_wallet': use_wallet,
        'wallet_discount': wallet_discount,
    })



@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
def place_order(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment-method')
        
        if payment_method in ['cash_on_delivery', 'wallet']:
            return save_order(request)
        else:
            return redirect('checkout')

    return redirect('order_success')


@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
@never_cache
def razorpay_view(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('checkout') 

        for item in cart_items:
            if item.quantity > item.product.stock:
                return redirect('cart')

        subtotal = Decimal('0.00')
        discount_amount = Decimal('0.00')

        coupon_id = request.session.get('coupon_id')
        if coupon_id:
            CouponModel = apps.get_model('orders', 'Coupon')
            try:
                coupon = CouponModel.objects.get(id=coupon_id, is_active=True)
                discount_amount = coupon.discount_amount
            except CouponModel.DoesNotExist:
                request.session['coupon_id'] = None

        for cart_item in cart_items:
            product_price = cart_item.product.price if cart_item.product.price is not None else Decimal('0.00')
            subtotal += product_price * cart_item.quantity

        total_cost = subtotal - discount_amount
        
        use_wallet = request.session.get('use_wallet', False)
        wallet_discount = Decimal('0.00')
        if use_wallet:
            try:
                wallet = Wallet.objects.get(user=request.user)
                if wallet.balance > 0:
                    wallet_discount = min(wallet.balance, total_cost)
                    total_cost -= wallet_discount
            except Wallet.DoesNotExist:
                pass
                
        if total_cost <= 0:
            return redirect('checkout')
        
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        payment = client.order.create({'amount': int(total_cost)*100, 'currency':'INR', 'payment_capture' : '1'})
        
        razorpay_order = Razorpay_Order(amount=total_cost, payment_id=payment['id'])
        razorpay_order.save()
        
        request.session['razorpay_order_id'] = payment['id']  
        
        razor_key_id = settings.RAZOR_KEY_ID
        
        save_order(request)
        return render(request, "razorpay.html", {'payment': payment, 'razor_key_id': razor_key_id})
    else:
        return redirect('home') 


@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
@never_cache
@csrf_exempt
def success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")

        razorpay_order = Razorpay_Order.objects.filter(payment_id=razorpay_order_id).first()
     
        if razorpay_order:
            razorpay_order.paid = True
            razorpay_order.save()
            
            # Post-payment stock validation
            try:
                order = Order.objects.get(razorpay_order=razorpay_order)
            except Order.DoesNotExist:
                return redirect(reverse('home'))
                
            out_of_stock = False
            for item in order.items.all():
                if item.quantity_ordered > item.product.stock:
                    out_of_stock = True
                    break
                    
            if out_of_stock:
                # Cancel the order items
                for item in order.items.all():
                    item.status = 'Cancelled'
                    item.save()
                    
                # Refund to Wallet
                wallet, _ = Wallet.objects.get_or_create(user=order.user)
                refund_amount = order.total_cost + order.wallet_discount
                wallet.balance += refund_amount
                wallet.save()
                
                # Record transaction
                Transaction.objects.create(
                    user=order.user,
                    amount=refund_amount,
                    transaction_type='Refund',
                    order=order
                )
                
                return render(request, 'order_success.html', {'refunded': True, 'order': order})
            else:
                # Everything is in stock, deduct it now
                for item in order.items.all():
                    item.product.stock -= item.quantity_ordered
                    item.product.save()

            return render(request, 'order_success.html')
        else:
            return redirect(reverse('home'))

    return render(request, 'order_success.html')



@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
def save_order(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('checkout')

        for item in cart_items:
            if item.quantity > item.product.stock:
                return redirect('cart')

        shipping_address_id = request.POST.get('selected-address')
        address = Address.objects.filter(user=request.user, id=shipping_address_id).first()
        if not address:
            return redirect('checkout')

        with transaction.atomic():
            subtotal = Decimal('0.00')
            original_total = Decimal('0.00')

            coupon_id = request.session.get('coupon_id')
            coupon = None
            discount_amount = Decimal('0.00')

            if coupon_id:
                CouponModel = apps.get_model('orders', 'Coupon')
                try:
                    coupon = CouponModel.objects.get(id=coupon_id, is_active=True)
                    discount_amount = coupon.discount_amount
                except CouponModel.DoesNotExist:
                    coupon = None
                    request.session['coupon_id'] = None

            for cart_item in cart_items:
                product_price = cart_item.product.price if cart_item.product.price is not None else Decimal('0.00')
                subtotal += product_price * cart_item.quantity
                original_total += cart_item.product.original_price * cart_item.quantity if cart_item.product.original_price is not None else Decimal('0.00')

            total_cost = subtotal - discount_amount
            
            use_wallet = request.session.get('use_wallet', False)
            wallet_discount = Decimal('0.00')
            wallet_instance = None
            if use_wallet:
                try:
                    wallet_instance = Wallet.objects.get(user=request.user)
                    if wallet_instance.balance > 0:
                        wallet_discount = min(wallet_instance.balance, total_cost)
                        total_cost -= wallet_discount
                except Wallet.DoesNotExist:
                    pass
            
            payment_method = request.POST.get('payment-method')

            order_address = Order_Address.objects.create(
                user=request.user,
                street=address.street,
                city=address.city,
                state=address.state,
                country=address.country,
                postal_code=address.postal_code,
                phone_number=address.phone_number,
                name=address.name,
            )

            razorpay_order = None
            if payment_method not in ['cod', 'cash_on_delivery', 'wallet']:
                razorpay_order_id = request.session.get('razorpay_order_id')
                if razorpay_order_id:
                    razorpay_order = Razorpay_Order.objects.filter(payment_id=razorpay_order_id).first()
                    if Order.objects.filter(razorpay_order=razorpay_order).exists():
                        razorpay_order = None

            order = Order.objects.create(
                user=request.user,
                total_cost=total_cost,
                payment_method=payment_method,
                total_products=len(cart_items),
                subtotal=subtotal,
                original_total=original_total,
                wallet_discount=wallet_discount,
                coupon=coupon,
                shipping_address=order_address,
                razorpay_order=razorpay_order if payment_method not in ['cod', 'cash_on_delivery', 'wallet'] else None
            )

            if wallet_discount > 0 and wallet_instance:
                wallet_instance.balance -= wallet_discount
                wallet_instance.save()
                Transaction.objects.create(
                    user=request.user,
                    amount=wallet_discount,
                    transaction_type='Purchase (Wallet)',
                    order=order
                )

            for cart_item in cart_items:
                product_price = cart_item.product.price if cart_item.product.price is not None else Decimal('0.00')
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity_ordered=cart_item.quantity,
                    original_price_total=cart_item.product.original_price * cart_item.quantity if cart_item.product.original_price is not None else Decimal('0.00'),
                    total_price=product_price * cart_item.quantity,
                    offer=cart_item.product.offer
                )
                
                if payment_method in ['cash_on_delivery', 'wallet']:
                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.save()

            cart_items.delete()
            if 'coupon_id' in request.session:
                del request.session['coupon_id']
            if 'use_wallet' in request.session:
                del request.session['use_wallet']
            if 'razorpay_order_id' in request.session and payment_method not in ['cod', 'cash_on_delivery', 'wallet']:
                del request.session['razorpay_order_id']

            return redirect('order_success')

    return redirect('order_success')


@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
@never_cache
def order_success(request):
    return render(request, 'order_success.html')


@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
@never_cache
def wallet(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user, balance=0)
        
    transactions_list = Transaction.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(transactions_list, 5)  # Show 5 transactions per page
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    
    return render(request, 'wallet.html', {'wallet': wallet, 'transactions': transactions})