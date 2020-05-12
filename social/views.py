from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Social
from .models import ChatRoom
from django.contrib.auth.models import User
from users.models import Following, Follower, Profile
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import F
from django.template import RequestContext
from .forms import CreatePostForm

from pprint import pprint

from django.utils.safestring import mark_safe
import json

# Create your views here.
@login_required
def home(request):
	images = Social.objects.all().order_by("-date_posted")		
	return render(request, 'social/home.html', {"images":images})

def about(request):
	return render(request, 'social/about.html')	

@ensure_csrf_cookie
def search_users(request):
	if request.method == 'POST':	#if method is POST we conclude data is entered from the search bar
		search_text = request.POST['search_text']
	else:
		search_text = ''
	users = User.objects.filter(username__icontains=search_text).exclude(username__icontains=request.user.username).annotate(Count('username')).order_by('-username__count')[:5]
	return render(request, 'social/ajax_search.html',{'users':users})

@login_required
def other_profile(request, visited_user):
	
	visited_user_profile = User.objects.get(username=visited_user)
	
	images = Social.objects.filter(author__username=visited_user).order_by("-date_posted")

	visited_user_follower = Follower.objects.get(current_user=visited_user_profile)

	visited_user_following = Following.objects.get(current_user=visited_user_profile)

	no_of_followers = visited_user_follower.no_of_followers

	no_of_following = visited_user_following.no_of_following

	following_status = False

	if request.user in visited_user_follower.followed_by.all():
		following_status = True

	request.session["visited_user_name"] =  visited_user

	room_name_list = []

	room_name_list.append(request.user.username)
	room_name_list.append(visited_user)

	room_name_list.sort()


	context = {
	'visited_user_profile': visited_user_profile,
	'images':images,
	'following_status':following_status,
	'no_of_followers':no_of_followers,
	'no_of_following': no_of_following,
	'no_of_posts': images.count,
	'room_name': room_name_list[0] + "-" + room_name_list[1],
	}

	return render(request, 'social/final_other_profile.html', context)

def follow(request, **kwargs):

	visited_user = User.objects.get(username=request.session["visited_user_name"])

	visited_user_follower = Follower.objects.get(current_user=visited_user)
	
	current_user_following = Following.objects.get(current_user=request.user)

	visited_user_follower.followed_by.add(request.user)

	visited_user_follower.no_of_followers = F('no_of_followers') + 1

	current_user_following.following_to.add(visited_user)

	current_user_following.no_of_following = F('no_of_following') + 1	

	current_user_following.save()

	visited_user_follower.save()

	visited_user_follower.refresh_from_db()

	room_name_list = []

	room_name_list.append(request.user.username)
	room_name_list.append(visited_user.username)

	room_name_list.sort()

	all_room = None

	try :
		all_room = ChatRoom.objects.get(room_name=room_name_list[0] + "-" + room_name_list[1])

	except:
		all_room = ChatRoom(room_name = room_name_list[0] + "-" + room_name_list[1])
		all_room.save()

	data = { "no_of_followers_after_ajax" : visited_user_follower.no_of_followers}

	return JsonResponse(data)

def unfollow(request, **kwargs):

	visited_user = User.objects.get(username=request.session["visited_user_name"])

	visited_user_follower = Follower.objects.get(current_user=visited_user)
	current_user_following = Following.objects.get(current_user=request.user)

	visited_user_follower.followed_by.remove(request.user)

	visited_user_follower.no_of_followers = F('no_of_followers') - 1

	current_user_following.following_to.remove(visited_user)

	current_user_following.no_of_following = F('no_of_following') - 1	

	current_user_following.save()

	visited_user_follower.save()

	visited_user_follower.refresh_from_db()

	data = {"no_of_followers_after_ajax" : visited_user_follower.no_of_followers}

	return JsonResponse(data)

def like(request, **kwargs):			
	if request.method == "POST" and request.is_ajax():
		selected_image = Social.objects.get(id=request.POST['imageid'])

		if request.user not in selected_image.liked_by.all():
			selected_image.liked_by.add(request.user)
			selected_image.no_of_likes = F('no_of_likes') + 1
			selected_image.save()
			selected_image.refresh_from_db()
	
		data = {"no_of_likes" : selected_image.no_of_likes}	
	return JsonResponse(data)

def unlike(request, **kwargs):  
	if request.method == 'POST' and request.is_ajax():
		selected_image = Social.objects.get(id=request.POST['imageid'])
		selected_image.liked_by.remove(request.user)
		selected_image.no_of_likes = F('no_of_likes') - 1
		selected_image.save()
		selected_image.refresh_from_db()
		
		data = {"no_of_likes" : selected_image.no_of_likes}	
	
	return JsonResponse(data)

def chat(request):
	return render(request,"social/chat.html",{'room_name_json': mark_safe(json.dumps("hel12o"))})

@login_required
def create_a_post(request, **kwargs):
	if request.method == 'POST':
		post_create_form = CreatePostForm(request.POST,request.FILES)
		if post_create_form.is_valid():
			new_post = post_create_form.save(commit=False) #basically do not save it in database yet
			new_post.author = request.user
			new_post.save()

			return redirect('profile')

	else:
		post_create_form = CreatePostForm()

	return render(request,'social/create_a_post.html',{'post_create_form' : post_create_form})

@login_required
def instagram_chatting(request, room_name):

	receiver_user_name = room_name.replace('-' + request.user.username,'').replace(request.user.username + '-','')

	receiver_user = User.objects.get(username=receiver_user_name)

	context = {
	'room_name': mark_safe(json.dumps(str(room_name))), 
	'sender' : mark_safe(json.dumps(str(request.user.username))),
	'receiver_user' : receiver_user,
	}

	return render(request,'social/chatui.html',context)