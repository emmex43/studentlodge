from django.db import models
from urllib.parse import quote
from cloudinary.models import CloudinaryField


class Agent(models.Model):
    name = models.CharField(max_length=100)
    # WhatsApp number should include the country code without the '+' sign
    whatsapp_number = models.CharField(
        max_length=20,
        help_text="Format: 2348012345678 (No '+' or spaces)"
    )

    def __str__(self):
        return self.name


class House(models.Model):
    title = models.CharField(
        max_length=200, help_text="e.g., 2-Bedroom Apartment in Ekosodin")
    description = models.TextField(
        help_text="Details about water, electricity, security, etc.")
    price = models.CharField(max_length=100, help_text="e.g., ₦150,000 / year")
    location = models.CharField(max_length=200, help_text="e.g., BDPA, Ugbowo")

    # We will upload videos to a specific folder.
    # Later, we will configure this to use Cloudinary or AWS S3 for production.
    # We tell Cloudinary specifically to expect a 'video' resource
    video = CloudinaryField('video', resource_type='video',
                            folder='studentlodge_videos/')
    # Link the house to a specific agent
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name='houses')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"

    @property
    def whatsapp_link(self):
        """Generates the direct WhatsApp click-to-chat URL with a pre-filled message."""
        base_url = f"https://wa.me/{self.agent.whatsapp_number}"
        message = f"Hello {self.agent.name}, I found your listing on the housing portal. Is the {self.title} at {self.location} still available?"
        encoded_message = quote(message)
        return f"{base_url}?text={encoded_message}"
