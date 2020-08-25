from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404

from tasdesk_frontend.home.models import Categories
from .models import Advert, AdvertComment, AdvertView
from .forms import AdvertForm, CommentForm
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json


def advert_index(request):
    advert_list = Advert.objects.all()

    #*** Görüntülenme Sayısı İçin ***
    for advert in advert_list:
        advert = get_object_or_404(Advert, pk=advert.id)
        if not AdvertView.objects.filter(
                advert=advert,
                session=request.session.session_key):
            view = AdvertView(advert=advert, ip=request.META['REMOTE_ADDR'], session=request.session.session_key)
            view.save()
    # *** Bitti ***
    if request.method == "POST":
        category = request.POST.get('category_id')
        advert_list = advert_list.filter(category=category)
    else:
        query = request.GET.get('q')
        if query:
            advert_list = advert_list.filter(Q(advert_content__icontains=query) |
                                             Q(advert_title__icontains=query) |
                                             Q(user__first_name__icontains=query) |
                                             Q(user__last_name__icontains=query)).distinct()

    paginator = Paginator(advert_list, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    adverts = paginator.get_page(page)
    categories = Categories.objects.all()

    return render(request, 'tasdesk-frontend/jobs/jobs-main.html', {'adverts': adverts, 'categories': categories})

def advert_create(request):
    if request.method == "POST":
        form = AdvertForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            advert = form.save(commit=False)
            advert.user = request.user
            advert.save()
            messages.success(request, "iLAN  Eklendi")
            return redirect('home:home')

    else:
        form = AdvertForm()

    context = {
        'form': form,
    }
    return render(request, "tasdesk-frontend/homepage/index.html", context)

def advert_update(request, slug):
    post = get_object_or_404(Advert, slug=slug)
    form = AdvertForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "İlan  Güncellendi")
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'tasdesk-frontend/homepage/index.html', context)

def advert_delete(request, slug):
    advert = get_object_or_404(Advert, slug=slug)
    advert.delete()
    return redirect('adverts:index')

def advert_like(request):
    global advert, message
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id', None)
        advert = get_object_or_404(Advert, id=id)
        if advert.likes.filter(id=user.id).exists():
            # remove like/user
            advert.likes.remove(user)
            message = '0' #beğeni kaldırıldı
        else:
            advert.likes.add(user)
            message = '1' #beğendim

    ctx = {'likes_count': advert.total_likes(), 'message': message}

    return HttpResponse(json.dumps(ctx), content_type='application/json')

def advert_comment_create(request):
    global comment, total_comments, advert

    if request.method == 'POST':
        advert_id = request.POST.get('advert_id')
        comment_content = request.POST.get('comment_content')
        user_id = request.POST.get('user_id')
        comment = AdvertComment.objects.create(advert_id=advert_id, comment_content=comment_content, user_id=user_id)
        advert = get_object_or_404(Advert, id=advert_id)
        total_comments = advert.comments.all()

    ctx = {'advert_id': advert.id,'content': comment.comment_content, 'user': comment.user.get_full_name(),
            'total_comments': total_comments.count()}

    return HttpResponse(json.dumps(ctx), content_type='application/json')


'''if request.method =="POST":
        print(request.POST)
    title = request.POST.get('title')
    content = request.POST.get('content')
    Post.objects.create(title= title, content= content)
    return render(request,'post/form.html', context)'''