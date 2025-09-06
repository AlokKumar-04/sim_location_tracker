import requests
from django.conf import settings
from twilio.rest import Client
import phonenumbers
from phonenumbers import geocoder, carrier

class LocationService:
    def __init__(self):
        self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    def validate_phone_number(self, phone_number):
        """Validate and parse phone number"""
        try:
            parsed = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            pass
        return None
    
    def get_basic_info(self, phone_number):
        """Get basic info about phone number (carrier, country)"""
        try:
            parsed = phonenumbers.parse(phone_number, None)
            country = geocoder.description_for_number(parsed, "en")
            carrier_name = carrier.name_for_number(parsed, "en")
            country_code = phonenumbers.region_code_for_number(parsed)
            
            return {
                'country': country,
                'carrier': carrier_name,
                'country_code': country_code,
                'is_valid': phonenumbers.is_valid_number(parsed)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def verify_ownership(self, phone_number):
        """Send verification SMS to verify phone ownership"""
        try:
            verification = self.twilio_client.verify.v2.services(
                settings.TWILIO_VERIFY_SID
            ).verifications.create(to=phone_number, channel='sms')
            return {'status': 'sent', 'sid': verification.sid}
        except Exception as e:
            return {'error': str(e)}
    
    def check_verification(self, phone_number, code):
        """Check verification code"""
        try:
            verification_check = self.twilio_client.verify.v2.services(
                settings.TWILIO_VERIFY_SID
            ).verification_checks.create(to=phone_number, code=code)
            return verification_check.status == 'approved'
        except Exception as e:
            return False
    
    def get_location_mock(self, phone_number):
        """Mock location service - replace with real API"""
        # This is a mock implementation
        # Real implementation would use carrier APIs or location services
        mock_data = {
            'latitude': 40.7128,
            'longitude': -74.0060,
            'accuracy': 1000,
            'address': 'New York, NY, USA',
            'source': 'cell_tower'
        }
        return mock_data