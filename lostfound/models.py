
from django.db import models
from django.conf import settings


class Item(models.Model):

    ITEM_TYPES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    ]

    CATEGORIES = [
        ('Electronics', 'Electronics'),
        ('Books', 'Books'),
        ('Bags', 'Bags'),
        ('Clothing', 'Clothing'),
        ('Accessories', 'Accessories'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CLAIM_PENDING', 'Claim Pending'),
        ('RETURNED', 'Returned'),
        ('RECEIVED', 'Received'),
        ('CLOSED', 'Closed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    item_name = models.CharField(max_length=200)

    item_type = models.CharField(
        max_length=10,
        choices=ITEM_TYPES
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORIES
    )

    description = models.TextField()

    date = models.DateField()

    location = models.CharField(max_length=200)

    image = models.ImageField(
        upload_to='items/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_name} - {self.item_type}"


class Claim(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='claims'
    )

    lost_item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='matched_claims'
    )

    claimant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_claims'
    )

    claim_message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    claimant_confirmed = models.BooleanField(default=False)

    finder_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim for {self.item.item_name}"


class Feedback(models.Model):

    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )

    subject = models.CharField(max_length=200)

    message = models.TextField()

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=5
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.user.username}"
