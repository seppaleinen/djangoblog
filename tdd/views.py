from django.views.generic import ListView
from django.views.generic import DetailView
from tdd.models import Entry


class HomeView(ListView):
    template_name = 'index2.html'
    queryset = Entry.objects.order_by('-created_at')


class EntryDetail(DetailView):
    model = Entry