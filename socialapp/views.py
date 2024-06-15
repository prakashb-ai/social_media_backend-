from django.shortcuts import render,redirect
from django.contrib.auth import User,auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,LikePost,FollwersCount
from itertools import chain
import random

# Create your views here.

@login_required(login_url='signin')

def index(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []

    feed =[]

    user_following = FollwersCount.objects.filter(follower = request.user.username)

    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))

    all_user = User.objects.all()

    user_following_all =[]

    for user in user_following :
        user_list = User.objects.filter(username = user.user)
        user_following_all.append(user_list)

    
    new_suggestion_list = [x for x in list(all_user) if (x not in list(user_following_all))]

    current_user = User.objects.filter(username = request.user.username)
    final_suggestion_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggestion_list)

    username_profile = []
    username_profile_list = []

    for user in final_suggestion_list:
        username_profile.append(users.id)
    
    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user = ids)
        username_profile_list.append(profile_lists)
    
    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request,'index.html',{'user_profile':user_profile, 'posts':feed_list,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})


@login_required(login_url='signin')

def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user = user,image = image,caption = caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')

def search(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username_icontains = username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            user_profile.append(users.id)
            
