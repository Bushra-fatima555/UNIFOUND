
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Q

from accounts.models import StudentProfile
from lostfound.models import Item, Claim, Feedback


# Check whether logged-in user is admin
def admin_check(user):
    return user.is_authenticated and user.is_staff


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@user_passes_test(admin_check)
def dashboard(request):

    total_students = StudentProfile.objects.count()

    total_lost_items = Item.objects.filter(
        item_type='LOST'
    ).count()

    total_found_items = Item.objects.filter(
        item_type='FOUND'
    ).count()

    total_claims = Claim.objects.count()

    pending_claims = Claim.objects.filter(
        status='PENDING'
    ).count()

    approved_claims = Claim.objects.filter(
        status='APPROVED'
    ).count()

    rejected_claims = Claim.objects.filter(
        status='REJECTED'
    ).count()

    recent_claims = Claim.objects.select_related(
        'claimant',
        'item'
    ).order_by('-created_at')[:5]

    context = {
        'total_students': total_students,
        'total_lost_items': total_lost_items,
        'total_found_items': total_found_items,
        'total_claims': total_claims,
        'pending_claims': pending_claims,
        'approved_claims': approved_claims,
        'rejected_claims': rejected_claims,
        'recent_claims': recent_claims,
    }

    return render(request, 'adminpanel/dashboard.html', context)


# ==========================================
# STUDENT MANAGEMENT
# ==========================================

@user_passes_test(admin_check)
def manage_students(request):

    students = StudentProfile.objects.select_related(
        'user'
    ).all().order_by('full_name')

    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()

    if search_query:
        students = students.filter(
            Q(full_name__icontains=search_query) |
            Q(roll_number__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    if status_filter == 'active':
        students = students.filter(user__is_active=True)

    elif status_filter == 'inactive':
        students = students.filter(user__is_active=False)

    context = {
        'students': students,
        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(request, 'adminpanel/manage_students.html', context)


@user_passes_test(admin_check)
def student_details(request, student_id):

    student = get_object_or_404(
        StudentProfile.objects.select_related('user'),
        id=student_id
    )

    return render(
        request,
        'adminpanel/student_details.html',
        {'student': student}
    )


# Activate / Deactivate Student Account
@user_passes_test(admin_check)
@require_POST
def toggle_student_status(request, student_id):

    student = get_object_or_404(
        StudentProfile.objects.select_related('user'),
        id=student_id
    )

    student.user.is_active = not student.user.is_active
    student.user.save(update_fields=['is_active'])

    if student.user.is_active:
        messages.success(
            request,
            'Student account activated successfully.'
        )
    else:
        messages.success(
            request,
            'Student account deactivated successfully.'
        )

    return redirect('manage_students')


# ==========================================
# CLAIMS MANAGEMENT
# ==========================================

@user_passes_test(admin_check)
def manage_claims(request):

    claims = Claim.objects.select_related(
        'claimant',
        'item'
    ).all().order_by('-created_at')

    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()

    if search_query:
        claims = claims.filter(
            Q(claimant__username__icontains=search_query) |
            Q(claimant__student_profile__full_name__icontains=search_query) |
            Q(claimant__student_profile__roll_number__icontains=search_query) |
            Q(item__item_name__icontains=search_query)
        )

    if status_filter in ['PENDING', 'APPROVED', 'REJECTED']:
        claims = claims.filter(status=status_filter)

    context = {
        'claims': claims,
        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(
        request,
        'adminpanel/manage_claims.html',
        context
    )


# Admin Approve / Reject Claim
@user_passes_test(admin_check)
@require_POST
def admin_update_claim_status(request, claim_id):

    claim = get_object_or_404(Claim, id=claim_id)

    new_status = request.POST.get('status')

    if new_status not in ['PENDING', 'APPROVED', 'REJECTED']:
        messages.error(request, 'Invalid claim status.')
        return redirect('manage_claims')

    claim.status = new_status
    claim.save()

    if new_status == 'REJECTED':

        other_active_claims = Claim.objects.filter(
            item=claim.item,
            status__in=['PENDING', 'APPROVED']
        ).exists()

        if not other_active_claims and claim.item.status == 'CLAIM_PENDING':
            claim.item.status = 'ACTIVE'
            claim.item.save()

    messages.success(
        request,
        f'Claim successfully {new_status.lower()}.'
    )

    return redirect('manage_claims')


# ==========================================
# REPORT MANAGEMENT
# ==========================================

@user_passes_test(admin_check)
def manage_reports(request):

    reports = Item.objects.select_related(
        'user'
    ).all().order_by('-created_at')

    search_query = request.GET.get('search', '').strip()
    selected_type = request.GET.get('item_type', '').strip()
    selected_status = request.GET.get('status', '').strip()

    if search_query:
        reports = reports.filter(
            Q(item_name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )

    if selected_type in ['LOST', 'FOUND']:
        reports = reports.filter(item_type=selected_type)

    if selected_status in [
        'ACTIVE',
        'CLAIM_PENDING',
        'RETURNED',
        'RECEIVED',
        'CLOSED'
    ]:
        reports = reports.filter(status=selected_status)

    context = {
        'reports': reports,
        'search_query': search_query,
        'selected_type': selected_type,
        'selected_status': selected_status,
    }

    return render(
        request,
        'adminpanel/manage_reports.html',
        context
    )


# Report Details
@user_passes_test(admin_check)
def report_details(request, report_id):

    report = get_object_or_404(
        Item.objects.select_related('user'),
        id=report_id
    )

    return render(
        request,
        'adminpanel/report_details.html',
        {'report': report}
    )


# Delete Fake or Inappropriate Report
@user_passes_test(admin_check)
@require_POST
def delete_report(request, report_id):

    report = get_object_or_404(Item, id=report_id)

    report.delete()

    messages.success(
        request,
        'Report deleted successfully.'
    )

    return redirect('manage_reports')


# ==========================================
# FEEDBACK MANAGEMENT
# ==========================================

@user_passes_test(admin_check)
def manage_feedback(request):

    feedbacks = Feedback.objects.select_related(
        'user'
    ).all().order_by('-created_at')

    search_query = request.GET.get('search', '').strip()
    selected_rating = request.GET.get('rating', '').strip()

    # Search feedback by subject, message or student username
    if search_query:
        feedbacks = feedbacks.filter(
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )

    # Filter feedback by rating
    if selected_rating in ['1', '2', '3', '4', '5']:
        feedbacks = feedbacks.filter(
            rating=int(selected_rating)
        )

    context = {
        'feedbacks': feedbacks,
        'search_query': search_query,
        'selected_rating': selected_rating,
    }

    return render(
        request,
        'adminpanel/manage_feedback.html',
        context
    )


# Delete Feedback
@user_passes_test(admin_check)
@require_POST
def delete_feedback(request, feedback_id):

    feedback = get_object_or_404(
        Feedback,
        id=feedback_id
    )

    feedback.delete()

    messages.success(
        request,
        'Feedback deleted successfully.'
    )

    return redirect('manage_feedback')
