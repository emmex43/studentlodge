from django.db import models
from urllib.parse import quote
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError

# 1. AGENT MODEL
class Agent(models.Model):
    name = models.CharField(max_length=100)
    # WhatsApp number should include the country code without the '+' sign
    whatsapp_number = models.CharField(
        max_length=20,
        help_text="Format: 2348012345678 (No '+' or spaces)"
    )

    def __str__(self):
        return self.name

# housing/models.py

def validate_video_size(value):
    # Check if the incoming value is a new file with a 'size' attribute
    if hasattr(value, 'size'):
        filesize = value.size
        # Set limit to 10 Megabytes (10 * 1024 * 1024 bytes)
        limit_mb = 10 
        if filesize > limit_mb * 1024 * 1024:
            raise ValidationError(f"Maximum video size is {limit_mb}MB. Please compress your video.")
    
    # If it doesn't have a 'size' attribute, it's likely an already uploaded 
    # CloudinaryResource being edited, so we safely bypass the check.

# 2. HOUSE MODEL
class House(models.Model):
    title = models.CharField(
        max_length=200, help_text="e.g., 2-Bedroom Apartment in Ekosodin")
    description = models.TextField(
        help_text="Details about water, electricity, security, etc.")
    price = models.CharField(max_length=100, help_text="e.g., ₦150,000 / year")
    location = models.CharField(max_length=200, help_text="e.g., BDPA, Ugbowo")
    
    # Cloudinary Video Field
    video = CloudinaryField('video', resource_type='video',folder='studentlodge_videos/', validators=[validate_video_size])
    
    # Link the house to a specific agent
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='houses')
    
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Check if this is a brand new house (it won't have an ID yet)
        is_new = self.pk is None 
        
        # Save the house to the database first
        super().save(*args, **kwargs)
        
        # If it is a new house, send the update emails
        if is_new:
            # Grab all subscribers
            subscribers = Subscriber.objects.all()
            
            # Loop through them and send an email one by one to protect their privacy
            for sub in subscribers:
                try:
                    send_mail(
                        subject=f"New Listing: {self.title}",
                        message=f"Hi!\n\nWe just uploaded a new property on Studentlodge.ng.\n\nLocation: {self.location}\nPrice: {self.price}\n\nVisit the site to check out the video and contact the agent before it's gone!\n\nBest regards,\nThe Team",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[sub.email],
                        fail_silently=True, # Prevents your admin panel from crashing if an email fails
                    )
                except Exception as e:
                    print(f"Could not send email to {sub.email}: {e}")
    # --------------------------------
     
    def __str__(self):
        return f"{self.title} - {self.location}"

    @property
    def whatsapp_link(self):
        """Generates the direct WhatsApp click-to-chat URL with a pre-filled message."""
        base_url = f"https://wa.me/{self.agent.whatsapp_number}"
        message = f"Hello {self.agent.name}, I found your listing on the housing portal. Is the {self.title} at {self.location} still available?"
        encoded_message = quote(message)
        return f"{base_url}?text={encoded_message}"


# housing/models.py
# (Ensure send_mail and settings are imported at the top of the file, which they should be based on your previous code)

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # 1. Check if this is a new subscriber before saving
        is_new = self.pk is None
        
        # 2. Save the subscriber to the database
        super().save(*args, **kwargs)
        
        # 3. If they are new, send them a welcome email
        if is_new:
            try:
                send_mail(
                    subject="Welcome to the Studentlodge Newsletter!",
                    message="Hi there,\n\nThank you for subscribing to Studentlodge! You will now be the first to know when we upload new, affordable accommodations.\n\nBest regards,\nThe Studentlodge Team",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[self.email],
                    fail_silently=True, 
                )
            except Exception as e:
                # This prints to your Render server logs if it fails, making debugging easy
                print(f"Could not send welcome email to {self.email}: {e}")