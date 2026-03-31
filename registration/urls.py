from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user), # This will now find the function!
    path('admin-records/', views.get_admin_records),
    path('user-records/', views.get_user_records),
    path('update-status/', views.update_status),
    path('submit-vehicle/', views.submit_vehicle),
    path('mark-notifications-read/', views.mark_notifications_read),
]