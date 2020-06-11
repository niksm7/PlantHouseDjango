from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("about/",views.about,name="AboutUs"),
    path("contact/",views.contact,name="ContactUs"),
    path("tracker/",views.tracker,name="TrackingStatus"),
    path("search/",views.search,name="Search"),
    path("products/<int:myid>",views.productview,name="ProductView"),
    path("checkout/",views.checkout,name="Checkout"),
    path("cart/",views.cart,name="Cart"),
    path("logout/",views.handleLogout,name="handleLogout"),
    path("products/postReview",views.postReview,name="postReview"),
    path("ajax/cartUpdate/",views.update_cart,name="cartUpdate"),
]