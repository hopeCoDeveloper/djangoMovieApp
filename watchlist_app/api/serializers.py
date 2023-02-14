from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform,Review

#Model Serializer
#it defines create and update function automaticly
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        #fields = "__all__"
        exclude = ('watchlist',)
class WatchListSerializer(serializers.ModelSerializer):
    #reviews = ReviewSerializer(many = True,read_only = True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields= "__all__"
        #fields = ['id','name','description']
        #exclude = ['active']

class StreamPlatformSerializer(serializers.ModelSerializer):
    #the name watchlist is important it should be the the same name as defined in relationship
    watchlist = WatchListSerializer(many=True,read_only=True)

    #it will return __str__ inside the model
    #watchlist = serializers.StringRelatedField(many=True)

    #to show a link to the movie
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many = True,
    #     read_only = True,
    #     view_name = 'movie-detail'
    # )

    class Meta:
        model = StreamPlatform
        fields= "__all__"




#Normal Serializer
# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('Name is too short!')

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     # for post
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#     # for put
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.save()
#         return instance

#     #field level validation
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError('Name is too short!')
#     #     else:
#     #         return value

#     #object level validation
#     def validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('Title and description should be diffrent!')
#         else:
#             return data