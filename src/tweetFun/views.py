from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
from .models import Tweet
from .forms import TweetForm

ALLOWED_HOSTS= settings.ALLOWED_HOSTS


def homePage(request, *args, **kwargs):

    return render(request, "pages/home.html",context ={}, status = 200)

def tweetCreateView(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html', context = {"form" : form} )

def tweet_list_view(request, *args, **kwargs):
    """
    REST API View
    Consume via JS, TS, etc...
    return JSON data
    """
    querySet = Tweet.objects.all()
    tweet_list = [{"id":x.id, "content":x.content, "likes": 12 } for x in querySet]
    data = {
        "isUser": False,
        "response": tweet_list
    }
    return JsonResponse(data)

def tweetDetailView(request, tweet_id, *args, **kwargs):
    """
    REST API View
    Consume via JS, TS, etc...
    return JSON data
    """
    data = {
        "id": tweet_id,
        # "image_path": obj.image.url,
        
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] ="tweet_id Not Found"
        status = 404
    
    return JsonResponse(data,status=status)  #json.dumps 
