# housing/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.paginator import Paginator
from .models import SavedListing
from anymail.exceptions import AnymailAPIError
from .models import House, Subscriber, SavedListing 
from .forms import ContactForm
from django.contrib.auth.decorators import login_required



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            user_email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            full_message = f"New message from: {name} ({user_email})\n\nMessage:\n{message}"

            # Hardcoding the from_email guarantees Brevo receives the sender parameter
            email_msg = EmailMessage(
                subject=f"New Contact Form Submission from {name}",
                body=full_message,
                from_email='admin@studentlodge.com.ng',  
                to=['adminstudentlodge@gmail.com'],
                reply_to=[user_email],
            )

            email_msg.send(fail_silently=False)

            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('housing:contact')
    else:
        form = ContactForm()

    return render(request, 'housing/contact.html', {'form': form})


def home_feed(request):
    houses = House.objects.filter(is_available=True).order_by('-created_at')
    all_locations = set(houses.values_list('location', flat=True))

    query = request.GET.get('q', '')
    location = request.GET.get('location', '')

    if query:
        houses = houses.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if location:
        houses = houses.filter(location__iexact=location)


 # --- Fetch Saved House IDs ---
    saved_house_ids = []  # Changed from set() to an empty list
    if request.user.is_authenticated:
        try:
            student_profile = request.user.studentprofile
            # Wrapping with list() gives the Django template a structure it natively understands
            saved_house_ids = list(
                SavedListing.objects.filter(student=student_profile).values_list('listing_id', flat=True)
            )
        except Exception:
            saved_house_ids = []

    # --- PAGINATION LOGIC ---
    paginator = Paginator(houses, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  
        'all_locations': all_locations,
        'query': query,
        'selected_location': location
    }
    return render(request, 'housing/home_feed.html', context)


def house_detail(request, id):
    house = get_object_or_404(House, id=id)
    return render(request, 'housing/house_detail.html', {'house': house})


def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            if created:
                context = {
                    'website_url': 'https://studentlodge.com.ng/',
                }

                html_content = render_to_string('housing/welcome_email.html', context)
                text_content = "Welcome to Studentlodge! Thank you for subscribing. We will keep you updated on the best accommodations around campus."

                msg = EmailMultiAlternatives(
                    subject="Welcome to the Studentlodge Community! 🎓",
                    body=text_content,
                    from_email='admin@studentlodge.com.ng',
                    to=[email]
                )
                msg.attach_alternative(html_content, "text/html")

                try:
                    msg.send(fail_silently=False)
                except AnymailAPIError as e:
                    print(f"Brevo API Error sending welcome email: {e}")

            messages.success(request, "Thanks for subscribing! We will keep you updated.")

    return redirect(request.META.get('HTTP_REFERER', 'housing:home_feed'))

@require_POST
def toggle_save_listing(request, house_id):
    """
    Toggles a listing's saved state. Safely handles unauthenticated users 
    by returning a 401 Unauthorized JSON response.
    """
    # 1. Manually check if the user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'unauthorized', 'message': 'Please sign in to save listings.'}, status=401)

    try:
        # 2. Get the currently logged-in student's profile
        student_profile = request.user.studentprofile
        house = get_object_or_404(House, id=house_id)
        
        # 3. Check if the save record already exists
        saved_record = SavedListing.objects.filter(student=student_profile, listing=house).first()
        
        if saved_record:
            saved_record.delete()
            return JsonResponse({'status': 'unsaved', 'message': 'Removed from saved listings.'})
        else:
            SavedListing.objects.create(student=student_profile, listing=house)
            return JsonResponse({'status': 'saved', 'message': 'Listing saved successfully.'})
            
    except House.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Listing not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def saved_listings_view(request):
    """
    Retrieves all the properties saved by the logged-in student 
    and passes them to the saved listings template.
    """
    # Get the current student's profile
    student_profile = request.user.studentprofile
    
    # Fetch all their saved records from the database
    saved_records = SavedListing.objects.filter(student=student_profile).select_related('listing').order_by('-saved_at')
    
    # Pass the data to the HTML template
    context = {
        'saved_records': saved_records
    }
    return render(request, 'housing/saved_listings.html', context)




      