from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('donate/', views.donate, name='donate'),
    path('volunteer-register/', views.volunteer_register, name='volunteer_register'),
    path('elder-register/', views.elder_register, name='elder_register'),
    path('contact/', views.contact, name='contact'),
    
    # Status Check URLs
    path('check-registration/', views.check_registration_status, name='check_registration_status'),
    path('check-volunteer/', views.check_volunteer_status, name='check_volunteer_status'),
    path('volunteer-id-card/<str:volunteer_id>/', views.volunteer_id_card, name='volunteer_id_card'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Elder Management
    path('admin/elders/', views.admin_elders, name='admin_elders'),
    path('admin/elder/<int:elder_id>/', views.admin_elder_detail, name='admin_elder_detail'),
    
    # Volunteer Management
    path('admin/volunteers/', views.admin_volunteers, name='admin_volunteers'),
    path('admin/volunteer/<int:volunteer_id>/', views.admin_volunteer_detail, name='admin_volunteer_detail'),
    
    # Donation Management
    path('admin/donations/', views.admin_donations, name='admin_donations'),
    path('admin/donation/<int:donation_id>/', views.admin_donation_detail, name='admin_donation_detail'),
    
    # Inquiry Management
    path('admin/inquiries/', views.admin_inquiries, name='admin_inquiries'),
    path('admin/inquiry/<int:inquiry_id>/', views.admin_inquiry_detail, name='admin_inquiry_detail'),

     
]