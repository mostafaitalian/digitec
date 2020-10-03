from rest_framework import serializers
from .models import Machine,Call, EngineerReview,Report, Comment, ImageReview
from engineer.models import Engineer
from customer.models import Department

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields = '__all__'
class ImagesReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageReview
        fields ='__all__'

class EngineerReviewSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)
    images = ImagesReviewSerializer(many=True)
    class Meta:
        model = EngineerReview
        fields = '__all__'
        depth=1

class MachineSerializer(serializers.ModelSerializer):
    # engineers = serializers.PrimaryKeyRelatedField(many=True, queryset=Engineer.objects.all())
    # engineerss = serializers.ListSerializer(child=engineers)
    
    # to make serializer accept list of data
    # def __init(self, *args,**kwargs):
    #     many = kwargs.pop('many',True)
    #     super().__init__(many=many, *args, **kwargs)
    # reviews = serializers.RelatedField()

    reviews = EngineerReviewSerializer(many=True, required=False)
    # department = serializers.StringRelatedField()

    class Meta:
        model = Machine
        fields= ('id','machine_category', 'customer', 'department', 'area','name', 'serial',
        'serial2', 'reviews', 'machine_model', 'slug', 'description', 'added', 'speed','engineers' )
        # exclude=('engineers',)
        depth=1

class CallSerializer(serializers.ModelSerializer):
    # machine=  MachineSerializer()
    class Meta:
        model=Call
        fields = '__all__'

