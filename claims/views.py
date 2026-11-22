
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Claim, Feedback


def submit_claim(request):

    if request.method == 'POST':

        claimant_name = request.POST.get('claimant_name')
        item_name = request.POST.get('item_name')
        claim_message = request.POST.get('claim_message')

        Claim.objects.create(
            claimant_name=claimant_name,
            item_name=item_name,
            claim_message=claim_message
        )

        messages.success(
            request,
            'Your claim has been submitted successfully!'
        )

        return redirect('submit_claim')

    return render(request, 'claims/submit_claim.html')



def submit_feedback(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if student_name and email and subject and message:
            Feedback.objects.create(
                student_name=student_name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Your feedback has been submitted successfully!')
            return redirect('submit_feedback')

        messages.error(request, 'Please fill in all fields.')

    return render(request, 'claims/submit_feedback.html')
