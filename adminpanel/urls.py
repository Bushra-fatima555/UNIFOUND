
from django.urls import path
from . import views

urlpatterns = [

    # Admin Dashboard
    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    # Student Management
    path(
        'students/',
        views.manage_students,
        name='manage_students'
    ),

    path(
        'student/<int:student_id>/',
        views.student_details,
        name='student_details'
    ),

    path(
        'student/<int:student_id>/toggle-status/',
        views.toggle_student_status,
        name='toggle_student_status'
    ),

    # Claims Management
    path(
        'claims/',
        views.manage_claims,
        name='manage_claims'
    ),

    path(
        'update-claim/<int:claim_id>/',
        views.admin_update_claim_status,
        name='admin_update_claim_status'
    ),

    # Report Management
    path(
        'reports/',
        views.manage_reports,
        name='manage_reports'
    ),

    path(
        'report/<int:report_id>/',
        views.report_details,
        name='report_details'
    ),

    path(
        'report/<int:report_id>/delete/',
        views.delete_report,
        name='delete_report'
    ),

    # Feedback Management
    path(
        'feedback/',
        views.manage_feedback,
        name='manage_feedback'
    ),

    path(
        'feedback/<int:feedback_id>/delete/',
        views.delete_feedback,
        name='delete_feedback'
    ),

]
