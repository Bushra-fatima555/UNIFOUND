
from django.urls import path
from . import views

urlpatterns = [

    path('report/', views.create_item, name='create_item'),

    path('items/', views.item_list, name='item_list'),

    path('item/<int:id>/', views.item_detail, name='item_detail'),

    path(
        'item/<int:id>/claim/',
        views.submit_claim,
        name='submit_claim'
    ),

    path(
        'item/<int:id>/claims/',
        views.claim_requests,
        name='claim_requests'
    ),

    path(
        'claim/<int:id>/update/',
        views.update_claim_status,
        name='update_claim_status'
    ),

    path(
        'claim/<int:id>/confirm/',
        views.confirm_return,
        name='confirm_return'
    ),
path(
    'item/<int:id>/edit/',
    views.edit_item,
    name='edit_item'
),
path(
    'item/<int:id>/delete/',
    views.delete_item,
    name='delete_item'
),
]
