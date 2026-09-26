# housing/views.py
from django.shortcuts import render, get_object_or_404, redirect
# housing/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import House, Subscriber
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import ContactForm
from django.core.paginator import Paginator
from anymail.exceptions import AnymailAPIError
from anymail.exceptions import AnymailAPIError


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            user_email = form.cleaned_data['email']
            user_email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            full_message = f"New message from: {name} ({user_email})\n\nMessage:\n{message}"
            full_message = f"New message from: {name} ({user_email})\n\nMessage:\n{message}"

            # Hardcoding the from_email guarantees Brevo receives the sender parameter
            email_msg = EmailMessage(
            # Hardcoding the from_email guarantees Brevo receives the sender parameter
            email_msg = EmailMessage(
                subject=f"New Contact Form Submission from {name}",
                body=full_message,
                from_email='admin@studentlodge.com.ng',  
                to=['adminstudentlodge@gmail.com'],
                reply_to=[user_email],
            )

            email_msg.send(fail_silently=False)
                body=full_message,
                from_email='admin@studentlodge.com.ng',  
                to=['adminstudentlodge@gmail.com'],
                reply_to=[user_email],
            )

            email_msg.send(fail_silently=False)

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

    # --- PAGINATION LOGIC ---
    # --- PAGINATION LOGIC ---
    # Paginate the filtered houses (6 per page)
    paginator = Paginator(houses, 6)
    paginator = Paginator(houses, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass the paginated objects (page_obj) and search terms back to the frontend
    context = {
        'page_obj': page_obj,  
        'page_obj': page_obj,  
        'all_locations': all_locations,
        'query': query,
        'selected_location': location
    }
    return render(request, 'housing/home_feed.html', context)


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

            # Only send the beautifully formatted HTML email if they are a brand new subscriber

            # Only send the beautifully formatted HTML email if they are a brand new subscriber
            if created:
                # Prepare dynamic context for the template
                context = {
                    'website_url': 'https://studentlodge.com.ng/',
                }

                # Render the HTML and define the plain text fallback
                html_content = render_to_string('housing/welcome_email.html', context)
                text_content = "Welcome to Studentlodge! Thank you for subscribing. We will keep you updated on the best accommodations around campus."

                # Construct the multipart message
                msg = EmailMultiAlternatives(
                    subject="Welcome to the Studentlodge Community! 🎓",
                    body=text_content,
                    from_email='admin@studentlodge.com.ng',
                    to=[email]
                )
                msg.attach_alternative(html_content, "text/html")

                try:
                    # Send safely with the Brevo Anymail integration
                    msg.send(fail_silently=False)
                except AnymailAPIError as e:
                    # If Brevo drops the message, it prints to Render logs for debugging
                    print(f"Brevo API Error sending welcome email: {e}")

            # Display the UI banner regardless of whether they were newly created or already existed
            messages.success(
                request, "Thanks for subscribing! We will keep you updated.")

    # Redirect back to exactly where the user was when they submitted the form
                # Prepare dynamic context for the template
                context = {
                    'website_url': 'https://studentlodge.com.ng/',
                }

                # Render the HTML and define the plain text fallback
                html_content = render_to_string('housing/welcome_email.html', context)
                text_content = "Welcome to Studentlodge! Thank you for subscribing. We will keep you updated on the best accommodations around campus."

                # Construct the multipart message
                msg = EmailMultiAlternatives(
                    subject="Welcome to the Studentlodge Community! 🎓",
                    body=text_content,
                    from_email='admin@studentlodge.com.ng',
                    to=[email]
                )
                msg.attach_alternative(html_content, "text/html")

                try:
                    # Send safely with the Brevo Anymail integration
                    msg.send(fail_silently=False)
                except AnymailAPIError as e:
                    # If Brevo drops the message, it prints to Render logs for debugging
                    print(f"Brevo API Error sending welcome email: {e}")

            # Display the UI banner regardless of whether they were newly created or already existed
            messages.success(
                request, "Thanks for subscribing! We will keep you updated.")

    # Redirect back to exactly where the user was when they submitted the form
    return redirect(request.META.get('HTTP_REFERER', 'housing:home_feed'))
