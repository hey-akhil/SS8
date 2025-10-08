from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('export_csv/', views.export_users_csv, name='export_csv'),
    path('import_csv/', views.import_users_csv, name='import_csv'),
]
