from django.urls import path

from .views import *

urlpatterns = [
    path('house/', HouseListView.as_view(), name='houses'),
    path('house/create/', HouseCreateView.as_view(), name='house-create'),
    path('house/<int:house_pk>/', HouseDetailView.as_view(), name='house-detail'),
    path('house/update/<int:house_pk>/', HouseUpdateView.as_view(), name='house-update'),
    path('house/delete/<int:house_pk>/', delete_house, name='house-delete'),
    path('house/section/<int:section_pk>/', delete_section, name='section-delete'),
    path('house/floor/<int:floor_pk>/', delete_floor, name='floor-delete'),
    path('house/house-user/<int:house_user_pk>/', delete_house_user, name='house_user-delete'),
    path('flat/create/', FlatCreateView.as_view(), name='flat-create'),
    path('flat/update/<int:flat_pk>/', FlatUpdateView.as_view(), name='flat-update'),
    path('account/check-number/', personal_account_is_unique, name='account-check_number'),
]
