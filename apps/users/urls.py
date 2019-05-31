from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<int:id>', views.view_user),
    path('profiles', views.view_profile),
    path('friends', views.view_friends),
    path('friends/<int:friend_id>', views.view_friend_profile),
    path('friends/<int:friend_id>/request', views.send_friend_request),
    path('friends/accept/<int:req_id>', views.accept_friend_request),
    path('friends/cancel/<int:req_id>', views.cancel_friend_request),
    path('avatars', views.upload_avatar),
    path('avatars/process', views.process_upload_avatar),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)