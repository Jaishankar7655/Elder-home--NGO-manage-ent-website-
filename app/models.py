from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid
from datetime import datetime
import os

def elder_photo_path(instance, filename):
    """Generate file path for elder photos"""
    ext = filename.split('.')[-1]
    filename = f"elder_{instance.registration_id}.{ext}"
    return os.path.join('elders/photos/', filename)

def elder_id_proof_path(instance, filename):
    """Generate file path for elder ID proofs"""
    ext = filename.split('.')[-1]
    filename = f"elder_id_{instance.registration_id}.{ext}"
    return os.path.join('elders/id_proofs/', filename)

class Elder(models.Model):
    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Auto-generated registration ID
    registration_id = models.CharField(max_length=20, unique=True, blank=True)
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to=elder_photo_path, help_text="Upload elder's photo for ID card")
    age = models.PositiveIntegerField()
    
    # Contact Information
    address = models.TextField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # ID Proof
    id_proof = models.FileField(upload_to=elder_id_proof_path, help_text="Upload ID proof (Aadhar, PAN, etc.)")
    
    # Guardian Information
    guardian_name = models.CharField(max_length=200)
    guardian_contact = models.CharField(validators=[phone_regex], max_length=17)
    guardian_relationship = models.CharField(max_length=100, default="Son/Daughter")
    
    # Health Information
    health_conditions = models.TextField(blank=True, help_text="Describe any health conditions or medical history")
    special_requirements = models.TextField(blank=True, help_text="Any special care requirements")
    
    # Registration Status
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    rejection_reason = models.TextField(blank=True, help_text="Reason for rejection (if applicable)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.registration_id:
            # Generate registration ID: VK2025-0001 format
            year = datetime.now().year
            count = Elder.objects.filter(registration_id__startswith=f'VK{year}').count() + 1
            self.registration_id = f'VK{year}-{count:04d}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.full_name} ({self.registration_id})"
    
    class Meta:
        ordering = ['-created_at']
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import datetime


class Volunteer(models.Model):
    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # Auto-generated volunteer ID
    volunteer_id = models.CharField(max_length=20, unique=True, blank=True)

    # Personal Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    address = models.TextField()
    age = models.PositiveIntegerField()

    # Profile Photo with better file path handling
    def volunteer_photo_path(instance, filename):
        """Generate file path for volunteer photos"""
        ext = filename.split('.')[-1]
        filename = f"volunteer_{instance.volunteer_id}.{ext}"
        return os.path.join('volunteers/profile_photos/', filename)

    profile_photo = models.ImageField(
        upload_to=volunteer_photo_path,
        blank=True,
        null=True,
        help_text="Upload a profile picture for ID card"
    )

    # Volunteer Information
    skills = models.TextField(help_text="Describe your skills and how you can help")
    availability = models.CharField(max_length=200, help_text="When are you available? (e.g., weekends, evenings)")
    experience = models.TextField(blank=True, help_text="Any previous volunteer experience")

    # Status
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    rejection_reason = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.volunteer_id:
            # Generate volunteer ID: VL2025-0001 format
            year = datetime.now().year
            count = Volunteer.objects.filter(volunteer_id__startswith=f'VL{year}').count() + 1
            self.volunteer_id = f'VL{year}-{count:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.volunteer_id})"

    class Meta:
        ordering = ['-created_at']
        
    @property
    def profile_photo_url(self):
        """Return the URL of the profile photo or None if not available"""
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        return None
class Donation(models.Model):
    DONATION_TYPES = [
        ('food', 'Food'),
        ('clothes', 'Clothes'),
        ('medicines', 'Medicines'),
        ('money', 'Money'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Donor Information
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=17)
    
    # Donation Details
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES)
    description = models.TextField(help_text="Describe the donation items/amount")
    message = models.TextField(blank=True, help_text="Any message or special instructions")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fulfilled_at = models.DateTimeField(null=True, blank=True)
    fulfilled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.donor_name} - {self.donation_type} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']

class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100, help_text="e.g., Son of Mr. X, Volunteer, etc.")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    comment = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"
    
    class Meta:
        ordering = ['-created_at']

class ContactInquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=17)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Contact Inquiries"