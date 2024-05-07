from django.urls import path
from .views import *

urlpatterns = [
   path('', SubclassList.as_view(), name='subclass_list'),
   path('subclass/<int:pk>/', SubclassDetail.as_view(), name='subclass_detail'),
   path('categories/<int:pk>/', CategoryList.as_view(), name='subclass_cat_list'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
   path('create/', SubclassCreate.as_view(), name='subclass_create'),
   path('subclass/<int:pk>/update/', SubclassUpdate.as_view(), name='subclass_edit'),
   path('subclass/<int:pk>/delete/', SubclassDelete.as_view(), name='subclass_delete'),
   path('respond/<int:pk>/', Respond.as_view(), name='respond'),
   path('myresponse/<int:pk>', ResponseList.as_view(), name='myresponse'),
   path('myresponse/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
   path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
   path('myresponse/<int:pk>/accept/', accept_response, name='accept_response'),
]