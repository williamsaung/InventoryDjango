from django.shortcuts import render
from django.views.generic import ListView,CreateView,TemplateView,DetailView
from . import models
from django.http import HttpResponse,JsonResponse
import operator
from django.db.models import Q
from functools import reduce
import csv
from django.core import serializers
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'


class InventoryListView(ListView):
    context_object_name = 'inventory'
    model = models.Inventory

    def get_queryset(self):
        result = super(InventoryListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(price__icontains=q) for q in query_list))
            )

        return result

class InventoryCreateView(CreateView):
    fields = ('name','serial_number','price')
    model = models.Inventory

def inventory_download(request):
    items = models.Inventory.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="inventory.csv"'
    writer = csv.writer(response, delimiter=',')
    writer.writerow(['name','serial_number','price'])

    for obj in items:
        writer.writerow([obj.name, obj.serial_number, obj.price])

    return response

def inventory_json(request):
    inventory_list = models.Inventory.objects.all()
    output = serializers.serialize('json', inventory_list, fields=('name', 'serial_number', 'price'))

    return JsonResponse(output,safe=False, content_type="application/json")

class InventoryDetailView(DetailView):
    context_object_name = 'inventory_detail'
    model = models.Inventory
    template_name = 'inventory_tracker/inventory_detail.html'