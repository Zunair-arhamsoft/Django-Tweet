from django.contrib.auth.models import User
from tweet.models import Tweet
from .forms import ProfileForm
from .models import Profile
from django.shortcuts import redirect, get_object_or_404, get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.tweets import get_paginated_tweet_data


def user_profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=user_obj).order_by('-created_at')
    result = get_paginated_tweet_data(request, tweets)

    if result['json']:
        return result['json']

    return render(request, 'accounts/profile.html', {
        'profile_user': user_obj,
        'tweet_data': result['tweet_data'],
        'page_obj': result['page_obj'],
        'is_own_profile': request.user == user_obj,
    })


@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username=user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})
