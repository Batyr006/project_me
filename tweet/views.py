from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import login
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm


def index(request):
    return render(request, 'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all()

    # Поиск по содержимому
    query = request.GET.get('q')
    if query:
        tweets = tweets.filter(text__icontains=query)

    # Фильтрация по автору
    author = request.GET.get('author')
    if author:
        tweets = tweets.filter(user__username=author)

    # Сортировка
    sort = request.GET.get('sort')
    if sort == 'asc':
        tweets = tweets.order_by('created_at')
    else:
        tweets = tweets.order_by('-created_at')  # По умолчанию: новые сверху

    # Пагинация
    paginator = Paginator(tweets, 5)  # 5 твитов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tweet_list.html', {
        'page_obj': page_obj,
        'query': query,
        'author': author,
        'sort': sort
    })


@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()

    return render(request, 'tweet_form.html', {'form': form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'tweet_form.html', {'form': form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')

    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})