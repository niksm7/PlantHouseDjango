from django.urls import path
from . import views


urlpatterns = [
    path("",views.index,name="NurseryHome"),
    path('addItem/',views.addItem,name="AddItem"),
    path('addItem/saveItem/',views.saveItem,name="SaveItem"),
    path('morders/',views.manageOrders,name="manageOrders"),
    path('saveUpdate/<int:id>',views.saveUpdate,name="saveUpdate"),
]