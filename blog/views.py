from lib2to3.fixes.fix_input import context
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, View, FormView
from blog.models import Event
from blog.forms import MemberForm, ContactForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_str
from blog.models import User
from blog.tokens import account_activation_token
from blog.forms import EmailForm, PeopleForm
from django.core.mail import send_mail
from datetime import datetime


# Create your views here.



class IndexView(View):
    def get(self,request):
        form = MemberForm()
        return render(request,'blog/index.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


        return render(request,'blog/index.html', {'form':form})



class EventsListView(ListView):
    template_name = 'blog/event-listing.html'
    model = Event
    paginate_by = 2


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.now()
        upcoming_events = Event.objects.filter(created_at__gte=now).order_by('created_at')[:2]
        latest_events = Event.objects.filter(created_at__lt=now).order_by('-created_at')
        context['upcoming_events'] = upcoming_events
        context['latest_events'] = latest_events

        return context


class EventsDetailView(TemplateView):
    template_name = 'blog/event-detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=self.kwargs['pk'])
        context['event'] = event
        return context
    


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('verify_email_complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'blog/auth/email/verify-email-confirm.html')




def sending_email(request):
    form = EmailForm()
    if request.method == 'GET':
        subject = request.GET.get('subject')
        message = request.GET.get('message')
        from_email = request.GET.get('from_email')
        to = request.GET.get('to')
        send_mail(subject, message, from_email, [to])
    return render(request, 'blog/sending-email.html', {'form': form})
    

def verify_email_done(request):
    return render(request, 'blog/auth/email/verify-email-done.html')    


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify_email_complete')   
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'blog/auth/email/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'blog/auth/email/verify_email_complete.html')


class PeopleSave(View):
    def get(self,request):
        form = PeopleForm()
        return render(request,'blog/index.html',{'form':form})

    def post(self, request, *args, **kwargs):
        form = PeopleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


        return render(request,'blog/index.html',{'form':form})
    

class ContactSave(View):
    def get(self,request):
        form = ContactForm()
        return render(request,'app/index.html',{'form':form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


        return render(request,'app/index.html',{'form':form})    