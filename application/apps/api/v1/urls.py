from django.urls import path

from application.apps.api.v1.views.dealers import DealerView
from application.apps.api.v1.views.orders import OrderView

urlpatterns = [
    path('dealers/', DealerView.as_view(), name='dealers'),
    path('orders/', OrderView.as_view(), name='orders')
]
