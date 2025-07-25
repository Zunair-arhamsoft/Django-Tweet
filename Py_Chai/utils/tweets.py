# utils/tweet_utils.py

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse


def get_paginated_tweet_data(request, queryset, per_page=6):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return {
                'json': JsonResponse({'tweets': [], 'has_next': False}),
                'page_obj': None,
                'tweet_data': []
            }
        page_obj = paginator.page(paginator.num_pages)

    tweet_data = []
    for tweet in page_obj:
        liked = tweet.likes.filter(user=request.user).exists(
        ) if request.user.is_authenticated else False
        avatar_url = (
            tweet.user.profile.avatar.url
            if hasattr(tweet.user, 'profile') and tweet.user.profile.avatar
            else '/static/images/profile-user.png'
        )

        tweet_data.append({
            'id': tweet.id,
            'user': tweet.user.username,
            'avatar_url': avatar_url,
            'text': tweet.text,
            'created_at': tweet.created_at.strftime("%b %d, %Y %H:%M"),
            'photo_url': tweet.photo.url if tweet.photo else None,
            'liked': liked,
            'like_count': tweet.likes.count(),
            'is_owner': request.user == tweet.user
        })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return {
            'json': JsonResponse({'tweets': tweet_data, 'has_next': page_obj.has_next()}),
            'page_obj': page_obj,
            'tweet_data': tweet_data
        }

    return {
        'json': None,
        'page_obj': page_obj,
        'tweet_data': tweet_data
    }
