from datetime import datetime
from store.models import Order
from django.db.models import Sum
from user.models import User

def level(user:User):
    now = datetime.now()
    last_month = now.month - 1
    last_year = now.year if last_month == 0 else now.year - 1
    sum_orders = Order.objects.filter(user=user, created_at__year=last_year, created_at__month=last_month).aggregate(total=Sum('product__price'))['total']
    sum_orders_fee = sum_orders * 0.005
    balance_effect = user.balance - sum_orders_fee
    level_1_limit = 50000000
    level_2_limit = 100000000
    level_3_limit = 150000000
    level_4_limit = 200000000
    level_5_limit = 250000000
    level_6_limit = 300000000
    level_7_limit = 350000000
    level_8_limit = 400000000
    if balance_effect < level_1_limit:
        return 1
    elif balance_effect < level_2_limit:
        return 2
    elif balance_effect < level_3_limit:
        return 3
    elif balance_effect < level_4_limit:
        return 4
    elif balance_effect < level_5_limit:
        return 5
    elif balance_effect < level_6_limit:
        return 6
    elif balance_effect < level_7_limit:
        return 7
    elif balance_effect < level_8_limit:
        return 8
    return 9
