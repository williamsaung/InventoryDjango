from inventory_tracker import views
from django.urls import path
app_name = 'inventory_tracker'

urlpatterns = [
    path('',views.InventoryListView.as_view(),name='list'),
    path('create/',views.InventoryCreateView.as_view(),name='create'),
    path('<int:pk>/',views.InventoryDetailView.as_view(),name='detail')
]