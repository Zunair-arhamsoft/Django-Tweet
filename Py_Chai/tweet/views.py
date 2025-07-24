from .models import Tweet
from django.shortcuts import redirect, get_object_or_404, get_object_or_404, redirect, render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def tweet_list(req):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(req, 'tweet/tweet_list.html', {'tweets': tweets})

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
