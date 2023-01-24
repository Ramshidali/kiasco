#standerd
import json
import datetime
#django
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
#local
from main.functions import generate_form_errors, get_auto_id
from offers.forms import OffersForm
from main.decorators import role_required
from offers.models import Offers


# Create your views here.


@login_required
@role_required(['superadmin'])
def offers(request):
    """
    product offers listings
    :param request:
    :return: offers list view
    """
    instances = Offers.objects.filter(is_deleted=False).order_by("-id")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(product__name__icontains=query) 
        )
        title = "Offer - %s" % query
        filter_data['q'] = query

    context = {
        'instances': instances,
        'page_name' : 'Offers',
        'page_title' : 'Offers',
        'filer_data' : filter_data,
    }

    return render(request, 'admin_panel/offers/offers.html', context)


@login_required
@role_required(['superadmin'])
def create_offer(request, pk):
    """
    create and update operation of offer
    :param request:
    :param pk:
    :return:
    """
    # check pk for getting instance
    if pk:
        instance = get_object_or_404(Offers, pk=pk)
        response_title = "Successfully Updated."
        response_message = "Offer updated successfully."
    else:
        instance = ''
        response_title = "Successfully Created."
        response_message = "Offer created successfully."

    message = ''
    if request.method == 'POST':
        # if instance go to edit
        if instance:
            form = OffersForm(request.POST, instance=instance)
        else:
            form = OffersForm(request.POST)
            
        if form.is_valid():
            data = form.save(commit=False)
            if not instance:
                data.auto_id = get_auto_id(Offers)
                data.creator = request.user
            else:
                data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": response_title,
                "message": response_message,
                'redirect': 'true',
                "redirect_url": reverse('offers:offers')
            }
    
        else:
            message = generate_form_errors(form ,formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
                
        if not instance :
            form = OffersForm()
        else:
            form = OffersForm(instance=instance)
            
        context = {
            'form': form,
            'page_name' : 'Create Offer',
            'page_title' : 'Create Offer',
            'url' : reverse('offers:create_offer', kwargs={'pk':''}),
            'is_need_forms' : True,
            'is_need_datetime_picker' : True,
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_offer(request, pk):
    """
    offer deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Offers.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Offer Successfully Deleted.",
        "redirect": "true",
        'url' : reverse('offers:create_offer', kwargs={'pk':''}),
    }
  
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')