from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from watchlist_app.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from watchlist_app.api.pagination import WatchListPagination,WatchListLOPagination,WatchListCPagination
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class UserReview(generics.ListAPIView):
     #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #filtering against user
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     #because review_user is a forign key if you want to access the username you should use __
    #     return Review.objects.filter(review_user__username=username)
    #Filtering against query parameters
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)

#generic class based view / concrete class view
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    #throttle_classes = [ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()
    #use this method to override create
    def perform_create(self,serializer):
        pk = self.kwargs['pk']
        movie = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie,review_user=review_user)

        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie!')
        #calculating the avg rating and number of rating
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
        movie.number_rating = movie.number_rating + 1
        movie.save()

        serializer.save(watchlist = movie,review_user= review_user)



class ReviewList(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #object level permision
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    #it only work in generic class view
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]


#mixins and generic ApiView
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self,request,*arg,**kwargs):
#         return self.list(request,*arg,**kwargs)

#     def post(self,request,*arg,**kwargs):
#         return self.create(request,*arg,**kwargs)

# model view set it perform create list retrieve and destroy auto
class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

#view sets
# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(user)
#         return Response(serializer.data)

#     def create(self,request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)



class StreamPlatformAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,many = True,context = {'request' : request})
        return Response(serializer.data)
    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class StreamDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform)
            return Response(serializer.data)
        except StreamPlatform.DoesNotExist:
            return Response({'Error' : 'Not found'},status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#just for test
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination
    #it only work in generic class view
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields=['title','platform__name']

    #search filter
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']
    
    #ordering filter
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']

class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    #GET method
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)
    #POST method
    def post(self,request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    #GET method
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie)
            return Response(serializer.data)
        except WatchList.DoesNotExist:
            return Response({'Error' : 'Not found'},status=status.HTTP_404_NOT_FOUND)
    #PUT method
    def put(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    #DELETE method
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#             serializer = MovieSerializer(movie)
#             return Response(serializer.data)
#         except Movie.DoesNotExist:
#             return Response({'Error' : 'Movie not found'},status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie,data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)