from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
import bcrypt
from .models import *
from .forms import *
from apps.travels.models import *

# Create your views here.
def view_user(request, id):
    if 'id' in request.session and request.session['id'] == id:
        user = User.objects.get(id=id)
        context = { 'user': user }
        return render(request, "users/profile.html", context)
        # return redirect(f"/users/{id}")
    else:
        return redirect("/logout")


def view_profile(request):
    user = User.objects.get(id=request.session['id'])
    requests = FriendRequest.objects.filter(Q(recipient=user) & Q(is_pending=True))

    context = {
        'user': user,
        'friend_requests': requests,
    }

    avt = Avatar.objects.filter(user=user)
    if len(avt) > 0:
        context['avatar'] = avt[0].image_name
    

    return render(request, "users/profile.html", context)


def view_friend_profile(request, friend_id):
    user = User.objects.get(id=request.session['id'])
    friend = user.friends.get(id=friend_id)

    # check the users are friends
    if friend:
        trips = Trip.objects.filter(created_by=friend)

        context = {
            'user': user,
            'friend': friend,
            'trips': trips,
        }
        
        return render(request, "users/other_profile.html", context)
    else:
        return redirect("/users/profiles")


def view_friends(request):
    user = User.objects.get(id=request.session['id'])
    requested_users = FriendRequest.objects.filter(Q(sender=user) & Q(is_pending=True))
    pending_users = FriendRequest.objects.filter(Q(recipient=user) & Q(is_pending=True))

    others = User.objects.exclude(id=user.id)\
        .exclude(id__in=user.friends.all())\
            .exclude(id__in=requested_users.values('recipient').all())\
                .exclude(id__in=pending_users.values('sender').all())

    context = {
        'user': user,
        'requested_users': requested_users,
        'pending_response': pending_users,
        'other_users': others,
    }

    return render(request, "users/friends.html", context)


def accept_friend_request(request, req_id):
    friend_req = FriendRequest.objects.get(id=req_id)
    friend_req.recipient.friends.add(friend_req.sender)
    friend_req.is_pending = False
    friend_req.save()

    messages.info(request, f"{friend_req.sender.username} added as a friend.")

    return redirect("/users/friends")

def cancel_friend_request(request, req_id):
    friend_req = FriendRequest.objects.get(id=req_id)
    # friend_req.recipient.friends.add(friend_req.sender)
    friend_req.is_pending = False
    friend_req.save()

    messages.info(request, f"Friend request to {friend_req.recipient.username} cancelled")

    return redirect("/users/friends")


def upload_avatar(request):
    user = User.objects.get(id=request.session['id'])
    form = UploadAvatarForm()
    return render(request, "users/upload_avatar.html", { 'avatar_form': form, 'user': user })


def process_upload_avatar(request):
    if request.method == 'POST':

        form = UploadAvatarForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.get(id=request.session['id'])
            fname = handle_uploaded_file(request.FILES['avatar'], user.id)

            Avatar.objects.create(image_name=fname, user=user)
            
            return redirect('/users/profiles')
    
    return redirect("/users/avatars")


def handle_uploaded_file(f, user_id):
    ext = f.name.split(".")[-1]
    fname = f"{user_id}.{ext}"
    with open(f"media/avatars/{fname}", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return fname


def send_friend_request(request, friend_id):
    sender = User.objects.get(id=request.session['id'])
    recipient = User.objects.get(id=friend_id)

    check = FriendRequest.objects.filter(Q(sender=sender) & Q(recipient=recipient) & Q(is_pending=True))
    if check:
        messages.info(request, "Friend request already pending")
    else:
        FriendRequest.objects.create(sender=sender, recipient=recipient, is_pending=True)
        messages.info(request, "Friend request sent")

    return redirect("/users/friends")