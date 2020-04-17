from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("signup",  views.signup_view, name="signup"),
    path("logout", views.logout_view, name="logout"),
    path("menu", views.menu_view, name="menu"),
    re_path(r'^add-to-cart/(?P<item_id>\d+)/$', views.add_to_cart, name="order"),
    path("cart", views.cart_view, name="cart"),
    re_path(r'^place_order/(?P<order_id>\d+)/$', views.place_order, name="place_order"),
    path("success", views.success_view, name="success")
]
