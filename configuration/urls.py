from django.urls import path

from .views import *


urlpatterns = [
    path('measurement-unit/', MeasurementUnitListView.as_view(), name='measurement-units'),
    path('measurement-unit/<int:pk>', MeasurementUnitDeleteView.as_view(), name='measurement-unit-delete'),
    path('service/', ServiceCreateListView.as_view(), name='services'),
    path('service/<int:pk>/', ServiceDeleteView.as_view(), name='service-delete'),
    path('tariff/', TariffListView.as_view(), name='tariffs'),
    path('tariff/create/', TariffCreateView.as_view(), name='tariff-create'),
    path('tariff/<int:pk>/', TariffDetailView.as_view(), name='tariff-detail'),
    path('tariff/update/<int:pk>/', TariffUpdateView.as_view(), name='tariff-update'),
    path('tariff/delete/<int:pk>/', tariff_delete, name='tariff-delete'),
    path('tariff-service/delete/<int:pk_tariff_service_to_delete>/', tariff_service_delete, name='tariff-service-delete'),
    path('roles/', RolesListUpdate.as_view(), name='roles'),
    path('user/', UserListView.as_view(), name='users'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('user/delete/<int:pk>', delete_user, name='user-delete'),
    path('requisites/', PaymentRequisitesCreateView.as_view(), name='requisites'),
    path('article-payment/', ArticlePaymentListView.as_view(), name='articles-payment'),
    path('article-payment/create/', ArticlePaymentCreateView.as_view(), name='article-payment-create'),
    path('article-payment/update/<int:pk>/', ArticlePaymentUpdateView.as_view(), name='article-payment-update'),
    path('article-payment/delete/<int:pk>/', delete_article, name='delete-article'),
]
