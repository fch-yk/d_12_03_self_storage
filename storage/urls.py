from django.urls import path


from storage import views


urlpatterns = [
    path('', views.show_home),
]
