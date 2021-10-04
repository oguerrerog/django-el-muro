from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index), 
    path('administrador/', views.administrador), 
    path('registro/', auth.registro),
    path('login/', auth.login),
    path('logout/', auth.logout),
    path('mensaje/crear', views.crea_mensaje),
    path('mensaje/<int:id>/borrar', views.elimina_mensaje),
    path('mensaje/comentario', views.crea_comentario),
    path('comentario/<int:id>/borrar', views.elimina_comentario)
    
]
