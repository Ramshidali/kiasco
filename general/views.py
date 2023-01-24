#standerd
import json
import datetime
from multiprocessing.connection import deliver_challenge
import xlrd
# django
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Q
#local
from main.decorators import role_required
from general.models import Contacts, Location
from main.functions import get_auto_id,generate_form_errors
from general.forms import ContactsForm, LocationForm,FileForm
from web.forms import BannersForm
from web.models import Banner


# Create your views here.
@login_required
@role_required(['superadmin'])
def locations(request):
    """
    location listings
    :param request:
    :return: product list view
    """
    instances = Location.objects.filter(is_deleted=False)

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(pincode__icontains=query)
        )
        title = "Location - %s" % query
        filter_data['q'] = query

    context = {
        'instances': instances,
        'page_name' : 'Locations',
        'page_title' : 'Locations'
    }

    return render(request, 'admin_panel/general/locations.html', context)



@login_required
@role_required(['superadmin'])
def create_location(request):
    """
    create and update operation of location
    :param request:
    :pk for using edit each location
    :return:
    """
    if request.method == 'POST':

        form = LocationForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Location)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Location created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('general:locations')
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

        form = LocationForm()

        context = {
            'form': form,
            'page_name' : 'Create Location',
            'page_title' : 'Create Location',
            'is_need_select2' : True,
            'url' : reverse('general:create_location'),
        }

        return render(request, 'admin_panel/create/create.html',context)



@login_required
@role_required(['superadmin'])
def edit_location(request,pk):
    """
    edit operation of location
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Location, pk=pk)

    message = ''
    if request.method == 'POST':
        form = LocationForm(request.POST,instance=instance)

        if form.is_valid():

            #create product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Location created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('general:locations')
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

        form = LocationForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Create Location',
            'page_title' : 'Create Location',
            'is_need_select2' : True,
            'url' : reverse('general:create_location'),
        }

        return render(request, 'admin_panel/create/create.html',context)



@login_required
@role_required(['superadmin'])
def delete_location(request, pk):
    """
    location deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Location.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Location Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('general:locations')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')



@login_required
@role_required(['superadmin'])
def banners(request):
    """
    banners listings
    :param request:
    :return: product list view
    """
    instances = Banner.objects.filter(is_deleted=False)

    context = {
        'instances': instances,
        'page_name' : 'Banners',
        'page_title' : 'Banners'
    }

    return render(request, 'admin_panel/general/banners.html', context)


@login_required
@role_required(['superadmin'])
def create_banner(request):
    """
    create operation of location
    :param request:
    :pk for using edit each location
    :return:
    """
    if request.method == 'POST':

        form = BannersForm(request.POST,files=request.FILES)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Banner)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Banner created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('general:banners')
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = BannersForm()

        context = {
            'form': form,
            'page_name' : 'Create Banner',
            'page_title' : 'Create Banner',
            'url' : reverse('general:create_banner'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_banner(request, pk):
    """
    banner deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """

    Banner.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Banner Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('general:banners')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
@role_required(['superadmin'])
def update_contacts(request):
    instance = Contacts.objects.first()
    if request.method == "POST":
        form = ContactsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():

            form.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Contacts Successfully Updated.",
                "redirect": "true",
                "redirect_url": reverse('general:update_contacts')
            }
        else:
            message = str(generate_form_errors(form, formset=False))

            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = ContactsForm(instance=instance)
        context = {
            "form": form,
            "title": "Contacts Details",
            "instance": instance,
            "redirect": True,
            "url": reverse('general:update_contacts'),
            'page_name' : 'Contacts Details',
            'page_title' : 'Contacts Details',
            'url' : reverse('general:create_banner'),
        }

        return render(request, 'admin_panel/general/contacts.html', context)


@login_required
@role_required(['superadmin'])
def upload_locations(request):
    if request.method == 'POST':
        form = FileForm(request.POST,request.FILES) 
        
        if form.is_valid():
            input_excel = request.FILES['file']
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)

            dict_list = []
            keys = [str(sheet.cell(0, col_index).value) for col_index in range(sheet.ncols)]
            for row_index in range(1, sheet.nrows):
                d = {keys[col_index]: str(sheet.cell(row_index, col_index).value)
                    for col_index in range(sheet.ncols)}
                dict_list.append(d)

            is_ok = True
            message = ''
            row_count = 0
            for item in dict_list:
                name = item['Name']
                pincode = item['Pincode']
                delivery_charge = item['Delivery Charge']
                min_day_of_delivery = item['Min Days of Delivery']
                state = item['State']
                
                pincode = (pincode).split(".")[0]
                min_day_of_delivery = (min_day_of_delivery).split(".")[0]
                row_count +=1
                
                if State.objects.filter(name=state).exists():
                    state = State.objects.get(name=state)
                else:
                    response_data = {
                        "status": "false",
                        "stable": "true",
                        "title": "State Not Found",
                        "message": f"Invalid State Found at row: {row_count}"
                    }
                    return JsonResponse(response_data)

                # if  Location.objects.filter(pincode=pincode,is_deleted=False).exists():
                #     response_data = {
                #         "status": "false",
                #         "stable": "true",
                #         "title": "Pincode Duplication Founded",
                #         "message": f"Pincode Repeats on row: {row_count}"
                #     }
                #     return JsonResponse(response_data)
                # else:
                        
                location = Location.objects.create(
                    name = name,
                    pincode =pincode,
                    delivery_charge = delivery_charge,
                    min_day_of_delivery = min_day_of_delivery,
                    state = state,
                    auto_id =  get_auto_id(Location),
                    date_added = datetime.datetime.now(),
                    creator= request.user,
                    updater=request.user,
                )
                location.save()
                    
                response_data = {
                    "status" : "true",
                    "title" : "Successfully Uploaded",
                    "message" : "Pincode Successfully Added.",
                    "redirect" : "true",
                    "redirect_url" : reverse('general:locations')
                }
                

            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        else:
            form = FileForm()
            title = "Upload Pincode"
            context = {
                "form" : form,
                "title" : title,

                "is_need_popup_box" : True,
                "is_need_dropzone" : True
            }
            return render(request, 'admin_panel/create/create.html',context)
    else:
        form = FileForm()

        context = {
            "form" : form,
            'page_name' : 'Locations',
            'page_title' : 'Upload Location',
            "redirect" : True,
            "url" : reverse('general:upload_locations'),

            "is_need_popup_box" : True,
            "is_need_dropzone" : True,
            "is_upload" : True,
        }
        return render(request, 'admin_panel/create/create.html',context)