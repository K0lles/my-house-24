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
    path('flat/', FlatListView.as_view(), name='flats'),
    path('flat/create', FlatCreateView.as_view(), name='flat-create'),
    path('flat/<int:flat_pk>/', FlatDetailView.as_view(), name='flat-detail'),
    path('flat/update/<int:flat_pk>/', FlatUpdateView.as_view(), name='flat-update'),
    path('flat/delete/<int:flat_pk>/', delete_flat, name='flat-delete'),
    path('personal-account/', PersonalAccountListView.as_view(), name='personal-accounts'),
    path('personal-account/create/', PersonalAccountCreateView.as_view(), name='personal-account-create'),
    path('personal-account/<int:account_pk>/', PersonalAccountDetailView.as_view(), name='personal-account-detail'),
    path('personal-account/update/<int:account_pk>/', PersonalAccountUpdateView.as_view(), name='personal-account-update'),
    path('personal-account/delete/<int:account_pk>/', delete_personal_account, name='personal-account-delete'),
    path('account/check-number/', personal_account_is_unique, name='account-check-number'),
    path('owner/create/', OwnerCreateView.as_view(), name='owner-create'),
    path('owner/update/<int:owner_pk>/', OwnerUpdateView.as_view(), name='owner-update'),
    path('owner/', OwnerListView.as_view(), name='owners'),
]
