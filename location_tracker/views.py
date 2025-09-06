from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PhoneNumberSearch, LocationHistory
from .services import LocationService
import json

@login_required
def dashboard(request):
    searches = PhoneNumberSearch.objects.filter(user=request.user)[:10]
    return render(request, 'location_tracker/dashboard.html', {'searches': searches})

@method_decorator(csrf_exempt, name='dispatch')
class LocationSearchView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        consent = data.get('consent', False)
        
        if not phone_number:
            return JsonResponse({'error': 'Phone number required'}, status=400)
        
        if not consent:
            return JsonResponse({'error': 'User consent required'}, status=400)
        
        location_service = LocationService()
        
        # Validate phone number
        validated_number = location_service.validate_phone_number(phone_number)
        if not validated_number:
            return JsonResponse({'error': 'Invalid phone number'}, status=400)
        
        # Create search record
        search = PhoneNumberSearch.objects.create(
            user=request.user,
            phone_number=validated_number,
            consent_verified=consent,
            consent_method='web_form'
        )
        
        # Get basic info
        basic_info = location_service.get_basic_info(validated_number)
        if 'error' not in basic_info:
            search.carrier = basic_info.get('carrier', '')
            search.country_code = basic_info.get('country_code', '')
        
        # In a real implementation, you would:
        # 1. Send verification SMS
        # 2. Wait for user to verify ownership
        # 3. Then get location from carrier API
        
        # For demo purposes, using mock data
        location_data = location_service.get_location_mock(validated_number)
        
        search.latitude = location_data.get('latitude')
        search.longitude = location_data.get('longitude')
        search.accuracy = location_data.get('accuracy')
        search.address = location_data.get('address', '')
        search.status = 'completed'
        search.save()
        
        # Create history record
        LocationHistory.objects.create(
            search=search,
            latitude=location_data.get('latitude'),
            longitude=location_data.get('longitude'),
            source=location_data.get('source', 'mock')
        )
        
        return JsonResponse({
            'status': 'success',
            'search_id': search.id,
            'location': {
                'latitude': float(search.latitude),
                'longitude': float(search.longitude),
                'accuracy': search.accuracy,
                'address': search.address,
                'carrier': search.carrier
            }
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_search_result(request, search_id):
    search = get_object_or_404(PhoneNumberSearch, id=search_id, user=request.user)
    
    data = {
        'id': search.id,
        'phone_number': search.phone_number,
        'status': search.status,
        'created_at': search.created_at,
        'location': None
    }
    
    if search.status == 'completed' and search.latitude:
        data['location'] = {
            'latitude': float(search.latitude),
            'longitude': float(search.longitude),
            'accuracy': search.accuracy,
            'address': search.address,
            'carrier': search.carrier
        }
    
    return Response(data)