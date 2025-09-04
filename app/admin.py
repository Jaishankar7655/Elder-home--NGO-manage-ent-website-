from django.contrib import admin
from django.utils.html import format_html
from .models import Elder, Volunteer, Donation, Testimonial, ContactInquiry

@admin.register(Elder)
class ElderAdmin(admin.ModelAdmin):
    list_display = ['registration_id', 'full_name', 'age', 'status', 'guardian_name', 'created_at']
    list_filter = ['status', 'created_at', 'age']
    search_fields = ['registration_id', 'full_name', 'guardian_name', 'phone_number']
    readonly_fields = ['registration_id', 'created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Registration Info', {
            'fields': ('registration_id', 'status', 'rejection_reason')
        }),
        ('Personal Information', {
            'fields': ('full_name', 'photo', 'age', 'address', 'phone_number', 'id_proof')
        }),
        ('Guardian Information', {
            'fields': ('guardian_name', 'guardian_contact', 'guardian_relationship')
        }),
        ('Health Information', {
            'fields': ('health_conditions', 'special_requirements')
        }),
        ('Approval Info', {
            'fields': ('approved_at', 'approved_by'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # Editing existing object
            readonly.extend(['photo', 'id_proof'])  # Admin cannot change uploaded files
        return readonly
    
    actions = ['approve_elders', 'reject_elders']
    
    def approve_elders(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} elders approved successfully.')
    approve_elders.short_description = "Approve selected elders"
    
    def reject_elders(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} elders rejected.')
    reject_elders.short_description = "Reject selected elders"
from django.contrib import admin
from django.utils.html import format_html
from .models import Elder, Volunteer, Donation, Testimonial, ContactInquiry

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['volunteer_id', 'full_name', 'email', 'status', 'availability', 'created_at', 'profile_photo_preview']
    list_filter = ['status', 'created_at']
    search_fields = ['volunteer_id', 'full_name', 'email', 'phone_number']
    readonly_fields = ['volunteer_id', 'created_at', 'updated_at', 'profile_photo_preview']
    list_per_page = 25
    
    fieldsets = (
        ('Registration Info', {
            'fields': ('volunteer_id', 'status', 'rejection_reason')
        }),
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone_number', 'address', 'age', 'profile_photo', 'profile_photo_preview')
        }),
        ('Volunteer Information', {
            'fields': ('skills', 'availability', 'experience')
        }),
        ('Approval Info', {
            'fields': ('approved_at', 'approved_by'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def profile_photo_preview(self, obj):
        if obj.profile_photo:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.profile_photo.url)
        return "No photo"
    profile_photo_preview.short_description = 'Profile Photo Preview'
    
    actions = ['approve_volunteers', 'reject_volunteers']
    
    def approve_volunteers(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} volunteers approved successfully.')
    approve_volunteers.short_description = "Approve selected volunteers"
    
    def reject_volunteers(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} volunteers rejected.')
    reject_volunteers.short_description = "Reject selected volunteers"

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'donation_type', 'status', 'created_at', 'donor_phone']
    list_filter = ['donation_type', 'status', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'donor_phone', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone')
        }),
        ('Donation Details', {
            'fields': ('donation_type', 'description', 'message')
        }),
        ('Status', {
            'fields': ('status', 'fulfilled_at', 'fulfilled_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_fulfilled', 'mark_pending']
    
    def mark_fulfilled(self, request, queryset):
        updated = queryset.update(status='fulfilled')
        self.message_user(request, f'{updated} donations marked as fulfilled.')
    mark_fulfilled.short_description = "Mark selected donations as fulfilled"
    
    def mark_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} donations marked as pending.')
    mark_pending.short_description = "Mark selected donations as pending"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'relationship', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'relationship', 'comment']
    readonly_fields = ['created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Testimonial Info', {
            'fields': ('name', 'relationship', 'rating', 'comment')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_testimonials', 'deactivate_testimonials']
    
    def activate_testimonials(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} testimonials activated.')
    activate_testimonials.short_description = "Activate selected testimonials"
    
    def deactivate_testimonials(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} testimonials deactivated.')
    deactivate_testimonials.short_description = "Deactivate selected testimonials"

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'is_resolved', 'created_at']
    list_filter = ['is_resolved', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Contact Info', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_resolved',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_resolved', 'mark_unresolved']
    
    def mark_resolved(self, request, queryset):
        updated = queryset.update(is_resolved=True)
        self.message_user(request, f'{updated} inquiries marked as resolved.')
    mark_resolved.short_description = "Mark selected inquiries as resolved"
    
    def mark_unresolved(self, request, queryset):
        updated = queryset.update(is_resolved=False)
        self.message_user(request, f'{updated} inquiries marked as unresolved.')
    mark_unresolved.short_description = "Mark selected inquiries as unresolved"

# Customize admin site headers
admin.site.site_header = "Vrudhashram Kamalbasant Admin"
admin.site.site_title = "VK Admin Portal"
admin.site.index_title = "Welcome to Vrudhashram Kamalbasant Administration"