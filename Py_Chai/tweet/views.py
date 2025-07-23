from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


def tweet_list(req):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(req, 'tweet/tweet_list.html', {'tweets': tweets})

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

def tweet_delete(req, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=req.user)
    if req.method == 'POST':
        tweet.delete()
        messages.success(req, "Tweet deleted successfully.")
        return redirect('tweet:tweet_list')
    return render(req, 'tweet/tweet_confirm_delete.html', {'tweet': tweet})