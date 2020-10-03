from django.shortcuts import render,get_object_or_404, redirect

from .forms import ReviewForm, EngineerForm,ApproveReviewForm, AreaForm, AreaInlineFormset
from django.db import transaction
from .models import Engineer, Area
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import DetailView, View, CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect
from numpy.distutils.from_template import template_name_re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Count
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from twython import Twython
from django.core.mail.backends.smtp import EmailBackend
# Create your views here.
from django.core.mail import get_connection
from django.core.mail import EmailMessage
import datetime
from rest_framework.generics import ListCreateAPIView
from .serializers import EngineerSerializer, AreaSerializer
from rest_framework.permissions import IsAdminUser
from machine.models import EngineerReview, Comment


class AreaEngineerCreateView(CreateView):
    template_name="engineer/create_area_with_engineer.html"
    model = Area
    form_class = AreaForm
    # success_url = reverse_lazy(engineer:engineer-create)
    success_url = 'engineer/list'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = AreaInlineFormset(self.request.POST)
        else:
            data['formset'] = AreaInlineFormset()    
        return data
    def form_valid(self, form):
        data = self.get_context_data()
        formset = data['formset']
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)                

class EngineerCreateView(CreateView):
    template_name="engineer/create_engineer.html"
    model = Engineer
    form_class = EngineerForm
    success_url = reverse_lazy("engineer:engineer_create")
class AreaCreateView(CreateView):
    template_name="engineer/create_area.html"
    model = Area
    form_class = AreaForm
    success_url = reverse_lazy("engineer:engineer_create")
# def create_area_with_engineer(request):
#     if request.method == 'POST':
#         formset = AreaInlineFormset(request.POST)
#         return redirect('engineer/create/')
#     else:
#         formset=AreaInlineFormset(instance=Area())
#     return render(request, 'engineer/create_area_with_engineer.html', {'formset':formset})


def review_create(request):
    
    if request.method=='POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.state = 'pending'
            new_review.save()
            engineer = form.cleaned_data['auther']
            review = form.cleaned_data['review']
            subject = 'review is created waiting for checking'
            message = 'reviews was just made by {} and is talking about\n {}. '.format(engineer.name, review)
            send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=['eng_mustafa_yossef@hotmail.com'])
            return HttpResponseRedirect('/machine/list1/')
    else:
        form = ReviewForm(request.POST)
        return render(request, 'machine/create_review.html', {'form':form})
            
class GetPostMixin:
    form_class = None
    template_name= ''
     
    def get(self,request):
        
        engineer = Engineer.objects.get(engineer = self.request.user)
        auther= Engineer.objects.get(id=engineer.id)    
        form = self.form_class(initial={'auther':auther})
        form.save(commit=False)
        #print(self.request.user, form.auther)
        reviews = EngineerReview.objects.filter(state='pending')
        return render(request, self.template_name, {'form':form, 'reviews':reviews})
    def post(self, request):
        form = self.form_class(request.POST)
        print(form.is_bound,form.is_valid)

        if form.is_valid()==True:
            #new_tweet = form.save(commit=False)
            #new_tweet.state = 'pending'

            new_review = EngineerReview()
            new_review.auther = form.cleaned_data['auther']
            print(new_review.auther)
            new_review.state = form.cleaned_data['state']
            print(new_review.state)
            new_review.review = form.cleaned_data['review']
            print(new_review.review)
            new_review.save()

            form.save()
            return HttpResponseRedirect('engineer/review/create')
        else:
            engineer = Engineer.objects.get(engineer = self.request.user)
            auther= Engineer.objects.get(id=engineer.id)    
            form = self.form_class(initial={'auther':auther})
            reviews = EngineerReview.objects.filter(state='pending')
            return render(request,self.template_name, {'form':form,'reviews': reviews})    

class CreateReview(GetPostMixin, View):
    
    model = EngineerReview
    form_class = ReviewForm
    template_name= 'machine/create_review.html'
class PostCreate(CreateView):
    form_class = ReviewForm
    template_name = 'machine/create_review.html'
    model = EngineerReview
    def get_initial(self,request):
        engineer = Engineer.objects.get(engineer = request.user.id)
        auther= Engineer.objects.get(id=engineer.id)
        initial = super().get_initial()
        initial['auther']=auther
        return initial
    def get(self, request):
        form = self.form_class(initial=self.get_initial(request))
        #print(form.fields.get_values())
        reviews = EngineerReview.objects.filter(state='pending')

        return render(request, self.template_name, {'form' : form, 'reviews':reviews})
    def post(self,request):
        engineer = Engineer.objects.get(engineer = request.user.id)
        auther= Engineer.objects.get(id=engineer.id)
        #form.auther=auther
        form = self.form_class(initial={'auther':auther},data=self.request.POST)
        form.full_clean()
        print(form.is_valid, form.is_bound, form.data, form.errors)
        if form.is_valid():
            new_post = form.save()
            send_review_email()
            return HttpResponseRedirect('/engineer/review/thank_you')
        else:
            form = self.form_class(initial=self.get_initial(request))
            return render(request, self.template_name,{'form':form})
class ReviewDetailView(DetailView):
    model = EngineerReview
    queryset = EngineerReview.objects.all()
    template_name = 'engineer/review_detail.html'
    context_object_name='review'
    
    def get_object(self, queryset=None):
        review_id = self.request.Get.get('review_id')
        try:
            review = EngineerReview.objects.get(id=review_id)
        except:
            raise ObjectDoesNotExist('can not find the review')
        return review
def send_review_email():
    subject = 'Action required: review tweet'
    body = 'A new tweet has been submitted for approval.Please review it as soon as possible.'
    send_mail(subject, body, settings.EMAIL_HOST_USER,[settings.TWEET_APPROVER_EMAIL,])
dic={'a':'a','b':'b'}
dic.values()
print(list(dic.values())[0])
print(dic.values())
def thank_you(request):
    reviews_in_queue = list(EngineerReview.objects.filter(state='pending').aggregate(Count('id')).values())[0]
    print(reviews_in_queue)
    return render(request, 'engineer/thankyou.html', {'reviews_in_queue':reviews_in_queue})
@permission_required('engineer.can_approve_or_reject_review')
@login_required
def list_reviews(request):
    pending_reviews = EngineerReview.objects.filter(state='pending').order_by('-created_at')
    published_reviews = EngineerReview.objects.filter(state='published').order_by('-created_at')
    return render(request,
                  'engineer/list_review.html',
                  {'pending_reviews':pending_reviews,'published_reviews':published_reviews})
def preview_review(request, review_id):
    review = get_object_or_404(EngineerReview, id=review_id)
    print(review.review)
    if request.method=='POST':
        form = ApproveReviewForm(request.POST)
        print(form.is_bound, form.is_valid)
        if form.is_valid():
            new_comment = form.cleaned_data['new_comment']
            approval = form.cleaned_data['approval']
            if approval=='approved':
                send_approve_email(review, new_comment)
                publish_review(review)
                review.state='published'
                review.published_at = datetime.datetime.now()
            else:
                #link = request.build_absolute_uri(reverse())
                review.state = 'rejected'
                send_rejection_email(review, new_comment)
                if new_comment:
                    c = Comment(engineer=review.auther, engineer_review=review, text=new_comment) 
            return HttpResponseRedirect('/approve/')
        else:
            form = ApproveReviewForm()
            return render(request, 'engineer/preview_review2.html', {'form':form,'review':review,'comments':review.comment_set.all()})
    else:
        form = ApproveReviewForm()
        return render(request, 'engineer/preview_review2.html', {'form':form})
def send_approve_email(review, new_comment):
    subject = 'approved'
    body = 'your review -{}- was published in twitter'.format(review.review)
    send_mail(subject, message=body, from_email='eng_mustafa_yossef@hotmail.com', recipient_list=[settings.DEFAULT_FROM_EMAIL,])
    
def publish_review(review):
    twitter = Twython(twitter_token=settings.TWITTER_CONSUMER_KEY,
                        twitter_secret=settings.TWITTER_CONSUMER_SECRET,
                        oauth_token=settings.TWITTER_OAUTH_TOKEN,
                        oauth_token_secret=settings.TWITTER_OAUTH_TOKEN_SECRET)
    twitter.updateStatus(status=review.text.encode('utf-8'))
def send_rejection_email(review, new_comment):
    subject = 'rejected'
    body = 'your review -{}- was rejected by manager with notification -{}-please edit it and send it back'.format(review.review,new_comment)
    backend = EmailBackend(host='smtp-mail.hotmail.com', port='587', username='eng_mustafa_yossef@hotmail.com', password='100aa100', use_tls=True, fail_silently=False)
    connection = get_connection(backend=settings.EMAIL_BACKEND)
    #backend.send_messages(email_messages)
    connection.open()
    email1 = EmailMessage(
    'Hello','Body goes here','from@example.com',['to1@example.com'],connection=connection,)
    email1.send()
    send_mail(subject=subject,
              message=body,
              from_email='eng_mustafa_yossef@hotmail.com',
              recipient_list=[settings.DEFAULT_FROM_EMAIL],
              auth_user='eng_mustafa_yossef@hotmail.com',
              auth_password='100aa100',
              connection=connection)
    connection.close()
'''class CreateApprovalView(CreateView):
    form_class=ApproveReviewForm
    template_name='engineer/approval.html'''


class EngineerApiView(ListCreateAPIView):
    queryset=Engineer.objects.all()
    serializer_class = EngineerSerializer
    # permission_classes = (IsAdminUser,) 

class AreaApiView(ListCreateAPIView):
    queryset=Area.objects.all()
    serializer_class = AreaSerializer   


