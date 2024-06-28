from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Hotels import views
urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/buscar/', views.search_rooms, name='search_rooms'),
    path('perfil/', views.perfil, name='perfil'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # Actualiza esta línea
    path('accounts/logout/', views.logout_view, name='logout'),
    path('perfil/editar/', views.edit_profile, name='editar'),
    path('catalogo/crear/', views.create_room, name='create_room'), 
    path('add_to_cart/<int:room_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('reservar/<int:item_id>/', views.reservar, name='reservar'),
    path('search_room/', views.search_room, name='search_room'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)