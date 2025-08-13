from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import F
from django.urls import reverse
from .models import Link
from .forms import LinkForm

def create_link(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["original_url"]
            link = Link.objects.filter(original_url=url).first() or form.save()
            short_url = request.build_absolute_uri(reverse("follow", args=[link.slug]))
            return render(request, "links/created.html", {"link": link, "short_url": short_url})
    else:
        form = LinkForm()
    return render(request, "links/create.html", {"form": form})

def follow(request, slug):
    link = get_object_or_404(Link, slug=slug)
    # inkrement hits atomicky
    Link.objects.filter(pk=link.pk).update(hits=F("hits") + 1)
    return redirect(link.original_url)

def list_links(request):
    qs = Link.objects.order_by("-created_at")
    page_obj = Paginator(qs, 10).get_page(request.GET.get("page", 1))
    return render(request, "links/list.html", {
        "page_obj": page_obj,
        "links": page_obj.object_list,
    })
