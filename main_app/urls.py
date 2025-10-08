
from django.urls import path
from . import views  # Import your views file

urlpatterns = [
    path('', views.home_page, name='home'),
    # path('data/', views.show_data, name='show_data'),
    # path('data/export/csv/', views.export_users_csv, name='export_csv'),
    path('export/', views.export_users_csv, name='export_csv'),
]