from django.conf.urls.static import static
from django.urls import path

from self_storage import settings
from storage import views

app_name = 'storage'

urlpatterns = [
    path('', views.show_home, name='index'),
    path('faq/', views.show_faq_page, name='faq'),
    path('boxes/', views.show_boxes_page, name='boxes'),
    path('boxes/<int:box_id>/payment', views.show_payment_page, name='payment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
