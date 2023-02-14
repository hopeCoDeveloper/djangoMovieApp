from django.urls import path,include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list,movie_details
from watchlist_app.api.views import (WatchListAV,WatchDetailAV,StreamPlatformAV
                                    ,StreamDetailAV,ReviewList,ReviewDetail
                                    ,ReviewCreate,StreamPlatformVS,UserReview,WatchListGV)

router = DefaultRouter()
router.register('stream',StreamPlatformVS, basename = 'streamplatform')

urlpatterns = [
    path('list/',WatchListAV.as_view(),name='movie-list'),
    path('<int:pk>/',WatchDetailAV.as_view(),name='movie-detail'),
    path('list2/',WatchListGV.as_view(),name='watch-list'),   

    path('',include(router.urls)),
    # path('stream/',StreamPlatformAV.as_view(),name='stream_platform'),
    # path('stream/<int:pk>',StreamDetailAV.as_view(),name='stream_detail'),
    
    path('<int:pk>/reviews/',ReviewList.as_view(),name = 'review_list'),
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name = 'review_create'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review_detail'),
    path('reviews/',UserReview.as_view(),name='user_review_review')
]