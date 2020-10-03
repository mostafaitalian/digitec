from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django import forms
from .models import  Engineer, Area
from machine.models import EngineerReview
from django.contrib.auth import get_user_model

class EngineerForm(forms.ModelForm):
    
    class Meta:
        model=Engineer
        fields = '__all__'

class AreaForm(forms.ModelForm):
    
    class Meta:
        model = Area
        fields = '__all__'


AreaInlineFormset = inlineformset_factory(
    Area,
    Engineer,
    form=EngineerForm,
    extra=1,
    can_delete=False,
    can_order=False
)



class ReviewForm(ModelForm):
    #auther = forms.ModelChoiceField(queryset=Engineer.objects.all(),disabled=True)
    #review = forms.TextField(widget=forms.Textarea)
    
    state_choices = (('pending','pending'),('published','published'),('rejected','rejected'))

    state = forms.ChoiceField(help_text='if you do not set it it will be pending', choices=state_choices, required=True)
    class Meta:
        model=EngineerReview
        fields = '__all__'
        
class ApproveReviewForm(forms.Form):
    new_comment = forms.CharField(widget=forms.Textarea, required=False)
    approval_choices= (('approved', 'approve this tweet and post it in twitter'),('rejected', 'reject this review and send back to the creator for editing'))
    approval = forms.ChoiceField(choices=approval_choices,widget=forms.RadioSelect)