# Create your views here.
from ads.models import Songs, Fav
from ads.forms import CreateForm
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q

class AdListView(View):
    template_name = "ads/ad_list.html"
    
    def get(self, request) :
        ads_list = Songs.objects.all()
        print (ads_list)
        rs = 'https://indiehoy.com/wp-content/uploads/2020/09/goat-head-soup-rolling-stones.jpg'
        lz = 'https://www.elcomercio.com/wp-content/uploads/2021/11/Zeppelin-700x391.jpg'
        strval =  request.GET.get("search", False)
        if request.user.is_authenticated:
            rows = request.user.favorite_ads.values('id')
            #favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
            for obj in ads_list:
                obj.natural_updated = naturaltime(obj.updated_at)


        ctx = {'ad_list' : ads_list, 'search': strval, 'Stones':rs, 'ledzep':lz,}
        return render(request, self.template_name, ctx)


class AdDetailView(OwnerDetailView):
    model = Songs
    template_name = "ads/ad_detail.html"
    def get(self, request, pk) :
        x = Songs.objects.get(id=pk)
        context = { 'ad' : x, }
        return render(request, self.template_name, context)

class AdCreateView(LoginRequiredMixin, View):
    model = Songs
    fields = ['song', 'artista', 'category']
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        form.save_m2m()
        return redirect(self.success_url)



class AdUpdateView(LoginRequiredMixin, View):
    model = Songs
    fields = ['song', 'artista', 'category']
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Songs, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Songs, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()
        form.save_m2m()

        return redirect(self.success_url)



class AdDeleteView(OwnerDeleteView):
    model = Songs


def stream_file(request, pk):
    ad = get_object_or_404(Songs, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response
