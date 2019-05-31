from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.new_trip),
    path('new/process', views.process_new_trip),
    path('<int:trip_id>', views.view_trip),
    path('edit', views.edit_trip),
    path('edit/process', views.process_edit_trip),
    path('<int:trip_id>/locations/new', views.new_location),
    path('<int:trip_id>/locations/new/process', views.process_new_location),
    path('<int:trip_id>/locations/edit/<int:loc_id>', views.edit_location),
    path('<int:trip_id>/locations/edit/<int:loc_id>/process', views.process_edit_location),
    path('<int:trip_id>/locations/delete/<int:loc_id>', views.delete_location),
    # path('trips/<int:trip_id>/locations/<int:loc_id>', views.view_location),
    # path('trips/<int:trip_id>/locations/<int:loc_id>', views.view_child_location),
    re_path(r'(?P<trip_id>[0-9]+)/(locations/(?P<loc_id>[0-9]+)/)*new$',
        views.new_child_location),
    re_path(r'(?P<trip_id>[0-9]+)/(locations/(?P<loc_id>[0-9]+)/)*new/process$',
        views.process_new_child_location),
    re_path(r'(?P<trip_id>[0-9]+)/(locations/[0-9]+/)*locations/(?P<loc_id>[0-9]+)$',
        views.view_location),

    path('<int:trip_id>/accomodations/new', views.new_accomodations),
    path('<int:trip_id>/locations/<int:loc_id>/pictures/add', views.add_location_picture),
    path('<int:trip_id>/locations/<int:loc_id>/pictures/add/process', views.process_add_location_picture),
    #http://localhost:8000/travels/trips/7/join
    path('<int:trip_id>/join/request', views.request_join_trip),
    path('<int:trip_id>/join/<int:req_id>/accept', views.accept_join_request),
    path('<int:trip_id>/join/<int:req_id>/reject', views.reject_join_request),
]