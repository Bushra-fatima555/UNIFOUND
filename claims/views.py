
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Claim


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
