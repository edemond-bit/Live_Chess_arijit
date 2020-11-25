import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime
from users.models import Membership, Employee
import collections

session_id = collections.deque()

# This is your real test secret API key.
stripe.api_key = "sk_test_51HWPgxCMmNngA38zYgRqapqIq7UvFvccFYuey3A51Onwv6DwoQNuuYg6bw5apiTxF6Ml8cY37e4OOvUQylVLA1Eq00nogO1Ypg"
CHESS_DOMAIN = 'http://localhost:8000'
customer = stripe.Customer.create()

@login_required
def calculate_order_amount(self):
    product_id = self.body
    employee = Employee.objects.filter(user=self.user).first()
    membership = Membership.objects.filter(id=product_id).first()
    session_id.append(str(employee.id) + ':' + str(membership.id))
    item = {'product': membership.product, 'currency': membership.currency, 'price': membership.price*100}
    return item


@login_required
def checkout_page(self, id):
    membership = Membership.objects.filter(id=id).first()
    context = {'product_id': id, 'product': membership.product, 'price': membership.price}
    return render(self, 'gateway/checkout.html', context)


@login_required
def create_payment(self):
    try:
        item = calculate_order_amount(self)
        #print(item);
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item['currency'],
                    'product_data': {
                        'name': item['product'],
                    },
                    'unit_amount': item['price'],
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=CHESS_DOMAIN + '/gateway/purchase_success',
            cancel_url=CHESS_DOMAIN + '/gateway/purchase_cancel',
        )
        #print(checkout_session.id)
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse(error=str(e)), 403


@login_required
def success(self):
    try:
        items = session_id.pop().split(':')
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        Employee.objects.filter(id=items[0]).update(membership_id=items[1], purchase_date=dt_string)
        #membership = Membership.objects.filter(id=items[1]).first()

        return render(self, "gateway/success.html")
    except Exception as e:
        return JsonResponse(error=str(e)), 403


@login_required
def cancel(self):
    return render(self, "gateway/cancel.html")