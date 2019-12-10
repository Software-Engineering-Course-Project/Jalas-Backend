from django.urls import path

from . import views

urlpatterns = [
    path('available_room/<int:select_id>/', views.RoomsView.as_view()),
    path('set_room/<int:room>/<int:select_id>', views.SetRoomView.as_view()),
    path('set_date/<int:select_id>/', views.SetDateView.as_view()),
    path('set_cancel/<int:select_id>', views.SetCancel.as_view()),
]
