from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.db.models import Count, Q
from django.utils import timezone
from django.template.loader import get_template
from django.core.paginator import Paginator
from .models import Elder, Volunteer, Donation, Testimonial, ContactInquiry
from .forms import (
    ElderRegistrationForm, VolunteerRegistrationForm, DonationForm,
    ContactForm, RegistrationStatusForm, VolunteerStatusForm
)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import os

from django.http import JsonResponse
from .models import Volunteer


def home(request):
    """Home page with overview and statistics"""
    # Get statistics
    total_elders = Elder.objects.count()
    approved_elders = Elder.objects.filter(status='approved').count()
    active_volunteers = Volunteer.objects.filter(status='approved').count()
    total_donations = Donation.objects.count()
    
    # Get recent testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    context = {
        'total_elders': total_elders,
        'approved_elders': approved_elders,
        'active_volunteers': active_volunteers,
        'total_donations': total_donations,
        'testimonials': testimonials,
    }
    return render(request, 'app/home.html', context)

def about(request):
    """About page with mission, vision, and team information"""
    return render(request, 'app/about.html')

def testimonials_view(request):
    """Testimonials page with all reviews"""
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(testimonials, 12)  # Show 12 testimonials per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'testimonials': page_obj,
    }
    return render(request, 'app/testimonials.html', context)

def donate(request):
    """Donation page with form"""
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your donation! We will contact you soon.')
            return redirect('donate')
    else:
        form = DonationForm()
    
    return render(request, 'app/donate.html', {'form': form})

def volunteer_register(request):
    """Volunteer registration page"""
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            volunteer = form.save()
            messages.success(
                request, 
                f'Registration successful! Your Volunteer ID is {volunteer.volunteer_id}. '
                'We will review your application and contact you soon.'
            )
            return redirect('volunteer_register')
    else:
        form = VolunteerRegistrationForm()
    
    return render(request, 'app/volunteer_register.html', {'form': form})

def elder_register(request):
    """Elder registration page"""
    if request.method == 'POST':
        form = ElderRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            elder = form.save()
            messages.success(
                request,
                f'Registration successful! Registration ID: {elder.registration_id}. '
                'Please save this ID for future reference. We will review the application and contact you soon.'
            )
            return redirect('elder_register')
    else:
        form = ElderRegistrationForm()
    
    return render(request, 'app/elder_register.html', {'form': form})

def contact(request):
    """Contact page with form and location"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'app/contact.html', {'form': form})

def check_registration_status(request):
    """Check elder registration status by ID"""
    elder = None
    if request.method == 'POST':
        form = RegistrationStatusForm(request.POST)
        if form.is_valid():
            registration_id = form.cleaned_data['registration_id']
            try:
                elder = Elder.objects.get(registration_id__iexact=registration_id)
            except Elder.DoesNotExist:
                messages.error(request, 'Registration ID not found. Please check and try again.')
    else:
        form = RegistrationStatusForm()
    
    return render(request, 'app/check_status.html', {'form': form, 'elder': elder})

def check_volunteer_status(request):
    """Check volunteer registration status by ID"""
    volunteer = None
    if request.method == 'POST':
        form = VolunteerStatusForm(request.POST)
        if form.is_valid():
            volunteer_id = form.cleaned_data['volunteer_id']
            try:
                volunteer = Volunteer.objects.get(volunteer_id__iexact=volunteer_id)
            except Volunteer.DoesNotExist:
                messages.error(request, 'Volunteer ID not found. Please check and try again.')
    else:
        form = VolunteerStatusForm()
    
    return render(request, 'app/check_volunteer_status.html', {'form': form, 'volunteer': volunteer})


def volunteer_id_card(request, volunteer_id):
    """Generate PDF ID card for approved volunteers with robust error handling"""
    volunteer = get_object_or_404(Volunteer, volunteer_id=volunteer_id)
    
    if volunteer.status != 'approved':
        messages.error(request, 'ID card can only be generated for approved volunteers.')
        return redirect('check_volunteer_status')
    
    # Create PDF with ID card dimensions
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, 
                          pagesize=(3.375*inch, 2.125*inch),
                          leftMargin=0.2*inch,
                          rightMargin=0.2*inch,
                          topMargin=0.2*inch,
                          bottomMargin=0.2*inch)
    
    # Define styles
    styles = getSampleStyleSheet()
    org_style = ParagraphStyle(
        'OrgStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,
        textColor=colors.darkblue,
        spaceAfter=6,
    )
    
    # Build content
    content = []
    
    # Organization header
    content.append(Paragraph("VRUDHASHRAM KAMALBASANT", org_style))
    content.append(Paragraph("VOLUNTEER ID CARD", org_style))
    content.append(Spacer(1, 5))
    
    # Create a table for the ID card
    id_data = []
    
    # Photo row
    if volunteer.profile_photo:
        try:
            img = Image(volunteer.profile_photo.path, width=0.8*inch, height=1*inch)
            id_data.append([img])
        except Exception as e:
            id_data.append([Paragraph("Photo Not Available", styles['Normal'])])
    else:
        id_data.append([Paragraph("Photo Not Available", styles['Normal'])])
    
    # Details rows
    id_data.append([Paragraph(f"<b>{volunteer.full_name}</b>", styles['Normal'])])
    id_data.append([Paragraph(f"ID: {volunteer.volunteer_id}", styles['Normal'])])
    id_data.append([Paragraph(f"Phone: {volunteer.phone_number}", styles['Normal'])])
    
    if volunteer.approved_at:
        id_data.append([Paragraph(f"Member Since: {volunteer.approved_at.strftime('%Y')}", styles['Normal'])])
    
    # Create ID card table
    id_table = Table(id_data)
    id_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    content.append(id_table)
    content.append(Spacer(1, 10))
    
    # Footer
    content.append(Paragraph("Authorized Signature", styles['Normal']))
    content.append(Paragraph("Valid until further notice", styles['Normal']))
    
    # Build PDF
    doc.build(content)
    buffer.seek(0)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="volunteer_id_{volunteer_id}.pdf"'
    response.write(buffer.getvalue())
    buffer.close()
    
    return response

@login_required
def admin_dashboard(request):
    """Admin dashboard with statistics and quick actions"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    # Statistics
    stats = {
        'total_elders': Elder.objects.count(),
        'pending_elders': Elder.objects.filter(status='pending').count(),
        'approved_elders': Elder.objects.filter(status='approved').count(),
        'rejected_elders': Elder.objects.filter(status='rejected').count(),
        
        'total_volunteers': Volunteer.objects.count(),
        'pending_volunteers': Volunteer.objects.filter(status='pending').count(),
        'approved_volunteers': Volunteer.objects.filter(status='approved').count(),
        'rejected_volunteers': Volunteer.objects.filter(status='rejected').count(),
        
        'total_donations': Donation.objects.count(),
        'pending_donations': Donation.objects.filter(status='pending').count(),
        'fulfilled_donations': Donation.objects.filter(status='fulfilled').count(),
        
        'total_inquiries': ContactInquiry.objects.count(),
        'unresolved_inquiries': ContactInquiry.objects.filter(is_resolved=False).count(),
    }
    
    # Recent activities
    recent_elders = Elder.objects.filter(status='pending')[:5]
    recent_volunteers = Volunteer.objects.filter(status='pending')[:5]
    recent_donations = Donation.objects.filter(status='pending')[:5]
    
    context = {
        'stats': stats,
        'recent_elders': recent_elders,
        'recent_volunteers': recent_volunteers,
        'recent_donations': recent_donations,
    }
    
    return render(request, 'app/dashboard.html', context)

@login_required
def admin_elders(request):
    """Admin view for managing elder registrations"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    elders = Elder.objects.all()
    
    if status_filter != 'all':
        elders = elders.filter(status=status_filter)
    
    if search_query:
        elders = elders.filter(
            Q(registration_id__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(guardian_name__icontains=search_query)
        )
    
    elders = elders.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(elders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'elders': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'app/admin/elders.html', context)

@login_required
def admin_elder_detail(request, elder_id):
    """Admin view for elder details and approval/rejection"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    elder = get_object_or_404(Elder, id=elder_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            elder.status = 'approved'
            elder.approved_at = timezone.now()
            elder.approved_by = request.user
            elder.rejection_reason = ''
            elder.save()
            messages.success(request, f'Elder registration {elder.registration_id} has been approved.')
        
        elif action == 'reject':
            reason = request.POST.get('rejection_reason', '')
            if reason:
                elder.status = 'rejected'
                elder.rejection_reason = reason
                elder.approved_at = None
                elder.approved_by = None
                elder.save()
                messages.success(request, f'Elder registration {elder.registration_id} has been rejected.')
            else:
                messages.error(request, 'Please provide a reason for rejection.')
        
        return redirect('admin_elder_detail', elder_id=elder.id)
    
    return render(request, 'app/admin/elder_detail.html', {'elder': elder})

@login_required
def admin_volunteers(request):
    """Admin view for managing volunteer registrations"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    volunteers = Volunteer.objects.all()
    
    if status_filter != 'all':
        volunteers = volunteers.filter(status=status_filter)
    
    if search_query:
        volunteers = volunteers.filter(
            Q(volunteer_id__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    volunteers = volunteers.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(volunteers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'volunteers': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'app/admin/volunteers.html', context)

@login_required
def admin_volunteer_detail(request, volunteer_id):
    """Admin view for volunteer details and approval/rejection"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            volunteer.status = 'approved'
            volunteer.approved_at = timezone.now()
            volunteer.approved_by = request.user
            volunteer.rejection_reason = ''
            volunteer.save()
            messages.success(request, f'Volunteer registration {volunteer.volunteer_id} has been approved.')
        
        elif action == 'reject':
            reason = request.POST.get('rejection_reason', '')
            if reason:
                volunteer.status = 'rejected'
                volunteer.rejection_reason = reason
                volunteer.approved_at = None
                volunteer.approved_by = None
                volunteer.save()
                messages.success(request, f'Volunteer registration {volunteer.volunteer_id} has been rejected.')
            else:
                messages.error(request, 'Please provide a reason for rejection.')
        
        return redirect('admin_volunteer_detail', volunteer_id=volunteer.id)
    
    return render(request, 'app/admin/volunteer_detail.html', {'volunteer': volunteer})

@login_required
def admin_donations(request):
    """Admin view for managing donations"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    status_filter = request.GET.get('status', 'all')
    type_filter = request.GET.get('type', 'all')
    search_query = request.GET.get('search', '')
    
    donations = Donation.objects.all()
    
    if status_filter != 'all':
        donations = donations.filter(status=status_filter)
        
    if type_filter != 'all':
        donations = donations.filter(donation_type=type_filter)
    
    if search_query:
        donations = donations.filter(
            Q(donor_name__icontains=search_query) |
            Q(donor_email__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    donations = donations.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(donations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'donations': page_obj,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'search_query': search_query,
        'donation_types': Donation.DONATION_TYPES,
    }
    
    return render(request, 'app/admin/donations.html', context)

@login_required
def admin_donation_detail(request, donation_id):
    """Admin view for donation details and status update"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    donation = get_object_or_404(Donation, id=donation_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'fulfill':
            donation.status = 'fulfilled'
            donation.fulfilled_at = timezone.now()
            donation.fulfilled_by = request.user
            donation.save()
            messages.success(request, 'Donation marked as fulfilled.')
        
        elif action == 'cancel':
            donation.status = 'cancelled'
            donation.save()
            messages.success(request, 'Donation marked as cancelled.')
        
        elif action == 'pending':
            donation.status = 'pending'
            donation.fulfilled_at = None
            donation.fulfilled_by = None
            donation.save()
            messages.success(request, 'Donation marked as pending.')
        
        return redirect('admin_donation_detail', donation_id=donation.id)
    
    return render(request, 'app/admin/donation_detail.html', {'donation': donation})

@login_required
def admin_inquiries(request):
    """Admin view for managing contact inquiries"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    resolved_filter = request.GET.get('resolved', 'all')
    search_query = request.GET.get('search', '')
    
    inquiries = ContactInquiry.objects.all()
    
    if resolved_filter == 'resolved':
        inquiries = inquiries.filter(is_resolved=True)
    elif resolved_filter == 'unresolved':
        inquiries = inquiries.filter(is_resolved=False)
    
    if search_query:
        inquiries = inquiries.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    inquiries = inquiries.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(inquiries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'inquiries': page_obj,
        'resolved_filter': resolved_filter,
        'search_query': search_query,
    }
    
    return render(request, 'app/admin/inquiries.html', context)

@login_required
def admin_inquiry_detail(request, inquiry_id):
    """Admin view for inquiry details and resolution"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    inquiry = get_object_or_404(ContactInquiry, id=inquiry_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'resolve':
            inquiry.is_resolved = True
            inquiry.save()
            messages.success(request, 'Inquiry marked as resolved.')
        
        elif action == 'unresolve':
            inquiry.is_resolved = False
            inquiry.save()
            messages.success(request, 'Inquiry marked as unresolved.')
        
        return redirect('admin_inquiry_detail', inquiry_id=inquiry.id)
    
    return render(request, 'app/admin/inquiry_detail.html', {'inquiry': inquiry})



