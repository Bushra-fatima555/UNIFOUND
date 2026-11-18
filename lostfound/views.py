
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Item, Claim
from .forms import ItemForm,ClaimForm


# Create Lost or Found Item
@login_required
def create_item(request):

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()

            return redirect('item_list')

    else:
        form = ItemForm()

    return render(
        request,
        'item_pages/create_item.html',
        {'form': form}
    )


# Display Lost and Found Items Separately

@login_required
def item_list(request):

    items = Item.objects.all().order_by('-created_at')

    # Search by item name
    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(item_name__icontains=search_query)

    # Filter by Lost or Found
    selected_type = request.GET.get('item_type', '')
    if selected_type:
        items = items.filter(item_type=selected_type)

    # Filter by Category
    selected_category = request.GET.get('category', '')
    if selected_category:
        items = items.filter(category=selected_category)

    context = {
        'items': items,
        'search_query': search_query,
        'selected_type': selected_type,
        'selected_category': selected_category,
        'categories': Item.CATEGORIES,
    }

    return render(
        request,
        'item_pages/item_list.html',
        context
    )


# Display Single Item Details
@login_required
def item_detail(request, id):

    item = get_object_or_404(Item, id=id)

    approved_claim = Claim.objects.filter(
        item=item,
        status='APPROVED'
    ).first()

    return render(
        request,
        'item_pages/item_detail.html',
        {
            'item': item,
            'approved_claim': approved_claim
        }
    )

# Submit Claim Request
@login_required
def submit_claim(request, id):

    item = get_object_or_404(Item, id=id)

    # Only FOUND items can be claimed
    if item.item_type != 'FOUND':
        return redirect('item_detail', id=item.id)

    # User cannot claim their own item
    if item.user == request.user:
        return redirect('item_detail', id=item.id)

    # Item must be active
    if item.status != 'ACTIVE':
        return redirect('item_detail', id=item.id)

    # Check if user already submitted a claim
    existing_claim = Claim.objects.filter(
        item=item,
        claimant=request.user
    ).exists()

    if existing_claim:
        return redirect('item_detail', id=item.id)

    if request.method == 'POST':
        form = ClaimForm(request.POST)

        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user
            claim.save()

            item.status = 'CLAIM_PENDING'
            item.save(update_fields=['status'])

            return redirect('item_detail', id=item.id)

    else:
        form = ClaimForm()

    return render(
        request,
        'item_pages/submit_claim.html',
        {
            'form': form,
            'item': item
        }
    )
# View Claim Requests
@login_required
def claim_requests(request, id):

    item = get_object_or_404(Item, id=id)

    # Only item owner can view claims
    if item.user != request.user:
        return redirect('item_detail', id=item.id)

    claims = Claim.objects.filter(
        item=item
    ).order_by('-created_at')

    return render(
        request,
        'item_pages/claim_requests.html',
        {
            'item': item,
            'claims': claims
        }
    )

# Approve or Reject Claim Request

@login_required
def update_claim_status(request, id):

    claim = get_object_or_404(Claim, id=id)
    item = claim.item

    if item.user != request.user:
        return redirect('item_detail', id=item.id)

    if request.method == 'POST' and claim.status == 'PENDING':

        action = request.POST.get('action')

        if action == 'approve':
            claim.status = 'APPROVED'
            claim.save(update_fields=['status'])

            item.status = 'CLAIM_PENDING'
            item.save(update_fields=['status'])

        elif action == 'reject':
            claim.status = 'REJECTED'
            claim.save(update_fields=['status'])

            # Check if any pending or approved claim remains
            active_claims = Claim.objects.filter(
                item=item,
                status__in=['PENDING', 'APPROVED']
            ).exists()

            if not active_claims:
                item.status = 'ACTIVE'
                item.save(update_fields=['status'])

    return redirect('claim_requests', id=item.id)

# Confirm Item Return
@login_required
def confirm_return(request, id):

    claim = get_object_or_404(
        Claim,
        id=id,
        status='APPROVED'
    )

    item = claim.item

    if request.method == 'POST':

        # Claimant confirmation
        if request.user == claim.claimant:
            claim.claimant_confirmed = True

        # Finder/Item owner confirmation
        elif request.user == item.user:
            claim.finder_confirmed = True

        else:
            return redirect('item_detail', id=item.id)

        claim.save()

        # Both students confirmed
        if claim.claimant_confirmed and claim.finder_confirmed:

            item.status = 'RETURNED'
            item.save(update_fields=['status'])

        return redirect('item_detail', id=item.id)

    return redirect('item_detail', id=item.id)

# Edit Lost or Found Item
@login_required
def edit_item(request, id):

    item = get_object_or_404(Item, id=id)

    # Only item owner can edit
    if item.user != request.user:
        return redirect('item_list')

    # Do not edit returned items
    if item.status == 'RETURNED':
        return redirect('item_detail', id=item.id)

    if request.method == 'POST':

        form = ItemForm(
            request.POST,
            request.FILES,
            instance=item
        )

        if form.is_valid():
            form.save()
            return redirect('item_detail', id=item.id)

    else:
        form = ItemForm(instance=item)

    return render(
        request,
        'item_pages/edit_item.html',
        {
            'form': form,
            'item': item
        }
    )

# Delete Lost or Found Item
@login_required
def delete_item(request, id):

    item = get_object_or_404(Item, id=id)

    # Only item owner can delete
    if item.user != request.user:
        return redirect('item_list')

    if request.method == 'POST':
        item.delete()
        return redirect('item_list')

    return render(
        request,
        'item_pages/delete_item.html',
        {'item': item}
    )
