from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import * 

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect

def index(request):
	return render(request, "friends/index.html")

def register(request):
	result = User.objects.register_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request, error)
		return redirect('/main')
	else:
		request.session['user_id'] = result.id
		return redirect('/friends')

def login(request):
	result = User.objects.login_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request, error)
		return redirect('/main')
	else:
		request.session['user_id'] = result.id
		return redirect('/friends')

def friends(request):
	try:
		id = request.session['user_id']
		user = User.objects.get(id = id)

		context = {
			"user": user,
			"non_friends": User.objects.exclude(id__in=user.friends.all()),
			# "non_friends_self": non_friends.exclude(user=user),
			"friends": user.friends.all()
		}
		return render(request, "friends/friends.html", context)

	except:
		return redirect('/main')

def add_friend(request, user_id):
	current_user = User.objects.get(id=request.session['user_id'])
	this_friend = User.objects.get(id=user_id)
	current_user.friends.add(this_friend)

	return redirect('/friends')

def remove_friend(request, user_id):
	current_user = User.objects.get(id=request.session['user_id'])
	this_friend = User.objects.get(id=user_id)
	current_user.friends.remove(this_friend)
	
	return redirect('/friends')

def user_profile(request, user_id):
	friend = User.objects.get(id=user_id)
	context = {
		"friend": friend
	}
	return render(request, "friends/profile.html", context)

def logout(request):
	request.session.clear()
	return redirect('/main')
	