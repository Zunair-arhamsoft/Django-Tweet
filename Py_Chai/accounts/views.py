from django.contrib.auth.models import User
from tweet.models import Tweet
from .forms import ProfileForm
from .models import Profile
from django.shortcuts import redirect, get_object_or_404, get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import  JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def user_profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=user_obj).order_by('-created_at')
    paginator = Paginator(tweets, 6)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'tweets': [],
                'has_next': False,
            })
        page_obj = paginator.page(paginator.num_pages)

    tweet_data = []
    for tweet in page_obj:
        liked = tweet.likes.filter(user=request.user).exists(
        ) if request.user.is_authenticated else False
        tweet_data.append({
            'id': tweet.id,
            'user': tweet.user.username,
            'text': tweet.text,
            'created_at': tweet.created_at.strftime("%b %d, %Y %H:%M"),
            'photo_url': tweet.photo.url if tweet.photo else None,
            'liked': liked,
            'like_count': tweet.likes.count(),
            'is_owner': request.user == tweet.user
        })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'tweets': tweet_data,
            'has_next': page_obj.has_next(),
        })

    return render(request, 'accounts/profile.html', {
        'profile_user': user_obj,
        'tweet_data': tweet_data,
        'page_obj': page_obj,
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
