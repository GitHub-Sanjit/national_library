from django.urls import path
from .import views
from accounts.views import activate

urlpatterns = [
    path('details/<int:id>', views.DetailsPostView.as_view(), name='details_post'),
    path('purchase/<int:id>/', views.BorrowBookView.as_view(), name='borrow_book'),
    path('wishlist/<int:id>/', views.AddWishListView.as_view(), name='add_wishlist'),
    path('active/<uid64>/<token>/', activate, name='activate'),
]
