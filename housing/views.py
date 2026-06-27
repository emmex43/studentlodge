from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import House, Subscriber
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm

# housing/views.py


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Construct the email
            full_message = f"New message from: {name} ({email})\n\nMessage:\n{message}"

            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=full_message,
                from_email='adminstudentlodge@gmail.com', # MUST MATCH your EMAIL_HOST_USER
                recipient_list=['adminstudentlodge@gmail.com'], # Where you want to receive it
                fail_silently=False,
            )

            messages.success(
                request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('housing:contact')  # Redirect to clear the form
    else:
        form = ContactForm()

    return render(request, 'housing/contact.html', {'form': form})


def home_feed(request):
    # Start by grabbing all available houses
    houses = House.objects.filter(is_available=True).order_by('-created_at')

    # Grab a list of all unique locations currently in the database
    # We use 'set' to remove any duplicates, so the dropdown looks clean
    all_locations = set(houses.values_list('location', flat=True))

    # Listen for data coming from the search bar (GET request)
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')

    # Filter 1: Keyword search in title OR description
    if query:
        houses = houses.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Filter 2: Exact location match from the dropdown
    if location:
        houses = houses.filter(location__iexact=location)

    # Pass the filtered houses and search terms back to the frontend
    context = {
        'houses': houses,
        'all_locations': all_locations,
        'query': query,
        'selected_location': location
    }
    return render(request, 'housing/home_feed.html', context)


# Add this new view:


def house_detail(request, id):
    # This safely looks for the house, and returns a 404 Error if it doesn't exist
    house = get_object_or_404(House, id=id)

    return render(request, 'housing/house_detail.html', {'house': house})

def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # get_or_create returns a tuple: (the object, a boolean if it was newly created)
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            
            # Only send the email if they are a brand new subscriber
            if created:
                try:
                    send_mail(
                        subject="Welcome to the Studentlodge Newsletter!",
                        message="Hi there,\n\nThank you for subscribing! We will keep you updated with the newest and most affordable accommodations right in your inbox.\n\nBest regards,\nThe Team",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                        fail_silently=False, 
                    )
                except Exception as e:
                    # If the email fails (e.g., no internet), we just print the error but still show the success message on the site
                    print(f"Error sending welcome email: {e}")
            
            # Display the UI banner
            messages.success(request, "Thanks for subscribing! We will keep you updated.")
            
    return redirect(request.META.get('HTTP_REFERER', 'housing:home_feed'))