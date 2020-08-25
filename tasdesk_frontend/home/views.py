from django.shortcuts import render,get_object_or_404
from .models import Categories
from tasdesk_frontend.adverts.models import Advert, AdvertView
from tasdesk_frontend.designs.models import Design, DesignView
from tasdesk_frontend.accounts.models import User_Details
from itertools import chain
from django.contrib.contenttypes.models import ContentType
from operator import attrgetter
# Create your views here.
def home_view(request):
    categories = Categories.objects.all()
    advert_list = Advert.objects.all().order_by('publishing_date')
    design_list = Design.objects.all().order_by('publishing_date')
    # *** Görüntülenme Sayısı İlanlar İçin ***
    for advert in advert_list:
        advert = get_object_or_404(Advert, pk=advert.id)
        if not AdvertView.objects.filter(
                advert=advert,
                session=request.session.session_key):
            view = AdvertView(advert=advert, ip=request.META['REMOTE_ADDR'], session=request.session.session_key)
            view.save()
    # *** Bitti ***
    # *** Görüntülenme Sayısı Tasarımlar İçin ***
        for design in design_list:
            design = get_object_or_404(Design, pk=design.id)
            if not DesignView.objects.filter(
                    design=design,
                    session=request.session.session_key):
                view = DesignView(design=design, ip=request.META['REMOTE_ADDR'], session=request.session.session_key)
                view.save()
        # *** Bitti ***

    posts = sorted(chain(design_list, advert_list),  key=lambda i:i.publishing_date, reverse=True)
    control = ContentType.objects
    return render(request, 'tasdesk-frontend/homepage/index.html', {'control': control, 'posts': posts, 'categories': categories})
