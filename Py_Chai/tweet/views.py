from .models import Tweet, Like 
from django.shortcuts import redirect, get_object_or_404, get_object_or_404, redirect, render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

def tweet_list(req):
    tweets = Tweet.objects.all().order_by('-created_at')
    paginator = Paginator(tweets, 2) 
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tweet_data = []
    for tweet in page_obj:
        liked = tweet.likes.filter(user=req.user).exists(
        ) if req.user.is_authenticated else False
        tweet_data.append({
            'tweet': tweet,
            'liked': liked,
            'like_count': tweet.likes.count()
        })
        
    return render(req, 'tweet/tweet_list.html', {'tweet_data': tweet_data,  'page_obj': page_obj})

@login_required
def tweet_create(req):
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            messages.success(req, "Tweet added successfully.")
            return redirect('tweet:tweet_list')
    else:
        form = TweetForm()
    return render(req, 'tweet/tweet_form.html', {'form': form})

@login_required
def tweet_edit(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=req.user)
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            messages.success(req, "Tweet updated successfully.")
            return redirect('tweet:tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(req, 'tweet/tweet_form.html', {'form': form})

@login_required
def tweet_delete(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=req.user)
    if req.method == 'POST':
        tweet.delete()
        messages.success(req, "Tweet deleted successfully.")
        return redirect('tweet:tweet_list')
    return render(req, 'tweet/tweet_confirm_delete.html', {'tweet': tweet})

def register(req):
    if req.method == 'POST':
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(req, "User registered successfully.")
            login(req, user)
            return redirect('tweet:tweet_list')
    else:
        form = UserRegistrationForm()
    return render(req, 'registration/register.html', {'form': form})

@login_required
def toggle_like(req, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(user=req.user, tweet=tweet)
    if not created:
        like.delete()
    return HttpResponseRedirect(reverse('tweet:tweet_list'))
