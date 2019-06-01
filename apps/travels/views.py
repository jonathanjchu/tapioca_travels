from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from .models import *
from .forms import *
from apps.users.models import *


# Create your views here.
def index(request):
    user = User.objects.get(id=request.session['id'])
    trips = Trip.objects.filter(Q(created_by=user) | Q(companions=user))\
        .filter(start_date__gt=datetime.now())\
        .distinct()
    
    past_trips = Trip.objects.filter(Q(created_by=user) | Q(companions=user))\
        .filter(start_date__lte=datetime.now())\
        .distinct()

    
    context = {
        'user': user,
        'trips': trips,
        'past_trips': past_trips,
    }
    
    return render(request, "travels/index.html", context)

'''
TRIPS
'''

def new_trip(request):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        return render(request, "travels/trips/new_trip.html", { 'user': user })
    else:
        return redirect("/logout")


def process_new_trip(request):
    if request.method == "POST":
        results = Trip.objects.validate(request.POST)
        if results:
            for key, val in results.items():
                messages.error(request, val, key)
            return redirect("/travels/new")
        else:
            # print(request.POST)

            user = User.objects.get(id=request.session['id'])
            trip = Trip.objects.create(name=request.POST['name'],
                                        start_date=request.POST['trip_start'],
                                        end_date=request.POST['trip_end'],
                                        is_private=request.POST.get('is_private', '') == 'on',
                                        created_by=user)
            
            return redirect(f"/travels/{trip.id}")

    return redirect("/travels")


def view_trip(request, trip_id):
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=trip_id)
    treqs = TripJoinRequest.objects.filter(trip=trip, is_pending=True)
    accomodations = Accomodations.objects.filter(trip=trip)
    trans = Transportation.objects.filter(trip=trip)

    context = {
        'trip': trip,
        'user': user,
        'join_requests': treqs,
        'accomodations': accomodations,
        'trans': trans,
    }
    return render(request, "travels/trips/view_trip.html", context)

def edit_trip(request):
    return render(request, "travels/trips/edit_trip.html")


def process_edit_trip(request, trip_id):
    return redirect(f"/travels/{trip_id}/edit")

'''
LOCATIONS
'''

def view_location(request, trip_id, loc_id):
    ancestry = bread_crumbs(loc_id)
    trip = Trip.objects.get(id=trip_id)
    loc = Location.objects.get(id=loc_id)
    user = get_user(request)

    context = {
        'location': loc,
        'bread_crumbs': ancestry,
        'trip': trip,
        'user': user,
    }
    return render(request, "travels/locations/view_location.html", context)

# def new_location(request, trip_id):
#     user = User.objects.get(id=request.session['id'])
#     parent_locations = Location.objects.filter(id=loc_id)
#     trip = Trip.objects.get(id=trip_id)

#     if parent_locations:
#         parent_location = parent_locations.first()
#     else:
#         parent_location = None

#     context = {
#         'trip': trip,
#         'parent': parent_location,
#         'user': user,
#         'action': f"/travels/{trip.id}/locations/{loc_id}/new/process",
#     }

#     return render(request, "travels/locations/new_location.html", context)


def new_location(request, trip_id, loc_id=None):
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=trip_id)

    parent_location = None
    action = f"/travels/{trip.id}/locations/new/process"
    if loc_id:
        parent_locations = Location.objects.filter(id=loc_id)

        if parent_locations:
            parent_location = parent_locations.first()
            action = f"/travels/{trip.id}/locations/{loc_id}/new/process"

    context = {
        'trip': trip,
        'parent': parent_location,
        'user': user,
        'action': action,
    }

    return render(request, "travels/locations/new_location.html", context)

def process_new_location(request, trip_id):
    if request.method == "POST":
        results = Location.objects.validate(request.POST)
        if results:
            for key, val in results.items():
                messages.error(request, val, key)
            return redirect(f"/travels/{trip_id}/locations/new")
        else:
            trip = Trip.objects.get(id=trip_id)
            user = User.objects.get(id=request.session['id'])
            loc = Location.objects.create(name=request.POST['name'],
                                        location_type=request.POST['loc_type'],
                                        info=request.POST['info'],
                                        fees=float(request.POST['fees'] or 0.0),
                                        start_time=request.POST['start_time'] or None,
                                        end_time=request.POST['end_time'] or None,
                                        parent_location=None,
                                        added_by_user=user)
            
            trip.itinerary.add(loc)

            return redirect(f"/travels/{trip_id}")                                        

    return redirect(f"/travels/{trip_id}/locations/new")


def edit_location(request, trip_id, loc_id):
    user = get_user(request)
    # form = LocationForm()
    loc = Location.objects.get(id=loc_id)
    trip = Trip.objects.get(id=trip_id)

    context = {
        'loc': loc,
        'trip': trip ,
        'user': user,
    }

    return render(request, "travels/locations/edit_location.html", context)


def process_edit_location(request, trip_id, loc_id):
    if request.method == "POST":
        loc = Location.objects.get(id=loc_id)
        loc.name = request.POST['name']
        loc.location_type = request.POST['loc_type']
        loc.info = request.POST['info']
        loc.start_time = request.POST['start_time'] or None
        loc.end_time = request.POST['end_time'] or None
        loc.fees = float(request.POST['fees'] or 0.0)
        loc.save()

        messages.info(request, "Updates Saved")
        return redirect(f"/travels/{trip_id}/locations/{loc_id}")
    
    return redirect(f"/travels/{trip_id}/locations/{loc_id}/edit")


def process_new_child_location(request, trip_id, loc_id):
    if request.method == "POST":
        results = Location.objects.validate(request.POST)
        if not results:
            parent_loc = Location.objects.get(id=loc_id)
            user = User.objects.get(id=request.session['id'])
    
            child_loc = Location.objects.create(name=request.POST['name'],
                                                location_type=request.POST['loc_type'],
                                                info=request.POST['info'],
                                                added_by_user=user)

            child_loc.parent_location = parent_loc
            child_loc.save()

            return redirect(f"/travels/{trip_id}/locations/{child_loc.id}")
        else:
            for key, val in results.items():
                messages.error(request, val, key)
    
    return redirect(f"/travels/{trip_id}/locations/{loc_id}/new")


def delete_location(request, trip_id, loc_id):
    user = get_user()

    return redirect(f"/travels/{trip_id}")


def bread_crumbs(loc_id):
    loc = Location.objects.get(id=loc_id)
    ancestors = []

    while loc.parent_location != None:
        loc = loc.parent_location
        ancestors.insert(0, loc)

    return ancestors

'''
ACCOMODATIONS
'''

def new_accomodations(request, trip_id):
    # aform = AccomodationForm()
    trip = Trip.objects.get(id=trip_id)
    acom_types = ACCOMODATION_TYPE

    context = {
        # 'acco_form': aform,
        'trip': trip,
        'accom_types': ACCOMODATION_TYPE,
    }

    return render(request, "travels/accomodations/new_accomodations.html", context)


def process_new_accomodations(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['id'])

    if request.method == "POST":
        print("price: "+request.POST['price'])
        
        Accomodations.objects.create(business_name=request.POST['name'],
                                accomodation_type=request.POST['accom_type'],
                                address=request.POST['address'],
                                price_per_night=float(request.POST['price'] or 0),
                                check_in=request.POST['check_in'] or None,
                                check_out=request.POST['check_out'] or None,
                                added_by=user,
                                trip=trip)

        return redirect(f"/travels/{trip_id}")
    
    return redirect(f"{trip_id}/accomodations/new/process")

'''
TRANSPORTATION
'''

def new_transportation(request, trip_id):
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=trip_id)
    
    context = {
        'trip': trip,
        'trans_modes': TRANSPORTATION_MODE,
        'user': user,
    }

    return render(request, "travels/transportation/new_transportation.html", context)


def process_new_transportation(request, trip_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['id'])
        trip = Trip.objects.get(id=trip_id)

        Transportation.objects.create(mode=request.POST['trans_type'],
                                        company_name=request.POST['name'],
                                        price=float(request.POST['price'] or 0.0),
                                        origin=request.POST['origin'],
                                        destination=request.POST['destination'],
                                        departure_time=request.POST['departure'] or None,
                                        arrival_time=request.POST['arrival'] or None,
                                        added_by=user,
                                        trip=trip)
        

        return redirect(f"/travels/{trip_id}")
    
    return redirect(f"/travels/{trip_id}/transportation/new")

def add_location_picture(request, trip_id, loc_id):
    location = Location.objects.get(id=loc_id)
    form = UploadPictureForm()

    context = {
        'location': location,
        'form': form,
        'trip_id': trip_id,
    }

    return render(request, "travels/locations/new_location_img.html", context)


def process_add_location_picture(request, trip_id, loc_id):
    form = UploadPictureForm(request.POST, request.FILES)

    if form.is_valid():
        user = User.objects.get(id=request.session['id'])
        location = Location.objects.get(id=loc_id)
        fname = handle_uploaded_file(request.FILES['picture'], loc_id)

        LocationPicture.objects.create(image_name=fname,
                                picture_of=location,
                                uploaded_by=user)
        
        return redirect(f"/travels/{trip_id}/locations/{loc_id}")
    
    return redirect(f"/travels/{trip_id}/locations/{loc_id}/pictures/add")

def handle_uploaded_file(f, loc_id):
    ext = f.name.split(".")[-1]
    fname = f"{loc_id}.{ext}"
    with open(f"media/locations/{fname}", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return fname


def request_join_trip(request, trip_id):
    user = User.objects.get(id=request.session['id'])
    trip = Trip.objects.get(id=trip_id)
    check = TripJoinRequest.objects.filter(Q(trip=trip) & Q(requested_by=user) & Q(is_pending=True))

    if not check:
        TripJoinRequest.objects.create(trip=trip, requested_by=user)
        messages.info(request, f"Request sent to join {trip.created_by.username}'s \"{trip.name}\" trip.")
        
    else:
        messages.info(request, "You have already asked to join that trip")
    
    return redirect(f"/users/friends/{trip.created_by.id}")

def accept_join_request(request, trip_id, req_id):
    user = User.objects.get(id=request.session['id'])
    treq = TripJoinRequest.objects.get(id=req_id)
    trip = treq.trip

    trip.companions.add(treq.requested_by)

    treq.is_pending = False
    treq.save()
    

    return redirect(f"/travels/{trip_id}")


def reject_join_request(request, trip_id, req_id):
    user = User.objects.get(id=request.session['id'])
    treq = TripJoinRequest.objects.get(id=req_id)
    treq.is_pending = False
    treq.save()

    return redirect(f"/travels/{trip_id}")


def get_user(request):
    user = User.objects.get(id=request.session['id'])
    return user