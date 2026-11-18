
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.db.models import Q

from claims.models import Claim


def admin_check(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(admin_check)
def dashboard(request):

    total_students = User.objects.filter(is_staff=False).count()
    total_claims = Claim.objects.count()
    pending_claims = Claim.objects.filter(status='Pending').count()
    approved_claims = Claim.objects.filter(status='Approved').count()
    rejected_claims = Claim.objects.filter(status='Rejected').count()

    recent_claims = Claim.objects.order_by('-created_at')[:5]

    context = {
        'total_students': total_students,
        'total_claims': total_claims,
        'pending_claims': pending_claims,
        'approved_claims': approved_claims,
        'rejected_claims': rejected_claims,
        'recent_claims': recent_claims,
    }

    return render(request, 'adminpanel/dashboard.html', context)

@user_passes_test(admin_check)
def manage_claims(request):

   

    claims = Claim.objects.all().order_by('-created_at')

    search_query = request.GET.get('search', '').strip()

    status_filter = request.GET.get('status', '').strip()

    if search_query:
        claims = claims.filter(
            Q(claimant_name__icontains=search_query) |
            Q(item_name__icontains=search_query)
        )

    if status_filter in ['Pending', 'Approved', 'Rejected']:
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

@user_passes_test(admin_check)
@require_POST
def update_claim_status(request, claim_id):

    claim = get_object_or_404(Claim, id=claim_id)

    new_status = request.POST.get('status')

    if new_status in ['Pending', 'Approved', 'Rejected']:

        claim.status = new_status
        claim.save()

        messages.success(
            request,
            f'Claim successfully {new_status.lower()}.'
        )

    else:
        messages.error(request, 'Invalid claim status.')

    return redirect('manage_claims')
@user_passes_test(admin_check)
def manage_students(request):

    students = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).order_by('-date_joined')

    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '')

    if status_filter == 'active':
        students = students.filter(is_active=True)

    elif status_filter == 'inactive':
        students = students.filter(is_active=False)

    if search_query:
        students = students.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    context = {
        'students': students,
        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(
        request,
        'adminpanel/manage_students.html',
        context
    )

@user_passes_test(admin_check)
def student_detail(request, student_id):

    student = get_object_or_404(
        User,
        id=student_id,
        is_staff=False,
        is_superuser=False
    )

    context = {
        'student': student,
    }

    return render(
        request,
        'adminpanel/student_detail.html',
        context
    )
@user_passes_test(admin_check)
@require_POST
def toggle_student_status(request, student_id):

    student = get_object_or_404(
        User,
        id=student_id,
        is_staff=False,
        is_superuser=False
    )

    student.is_active = not student.is_active
    student.save()

    messages.success(
        request,
        f"{student.username}'s status updated successfully."
    )

    return redirect('manage_students')

    

