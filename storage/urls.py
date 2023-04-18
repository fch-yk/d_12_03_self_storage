from django.urls import path


from storage import views

app_name = 'storage'

urlpatterns = [
    path('', views.show_home, name='index'),
    path('faq/', views.show_faq_page, name='faq'),
]
