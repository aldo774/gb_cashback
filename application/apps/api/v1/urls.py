from django.urls import path

from application.apps.api.v1.views.dealers import DealerView

urlpatterns = [
    path('dealers/', DealerView.as_view(), name='dealers')
]
