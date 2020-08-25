from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404

from tasdesk_frontend.home.models import Categories
from .models import Design, DesignComment, DesignView
from .forms import DesignForm, CommentForm
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


def design_index(request):
    design_list = Design.objects.all()

    #*** Görüntülenme Sayısı İçin ***
    for design in design_list:
        design = get_object_or_404(Design, pk=design.id)
        if not DesignView.objects.filter(
                design=design,
                session=request.session.session_key):
            view = DesignView(design=design, ip=request.META['REMOTE_ADDR'], session=request.session.session_key)
            view.save()
    # *** Bitti ***
    if request.method == "POST":
        category = request.POST.get('category_id')
        design_list =design_list.filter(category=category)

    else:
        query = request.GET.get('q')
        if query:
            design_list = design_list.filter(Q(design_content__icontains=query) |
                                             Q(design_title__icontains=query) |
                                             Q(user__first_name__icontains=query) |
                                             Q(user__last_name__icontains=query)).distinct()

    paginator = Paginator(design_list, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    designs = paginator.get_page(page)
    categories = Categories.objects.all()

    return render(request, 'tasdesk-frontend/projects/projects-main.html', {'designs': designs, 'categories': categories})

def design_create(request):
    if request.method == "POST":
        form = DesignForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            design = form.save(commit=False)
            design.user = request.user
            design.save()
            messages.success(request, "Tasarım  Eklendi")
            return redirect('home:home')

    else:
        form = DesignForm()

    context = {
        'form': form,
    }
    return render(request, "tasdesk-frontend/homepage/index.html", context)

def design_update(request, slug):
    post = get_object_or_404(Design, slug=slug)
    form = DesignForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Tasarım  Güncellendi")
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'tasdesk-frontend/homepage/index.html', context)

def design_delete(request, slug):
    design = get_object_or_404(Design, slug=slug)
    design.delete()
    return redirect('designs:index')

def design_like(request):
    global design, message
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id', None)
        design = get_object_or_404(Design, id=id)
        if design.likes.filter(id=user.id).exists():
            # remove like/user
            design.likes.remove(user)
            message = '0' #beğeni kaldırıldı
        else:
            design.likes.add(user)
            message = '1' #beğendim

    ctx = {'likes_count': design.total_likes(), 'message': message}

    return HttpResponse(json.dumps(ctx), content_type='application/json')

def design_comment_create(request):
    global comment, total_comments, design

    if request.method == 'POST':
        design_id = request.POST.get('design_id')
        comment_content = request.POST.get('comment_content')
        user_id = request.POST.get('user_id')
        comment = DesignComment.objects.create(design_id=design_id, comment_content=comment_content, user_id=user_id)
        design = get_object_or_404(Design, id=design_id)
        total_comments = design.comments.all()

    ctx = {'design_id': design.id,'content': comment.comment_content, 'user': comment.user.get_full_name(),
            'total_comments': total_comments.count()}

    return HttpResponse(json.dumps(ctx), content_type='application/json')


'''if request.method =="POST":
        print(request.POST)
    title = request.POST.get('title')
    content = request.POST.get('content')
    Post.objects.create(title= title, content= content)
    return render(request,'post/form.html', context)'''