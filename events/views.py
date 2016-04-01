from django.shortcuts import render
from .models import Event
from .forms import EventForm, HostForm
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import *
# Create your views here.

###########

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
from django_messages.models import Message
from django_messages.forms import ComposeForm,EnquiryForm
from django_messages.utils import format_quote, get_user_model, get_username_field
from products.models import Product
from services.models import Service
from events.models import Event
from authtools.models import User
##########



def event(request):
    model = Event
    event = Event.objects.all()

    # Handle file upload
    if request.method == 'POST':
        form = EventForm(request.POST , request.FILES)
        if form.is_valid():
            event = Event(user=request.user, snap=request.FILES['snap'], eventtype = request.POST['eventtype'],duration = request.POST['duration'],dresscode = request.POST['duration'],date_event = request.POST['date_event'], description = request.POST['description'], place = request.POST['place'],)
            event.save()

            # Redirect to the document list after POST
            return redirect('/events/')
    else:
        form = EventForm() # A empty, unbound form
    
    event = Event.objects.all()
   # Load documents for the list page
    
    # Render list page with the documents and the form
    return render_to_response(
        'events/event.html',
        { 'event': event,'form': form,},
        context_instance=RequestContext(request)
    )


def event_detail(request, pk):
    model = Event
    event = get_object_or_404(Event, pk=pk)
    user_id=event.user.id
    return render(request,  'events/eventdetail.html', {'event': event })

@login_required
def host(request):
    model = Event
    # Handle file upload
    if request.method == 'POST':
        form = EventForm(request.POST , request.FILES)
        if form.is_valid():
            event = Event(user=request.user, snap=request.FILES['snap'], eventtype = request.POST['eventtype'],duration = request.POST['duration'],dresscode = request.POST['duration'],date_event = request.POST['date_event'], description = request.POST['description'], place = request.POST['place'],)
            event.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('events:host_detail',args=(event.pk,)))
    else:
        form = EventForm() # A empty, unbound form

   # Load documents for the list page

    # Render list page with the documents and the form
    return render_to_response(
        'events/hostevent.html',{'form': form},
        context_instance=RequestContext(request)
    )

@login_required
def host_detail(request, pk):
    model = Event
    event = get_object_or_404(Event, pk=pk)
    return render(request,  'events/host_detail.html', {'event': event })

@login_required
def host_edit(request,pk):
    model = Event
    event = get_object_or_404(Event, pk=pk)    
    # Handle file upload
    if request.method == 'POST':
        form = HostForm(request.POST,request.FILES, instance=event )
        if form.is_valid():
            event.user = request.user
            event.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('events:host_detail',args=(event.pk,)))
    else:
        form = HostForm(instance=event) # A empty, unbound form
# Render list page with the documents and the form
    return render(request,
        'events/hostevent.html',{'form': form})


@login_required
def devent_detail(request):
    model = Event
    event = Event.objects.filter(user_id = request.user.id)
    return render(request,  'events/detail.html', {'event': event })

#########################################################################################
@login_required
def host_public(request, pk, recipient=None, form_class=ComposeForm,
        template_name='django_messages/composee.html', success_url=None, recipient_filter=None):
    post = get_object_or_404(Event, pk=pk)
    #zipcode = User.objects.filter(name = 121212)
    zipcode = User.objects.all()
    if request.method == "POST":
        #sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('home')
            if 'next' in request.GET:
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
            # return render(request, 'products/post_list.html', {'posts': posts })
    else:
        form = form_class()
        if recipient is not None:
            recipients = [u for u in User.objects.filter(**{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
            form.fields['recipient'].initial = recipients
    return render_to_response('django_messages/composee.html', {'form': form, 'post': post, 'zipcode': zipcode, }, context_instance=RequestContext(request))
