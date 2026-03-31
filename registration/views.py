from django.http import JsonResponse
from .models import UserRegistration, VehicleApplication
import json
from django.views.decorators.csrf import csrf_exempt

# --- HELPER TO PREVENT 500 ERRORS ---
def get_val(data, key_camel, key_snake):
    """Checks for both camelCase (React) and snake_case (Django) keys"""
    return data.get(key_camel) or data.get(key_snake)

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            UserRegistration.objects.create(
                first_name=get_val(data, 'firstName', 'first_name'),
                last_name=get_val(data, 'lastName', 'last_name'),
                email=data.get('email'),
                username=data.get('username'),
                password=data.get('password'),
                identifier=data.get('identifier'),
                role=data.get('role')
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"REGISTRATION ERROR: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@csrf_exempt
def submit_vehicle(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Match React keys to your Django Model fields
            VehicleApplication.objects.create(
                applicant_username=data.get('username'),
                owner_name=get_val(data, 'ownerName', 'owner_name'),
                plate_number=get_val(data, 'plateNumber', 'plate_number'),
                vehicle_type=get_val(data, 'vehicleType', 'vehicle_type'),
                status="Pending",
                is_seen=True  # Ensure this is included!
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            # THIS PRINT IS YOUR BEST FRIEND
            # Check the black terminal window to see the error!
            print(f"CRITICAL SUBMIT ERROR: {e}") 
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            v = VehicleApplication.objects.get(id=data.get('id'))
            v.status = data.get('status')
            
            # TRIGGER: Mark as unseen so the user gets the notification bell red dot
            v.is_seen = False  
            
            if v.status == "Approved" and not v.sticker_id:
                count = VehicleApplication.objects.filter(status="Approved").count() + 1
                v.sticker_id = f"UA-{str(count).zfill(3)}"
            
            v.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"UPDATE ERROR: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def mark_notifications_read(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_nm = data.get('username')
            # Update all notifications for this user to 'seen'
            VehicleApplication.objects.filter(applicant_username=user_nm).update(is_seen=True)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"NOTIF READ ERROR: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def get_admin_records(request):
    try:
        vehicles = list(VehicleApplication.objects.all().values())
        return JsonResponse(vehicles, safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)

def get_user_records(request):
    try:
        user_nm = request.GET.get('username')
        if not user_nm:
            return JsonResponse([], safe=False)
        
        vehicles = list(VehicleApplication.objects.filter(applicant_username=user_nm).values())
        return JsonResponse(vehicles, safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)