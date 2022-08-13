from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing",views.listing,name="listing"),
    path("listing/<int:p_id>",views.item,name="item"),
    path("watchlist",views.view_watchlist,name="view_watchlist"),
    path("watchlist/<int:p_id>",views.add_watchlist,name="watchlist"),
    path("watchlist/remove/<int:p_id>",views.remove_watchlist,name="remove_watchlist"),
    path("addItem",views.add_item,name="add_item")
]
