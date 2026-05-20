from django.shortcuts import render
from django.db.models import Q
from .models import House


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
