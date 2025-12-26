from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('prime_add',views.prime_add,name='prime_add'),
    path('prime_edit',views.prime_edit,name='prime_edit'),
    path('prime_edit/get_user',views.get_user,name='get_user'),
    path('prime_view',views.prime_view,name='prime_view'),
    path('prime_add/add_contractor',views.add_contractor,name='add_contractor'),
    path('prime_view/all_contractors',views.all_contractors,name='all_contractors'),
    path('prime_view/delete_user',views.delete_user,name='delete_user'),
    path('prime_add/upload_img',views.upload_img,name='upload_img')
]

