
from django.urls import path
from missing_data import views

urlpatterns = [
    path("", views.home, name="home"),
    path("jupyter", views.jupyter_notebook, name="Notebook"),
    path("median_substitute", views.median_substitute, name="median_substitute"),
    path("mean_substitute", views.mean_substitute, name="mean_substitute"),
    path("mode_substitute", views.mode_substitute, name="mode_substitute"),
    path("ml_substitute", views.ml_substitute, name="ml_substitute"),
    path("dev", views.dev, name="dev"),

]
