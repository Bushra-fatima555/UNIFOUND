
from django.urls import path
from . import views

urlpatterns = [

    # Create Lost or Found Item
    path(
        'report/',
        views.create_item,
        name='create_item'
    ),

    # Display Lost and Found Items
    path(
        'items/',
        views.item_list,
        name='item_list'
    ),

    # Item Details
    path(
        'item/<int:id>/',
        views.item_detail,
        name='item_detail'
    ),

    # Submit Claim
    path(
        'item/<int:id>/claim/',
        views.submit_claim,
        name='submit_claim'
    ),

    # View Claim Requests
    path(
        'item/<int:id>/claims/',
        views.claim_requests,
        name='claim_requests'
    ),

    # Update Claim Status
    path(
        'claim/<int:id>/update/',
        views.update_claim_status,
        name='update_claim_status'
    ),

    # Confirm Item Return
    path(
        'claim/<int:id>/confirm/',
        views.confirm_return,
        name='confirm_return'
    ),

    # Edit Item
    path(
        'item/<int:id>/edit/',
        views.edit_item,
        name='edit_item'
    ),

    # Delete Item
    path(
        'item/<int:id>/delete/',
        views.delete_item,
        name='delete_item'
    ),

    # Student Feedback
    path(
        'feedback/',
        views.submit_feedback,
        name='submit_feedback'
    ),

]
