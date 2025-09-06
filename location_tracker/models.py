from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class PhoneNumberSearch(models.Model):
    SEARCH_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('unauthorized', 'Unauthorized'),
    ]
    
    phone_regex = RegexValidator(
    regex=r'^(?:\+91|91|0)?[6-9]\d{9}$',
    message="Enter a valid Indian phone number (10 digits, may start with +91, 91, or 0).")
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    status = models.CharField(max_length=20, choices=SEARCH_STATUS, default='pending')
    
    # Location data
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    accuracy = models.IntegerField(null=True, blank=True, help_text="Accuracy in meters")
    address = models.TextField(blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    country_code = models.CharField(max_length=3, blank=True)
    
    # Consent and legal
    consent_verified = models.BooleanField(default=False)
    consent_method = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.phone_number} - {self.status}"


class LocationHistory(models.Model):
    search = models.ForeignKey(PhoneNumberSearch, on_delete=models.CASCADE, related_name='history')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50)  # 'carrier_api', 'gps', 'wifi', etc.
    
    def __str__(self):
        return f"{self.search.phone_number} at {self.timestamp}"