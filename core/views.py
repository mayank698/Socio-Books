from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Like, Follow
from itertools import chain
import random


# Create your views here.
@login_required(login_url="/login")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_following_list = []
    feed = []
    user_following = Follow.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    for usernames in user_following_list:
        feed_list = Post.objects.filter(user=usernames)
        feed.append(feed_list)
    feed_list = list(chain(*feed))

    # user suggestions
    all_users = User.objects.all()
    user_following_all = []
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    new_suggestions_list = [
        x for x in list(all_users) if (x not in list(user_following_all))
    ]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [
        x for x in list(new_suggestions_list) if (x not in list(current_user))
    ]
    random.shuffle(final_suggestions_list)
    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile)
    suggestions_username_profile_list = list(chain(*username_profile_list))
    return render(
        request,
        "index.html",
        {
            "user_profile": user_profile,
            "posts": feed_list,
            "suggestions_username_profile_list": suggestions_username_profile_list[:4],
        },
    )


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmPassword = request.POST["confirmPassword"]

        if password == confirmPassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken.")
                return redirect("signup")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                # Log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # Create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id
                )
                new_profile.save()
                return redirect("settings")
        else:
            messages.info(request, "Password Not Matching")
            return redirect("signup")
    else:
        return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Credentials Invalid")
            return redirect("signin")

    return render(request, "signin.html")


@login_required(login_url="/login")
def logout(request):
    auth.logout(request)
    return redirect("signin")


@login_required(login_url="/login")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if request.FILES.get("image") is None:
            image = user_profile.profileimage
            bio = request.POST["bio"]
            location = request.POST["location"]

            user_profile.profileimage = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get("image") is not None:
            image = request.FILES.get("image")
            bio = request.POST["bio"]
            location = request.POST["location"]

            user_profile.profileimage = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect("settings")

    return render(request, "setting.html", {"user_profile": user_profile})


@login_required(login_url="/login")
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get("image_upload")
        caption = request.POST["caption"]
        user_profile = Profile.objects.get(user=request.user)
        profile_image_url = user_profile.profileimage.url
        new_post = Post.objects.create(
            user=user,
            image=image,
            caption=caption,
            user_profile_image=profile_image_url,
        )
        new_post.save()
        return redirect("/")
    else:
        return redirect("/")


@login_required(login_url="/login")
def likes(request):
    username = request.user.username
    post_id = request.GET.get("post_id")

    post = Post.objects.get(id=post_id)
    like_filter = Like.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = Like.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = Like.objects.filter(post_id=post_id).count()
        post.save()
        return redirect("/")
    else:
        like_filter.delete()
        post.no_of_likes = Like.objects.filter(post_id=post_id).count()
        post.save()
        return redirect("/")


@login_required(login_url="/login")
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    profile_object = Profile.objects.get(user=user_object)
    post_object = Post.objects.filter(user=pk)
    post_object_len = post_object.count()

    follower = request.user.username
    user = pk

    if Follow.objects.filter(follower=follower, user=user).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"
    user_followers = len(Follow.objects.filter(user=pk))
    user_following = len(Follow.objects.filter(follower=pk))
    context = {
        "user_object": user_object,
        "profile_object": profile_object,
        "post_object": post_object,
        "post_object_len": post_object_len,
        "button_text": button_text,
        "user_followers": user_followers,
        "user_following": user_following,
    }
    return render(request, "profile.html", context)


@login_required(login_url="/login")
def follow(request):
    if request.method == "POST":
        follower = request.POST["follower"]
        user = request.POST["user"]
        if Follow.objects.filter(follower=follower, user=user).first():
            delete_follower = Follow.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect(f"/profile/{user}")
        else:
            newFollower = Follow.objects.create(follower=follower, user=user)
            newFollower.save()
            return redirect(f"/profile/{user}")
    else:
        return redirect("/")


@login_required(login_url="/login")
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == "POST":
        username = request.POST["username"]
        username_object = User.objects.filter(username__icontains=username)
        username_profile = []
        username_profile_list = []
        for users in username_object:
            username_profile.append(users.id)
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        username_profile_list = list(chain(*username_profile_list))
    return render(
        request,
        "search.html",
        {"user_profile": user_profile, "username_profile_list": username_profile_list, 'username':username},
    )
