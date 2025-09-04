from django import forms
from .models import Elder, Volunteer, Donation, ContactInquiry, Testimonial

class ElderRegistrationForm(forms.ModelForm):
    class Meta:
        model = Elder
        fields = [
            'full_name', 'photo', 'age', 'address', 'phone_number',
            'id_proof', 'guardian_name', 'guardian_contact', 'guardian_relationship',
            'health_conditions', 'special_requirements'
        ]
        
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter full name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Age',
                'min': '60'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Complete address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '+91XXXXXXXXXX'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'accept': 'image/*'
            }),
            'id_proof': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Guardian/Child name'
            }),
            'guardian_contact': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '+91XXXXXXXXXX'
            }),
            'guardian_relationship': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Son/Daughter/Other'
            }),
            'health_conditions': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Any health conditions, medications, or medical history'
            }),
            'special_requirements': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Any special care requirements or preferences'
            }),
        }
        
        labels = {
            'full_name': 'Full Name *',
            'photo': 'Elder Photo (for ID Card) *',
            'age': 'Age *',
            'address': 'Complete Address *',
            'phone_number': 'Phone Number',
            'id_proof': 'ID Proof (Aadhar/PAN/etc.) *',
            'guardian_name': 'Guardian/Child Name *',
            'guardian_contact': 'Guardian Contact Number *',
            'guardian_relationship': 'Relationship *',
            'health_conditions': 'Health Conditions',
            'special_requirements': 'Special Requirements',
        }

class VolunteerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = [
            'full_name', 'email', 'phone_number', 'address', 'age',
            'profile_photo', 'skills', 'availability', 'experience'
        ]
        
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'your.email@example.com'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '+91XXXXXXXXXX'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Your complete address'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Age',
                'min': '18'
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'accept': 'image/*'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Describe your skills and how you can help (e.g., medical knowledge, teaching, cooking, etc.)'
            }),
            'availability': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., Weekends, Evenings, Full-time'
            }),
            'experience': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Any previous volunteer or relevant experience (optional)'
            }),
        }
        
        labels = {
            'full_name': 'Full Name *',
            'email': 'Email Address *',
            'phone_number': 'Phone Number *',
            'address': 'Address *',
            'age': 'Age *',
            'profile_photo': 'Profile Photo (for ID Card)',
            'skills': 'Skills & How You Can Help *',
            'availability': 'Availability *',
            'experience': 'Previous Experience',
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'donor_name', 'donor_email', 'donor_phone',
            'donation_type', 'description', 'message'
        ]
        
        widgets = {
            'donor_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Your full name'
            }),
            'donor_email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'your.email@example.com'
            }),
            'donor_phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '+91XXXXXXXXXX'
            }),
            'donation_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Describe what you want to donate (quantity, type, amount, etc.)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Any special message or delivery instructions (optional)'
            }),
        }
        
        labels = {
            'donor_name': 'Your Name *',
            'donor_email': 'Email Address *',
            'donor_phone': 'Phone Number *',
            'donation_type': 'Donation Type *',
            'description': 'Donation Details *',
            'message': 'Message/Instructions',
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'subject', 'message']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '+91XXXXXXXXXX'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Subject of your inquiry'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 5,
                'placeholder': 'Your message or inquiry'
            }),
        }
        
        labels = {
            'name': 'Full Name *',
            'email': 'Email Address *',
            'phone': 'Phone Number *',
            'subject': 'Subject *',
            'message': 'Message *',
        }

class RegistrationStatusForm(forms.Form):
    registration_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter Registration ID (e.g., VK2025-0001)'
        }),
        label='Registration ID'
    )

class VolunteerStatusForm(forms.Form):
    volunteer_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter Volunteer ID (e.g., VL2025-0001)'
        }),
        label='Volunteer ID'
    )