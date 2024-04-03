from django.urls import include, path
from .views import MissingDataApiView, Development, MeanSubstitute, MedianSubstitute, ModeSubstitute

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('person', MissingDataApiView.as_view()),
    path('person/mean', MeanSubstitute.as_view()),
    path('person/median', MedianSubstitute.as_view()),
    path('person/mode', ModeSubstitute.as_view()),
    path('dev/person/deleteall', Development.as_view()),
]