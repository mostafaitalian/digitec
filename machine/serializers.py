from rest_framework import serializers
from .models import Machine,Call, EngineerReview,Report, Comment, ImageReview, ImageReport
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

class ImagesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageReport
        fields ='__all__'

class EngineerReviewSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)
    images = ImagesReviewSerializer(many=True)
    class Meta:
        model = EngineerReview
        fields = '__all__'
        depth=1


class ReportSerializer(serializers.ModelSerializer):
    # machine=  MachineSerializer()
    report_images = ImagesReportSerializer(many=True, required=False)
    class Meta:
        model=Report
        fields = '__all__'
        depth = 1 


class ReportSerializer1(serializers.ModelSerializer):
    # machine=  MachineSerializer()
    report_images = ImagesReportSerializer(many=True, required=False)
    class Meta:
        model=Report
        fields = '__all__'


class CallSerializer(serializers.ModelSerializer):
    # machine=  MachineSerializer()
    reports = ReportSerializer(many=True, required=False)
    class Meta:
        model=Call
        fields = '__all__'
        depth=1






class CallAreaSerializer(serializers.ModelSerializer):
    # machine=  MachineSerializer()
    reports = ReportSerializer(many=True, required=False)
    class Meta:
        model=Call
        fields = ['notification_number', 'status', 'machine', 'customer',
        'engineer', 'created_date', 'real_assigned_date', 'start_of_call',
        'real_completed_date', 'response_time', 'down_time', 'response_time_end_date',
        'response_time_tail_end_date', 'down_time_end_date', 'first_time_finish',
        'callback_call',
        'delayed_call', 'no_of_visits', 'response_success_call', 'down_success_call',
        'fault', 'notes_from_customer']

        depth=1

class MachineAreaSerializer(serializers.ModelSerializer):
    # engineers = serializers.PrimaryKeyRelatedField(many=True, queryset=Engineer.objects.all())
    # engineerss = serializers.ListSerializer(child=engineers)
    
    # to make serializer accept list of data
    # def __init(self, *args,**kwargs):
    #     many = kwargs.pop('many',True)
    #     super().__init__(many=many, *args, **kwargs)
    # reviews = serializers.RelatedField()
    calls = CallAreaSerializer(many=True, required=False)
    reviews = EngineerReviewSerializer(many=True, required=False)
    # department = serializers.StringRelatedField()

    class Meta:
        model = Machine
        fields= ('id','machine_category','customer', 'department', 'area',
        'reviews', 'machine_model', 'machine_location', 'added', 'calls')
        # exclude=('engineers',)

        depth=1


class MachineSerializer(serializers.ModelSerializer):
    # engineers = serializers.PrimaryKeyRelatedField(many=True, queryset=Engineer.objects.all())
    # engineerss = serializers.ListSerializer(child=engineers)
    
    # to make serializer accept list of data
    # def __init(self, *args,**kwargs):
    #     many = kwargs.pop('many',True)
    #     super().__init__(many=many, *args, **kwargs)
    # reviews = serializers.RelatedField()
    calls = CallSerializer(many=True, required=False)
    reviews = EngineerReviewSerializer(many=True, required=False)
    # department = serializers.StringRelatedField()

    class Meta:
        model = Machine
        fields= ('id','machine_category','customer', 'department', 'area',
        'reviews', 'machine_model', 'machine_location', 'added', 'calls')
        # exclude=('engineers',)
        depth=1

