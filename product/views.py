#standerd
import json
import datetime
#django
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.core.serializers import serialize
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.forms.formsets import formset_factory
#thirdparty
from dal import autocomplete
#local
from offers.models import Offers
from product.forms import *
from main.functions import generate_form_errors, get_auto_id, paginate
from product.models import *
from main.decorators import role_required
from product.models import PRODUCT_TYPE_CHOICE as product_type

# # Create your views here.

class DeliveryLocationsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self, *args, **kwargs):
        items = Location.objects.filter(is_deleted=False)
        if self.q:
            items = items.filter(Q(name__istartswith=self.q))
        return items


class MetaKeywordsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self, *args, **kwargs):
        items = MetaKeyword.objects.filter(is_deleted=False)
        if self.q:
            items = items.filter(Q(name__istartswith=self.q))
        return items
    
    
class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        items = ProductCategory.objects.filter(is_deleted=False)

        if self.q:
            items = items.filter(Q(auto_id__istartswith=self.q) |
                                 Q(name__istartswith=self.q)
                                 )

        return items

    def create_object(self, text):

        if not ProductCategory.objects.filter(is_deleted=False, name=text).exists():
            category = ProductCategory.objects.create(
                auto_id=get_auto_id(ProductCategory),
                name=text,
                creator=self.request.user,
                updater=self.request.user
            )
            return category


# #*******************************CRUD Meta Keyword***************************************


@login_required
@role_required(['superadmin'])
def meta_keyword(request):
    """
    meta keyword listings
    :param request:
    :return: meta keyword list view
    """
    instances = MetaKeyword.objects.filter(is_deleted=False).order_by("-id")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) 
        )
        title = "Meta Keyword - %s" % query
        filter_data['q'] = query
    

    context = {
        'instances': instances,
        'page_name' : 'Meta Keyword',
        'page_title' : 'Meta Keyword',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/product/meta_keyword.html', context)


@login_required
@role_required(['superadmin'])
def create_meta_keyword(request):
    """
    create operation of meta keyword
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        # if instance go to edit
        form = MetaKeywordsForm(request.POST)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(MetaKeyword)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Meta Keyword created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:meta_keyword')
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
        
        form = MetaKeywordsForm()

        context = {
            'form': form,
            'page_name' : 'Create Meta Keyword',
            'page_title' : 'Create Meta Keyword',
            'url' : reverse('product:create_meta_keyword'),
        }

        return render(request, 'admin_panel/create/create.html',context)

    
@login_required
@role_required(['superadmin'])
def edit_meta_keyword(request,pk):
    """
    edit operation of meta_keyword
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(MetaKeyword, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = MetaKeywordsForm(request.POST,instance=instance)
        
        if form.is_valid():
            
            #update meta keyword
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Meta Keyword Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:meta_keyword')
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
        
        form = MetaKeywordsForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Create Meta Keyword',
            'page_title' : 'Create Meta Keyword',
            'is_need_select2' : True,
            'url' : reverse('product:meta_keyword'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_meta_keyword(request, pk):
    """
    meta keyword deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    MetaKeyword.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:meta_keyword')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

#*******************************CRUD Product***************************************


@login_required
@role_required(['superadmin'])
def product_list(request):
    """
    product listings
    :param request:
    :return: product list view
    """
    instances = Product.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(category__name__icontains=query) 
        )
        title = "Products - %s" % query
        filter_data['q'] = query
          

    context = {
        'instances': instances,
        'page_name' : 'Products',
        'page_title' : 'Products',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/product/product_list.html', context)


@login_required
@role_required(['superadmin'])
def product_details(request,pk):
    """
    product single view using product pk
    :param request:
    :pk
    :return: product list view
    """
    instance = Product.objects.get(pk=pk, is_deleted=False)
    #checking percentage between mrp and price for getting off precentage
    persentage = (instance.mrp - instance.price)/instance.mrp * 100
    product_variant = ProductVariant.objects.filter(product__pk=instance.pk,is_deleted=False)
    more_images = ProductImage.objects.filter(product__pk=instance.pk,is_deleted=False)
    
    context = {
        'instance': instance,
        'persentage' : int(persentage),
        'product_variant' : product_variant,
        'more_images' : more_images,
        'page_name' : 'Product Details',
        'page_title' : 'Product Details',
        'is_need_light_box' : True,
    }

    return render(request, 'admin_panel/product/product_details.html', context)


@login_required
@role_required(['superadmin'])
def create_product(request):
    """
    create operation of product
    :param request:
    :return:
    """
    # check pk for getting instance    
    ProductMoreImageFormset = formset_factory(ProductImageForm, extra=2)
    ProductVariantFormset = formset_factory(ProductVariantForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        form = ProductForm(request.POST,files=request.FILES)
        # image_form = ProductImageForm(request.POST)
        product_more_image_formset = ProductMoreImageFormset(request.POST, request.FILES, prefix='product_more_image_formset', form_kwargs={'empty_permitted': False})
        product_variation_formset = ProductVariantFormset(request.POST, prefix='product_variation_formset', form_kwargs={'empty_permitted': False})
        
        # varient_form = ProductVariantForm(request.POST)
        # files = request.FILES.getlist('image')
                    
        if form.is_valid() and product_variation_formset.is_valid():
            # location = request.POST.getlist('delivery_locations')
            meta_keyword = request.POST.getlist('meta_keywords')
            
            #create product
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Product)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            product_data = data
            
            instance = Product.objects.get(pk=data.pk)
            # for l in location:
            #     instance.delivery_locations.add(l)
            #     instance.save()
            
            for m in meta_keyword:
                instance.meta_keywords.add(m)
                instance.save()
            
            #create multiple images
            if product_more_image_formset.is_valid():
                for form in product_more_image_formset:
                    i_data = form.save(commit=False)
                    i_data.auto_id = get_auto_id(ProductImage)
                    i_data.creator = request.user
                    i_data.date_updated = datetime.datetime.today()
                    i_data.updater = request.user
                    i_data.product = product_data
                    i_data.save()
            
            if product_variation_formset.is_valid():
                for form in product_variation_formset:
                    is_default = form.cleaned_data['is_default']
                    print(is_default)
                    
                    
                    v_data = form.save(commit=False)
                    v_data.auto_id = get_auto_id(ProductVariant)
                    v_data.creator = request.user
                    v_data.date_updated = datetime.datetime.today()
                    v_data.updater = request.user
                    v_data.product = product_data
                    v_data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Product created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:product_list')
            }
    
        else:
            message = generate_form_errors(form,product_more_image_formset,product_variation_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = ProductForm()
        image_form = ProductImageForm()
        product_more_image_formset = ProductMoreImageFormset(prefix='product_more_image_formset')
        product_variation_formset = ProductVariantFormset(prefix='product_variation_formset')

        context = {
            'form': form,
            'image_form': image_form,
            'product_more_image_formset': product_more_image_formset,
            'product_variation_formset': product_variation_formset,
            'page_name' : 'Create Product',
            'page_title' : 'Create Product',
            'is_need_select2' : True,
            'url' : reverse('product:create_product'),
        }

        return render(request, 'admin_panel/create/create_product.html',context)


@login_required
@role_required(['superadmin'])
def edit_product(request,pk):
    """
    edit operation of product
    :param request:
    :param pk:
    :return:
    """
    product_instance = get_object_or_404(Product, pk=pk)
    pro_variant_instance = ProductVariant.objects.filter(product=product_instance,is_deleted=False)
    pro_more_image_instance = ProductImage.objects.filter(product=product_instance,is_deleted=False)
    
    if ProductImage.objects.filter(product=product_instance).exists():
        m_extra = 0
    else:
        m_extra = 1 
        
    if ProductVariant.objects.filter(product=product_instance).exists():
        v_extra = 0
    else:
        v_extra = 1 

    ProductVariantFormset = inlineformset_factory(
        Product,
        ProductVariant,
        extra=v_extra,
        form=ProductVariantForm,
    )
    
    ProductMoreImageFormset = inlineformset_factory(
        Product,
        ProductImage,
        extra=m_extra,
        form=ProductImageForm,
    )
        
    message = ''
    
    if request.method == 'POST':
        form = ProductForm(request.POST,files=request.FILES,instance=product_instance)
        # image_form = ProductImageForm(request.POST,instance=pro_more_image_instance)
        product_more_image_formset = ProductMoreImageFormset(request.POST,request.FILES,instance=product_instance, prefix='product_more_image_formset', form_kwargs={'empty_permitted': False})            
        product_variation_formset = ProductVariantFormset(request.POST,instance=product_instance, prefix='product_variation_formset', form_kwargs={'empty_permitted': False})            
        
        if form.is_valid() and product_variation_formset.is_valid():
            location = request.POST.getlist('delivery_locations')
            meta_keyword = request.POST.getlist('meta_keywords')
            
            #create product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            product_data = data
            
            instance = Product.objects.get(pk=data.pk)
            for l in location:
                instance.delivery_locations.add(l)
                instance.save()
            
            for m in meta_keyword:
                instance.meta_keywords.add(m)
                instance.save()
            
            #create multiple images
            if product_more_image_formset.is_valid():
                for form in product_more_image_formset:
                    if form not in product_more_image_formset.deleted_forms:
                        print(product_more_image_formset)
                        i_data = form.save(commit=False)
                        i_data.date_updated = datetime.datetime.today()
                        i_data.updater = request.user
                        if not i_data.auto_id :
                            i_data.auto_id = get_auto_id(ProductImage)
                            i_data.creator = request.user

                        i_data.save()

                for f in product_more_image_formset.deleted_forms:
                    f.instance.delete()
                print("images 2", product_more_image_formset.deleted_forms)

            else:
                print("errorr==>>", product_more_image_formset.errors)
            
            if product_variation_formset.is_valid():
                for form in product_variation_formset:
                    if form not in product_variation_formset.deleted_forms:
                        v_data = form.save(commit=False)
                        v_data.date_updated = datetime.datetime.today()
                        v_data.updater = request.user
                        v_data.save()

                for f in product_variation_formset.deleted_forms:
                    f.instance.delete()
                    
                response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Product Updated Successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:product_list'),
                "return" : True,
            }

            else:
                print(product_variation_formset.errors)
                print("error in update variant section...")
                
                response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Product Updated successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:product_list'),
                "return" : False,
            }
    
        else:
            message = generate_form_errors(product_variation_formset,formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                        
    else:

        form = ProductForm(instance=product_instance)
        # image_form = ProductImageForm(instance=pro_more_image_instance)
        product_more_image_formset = ProductMoreImageFormset(prefix='product_more_image_formset', instance=product_instance)
        product_variation_formset = ProductVariantFormset(prefix='product_variation_formset', instance=product_instance)
        

        context = {
            'form': form,
            'product_more_image_formset': product_more_image_formset,
            'product_variation_formset': product_variation_formset,
            'message': message,
            'pro_instance': product_instance,
            'pro_variant_instance': pro_variant_instance,
            'pro_more_image_instance': pro_more_image_instance,
            'page_name' : 'edit product'
            
        }

        return render(request, 'admin_panel/create/create_product.html', context)


@login_required
@role_required(['superadmin'])
def delete_product(request, pk):
    """
    product deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Product.objects.filter(pk=pk).update(is_deleted=True)
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:product_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def delete_product_varient(request, pk):
    """
    product deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    data = ProductVariant.objects.get(pk=pk)
    data.is_deleted = True
    data.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:product_details', kwargs={'pk': data.product.pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

#**************************** size chart *************************#


@login_required
@role_required(['superadmin'])
def size_chart(request):
    """
    product size chart listing
    :param request:
    :return: product size chart view
    """
    instances = ProductSizeChart.objects.filter(is_deleted=False)
    image_instances = SizeMeasurementChart.objects.filter()

    context = {
        'instances': instances,
        'image_instances': image_instances,
        
        'page_name' : 'Size Chart',
        'page_title' : 'Size Chart',
        'PRODUCT_TYPE_CHOICE' : [i[0] for i in PRODUCT_TYPE_CHOICE]
        
    }

    return render(request, 'admin_panel/product/product_size_chart.html', context)


@login_required
@role_required(['superadmin'])
def check_product_type(request):
    """
    product type checking
    :param request:
    :return: product size chart create
    """
    type = request.GET.get("type")
    print(type)
    
    product_type = Messurment.objects.filter(type=type, is_deleted=False)
    
    if product_type:
        
        return product_type
    else:
        print("elsssssssssssssssss")
    
    data = serialize("json",product_type)
    
    response_data = {
        "status": "6000",
        "product_type" : data,
        }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')



@login_required
@role_required(['superadmin'])
def create_size_chart(request):
    """
    create operation of product
    :param request:
    :return:
    """
    # check pk for getting instance    
    ProductSizeChartFormset = formset_factory(SizeChartForm, extra=2)
    
    if request.method == 'POST':
        type = request.POST.get("product_type")
        
        image_form = SizeChartImageForm(request.POST,files=request.FILES)
        size_chart_formset = ProductSizeChartFormset(request.POST, prefix='size_chart_formset', form_kwargs={'empty_permitted': False})
                    
        if size_chart_formset.is_valid() and image_form.is_valid() :            
            #create size chart
            for c_form in size_chart_formset:
                c_data = c_form.save(commit=False)
                c_data.Product_type = type
                c_data.save()
            
            #create size chart image
            ci_data = image_form.save(commit=False)
            ci_data.product_type = type
            ci_data.save()
            
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Size Chart created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:size_chart')
            }
    
        else:                
            message = generate_form_errors(size_chart_formset,formset=True)
            
            
            response_data = {
                "status": "false",
                "title": "Form Validation Error",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        size_chart_formset = ProductSizeChartFormset(prefix='size_chart_formset')
        image_form = SizeChartImageForm(request.POST,files=request.FILES)
        
        product_type_dict = []
        # print(product_type)
        for type in product_type:
            
            product_type_dict.append({
                "key":type[0],
                "value": type[1]
                })
            
        
        # print("+====>>> ",product_type_dict)
        context = {
            'size_chart_formset': size_chart_formset,
            'image_form' : image_form,
            'product_type' :  product_type_dict,
            'page_name' : 'Create Size Chart',
            'page_title' : 'Create Size Chart',
            'is_need_select2' : True,
            'url' : reverse('product:create_size_chart'),
        }

        return render(request, 'admin_panel/create/create_size_chart.html',context)
    

@login_required
@role_required(['superadmin'])
def edit_sizechart(request,pk):
    """
    edit operation of sizechart
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(ProductSizeChart, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = SizeChartForm(request.POST,instance=instance)
        
        if form.is_valid():
            
            #update meta keyword
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Sizechart Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:size_chart')
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
        
        form = SizeChartForm(instance=instance)

        context = {
            'form': form,
            'type' : instance.Product_type,
            'page_name' : 'Update size chart',
            'page_title' : 'Update size chart',
            'url' : reverse('product:size_chart'),
        }

        return render(request, 'admin_panel/product/update_sizechart.html',context)

    
    
@login_required
@role_required(['superadmin'])
def delete_size(request,pk):
    """
    size deletion, it only mark as is deleted field to true
    it delete each sizes from size chart
    :param request:
    :param pk:
    :return:
    """
    data = ProductSizeChart.objects.get(pk=pk)
    data.is_deleted = True
    data.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Size Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:size_chart')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def delete_size_category(request,c_pk):
    """
    size deletion, it only mark as is deleted field to true
    here deleting size by category
    c_pk (category pk)
    :param request:
    :param c_pk:
    :return:
    """
    ProductSizeChart.objects.filter(product_category__pk=c_pk).update(is_deleted=True)
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Category Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:size_chart')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def edit_sizechart_image(request,pk):
    """
    edit operation of sizechart image
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(SizeMeasurementChart, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = SizeChartImageForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            
            #update meta keyword
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Sizechart Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:size_chart')
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
        
        form = SizeChartImageForm(files=request.FILES,instance=instance)

        context = {
            'form': form,
            'type' : instance.product_type,
            'page_name' : 'Update size Image chart',
            'page_title' : 'Update size Image chart',
            'url' : reverse('product:size_chart'),
        }

        return render(request, 'admin_panel/product/update_sizechart.html',context)

    
    
@login_required
@role_required(['superadmin'])
def delete_size_image(request,pk):
    """
    size Image deletion,
    it delete each sizes from size chart
    :param request:
    :param pk:
    :return:
    """
    data = SizeMeasurementChart.objects.filter(pk=pk).delete()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Size Image Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:size_chart')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')




@login_required
@role_required(['superadmin'])
def product_category(request):
    instances = ProductCategory.objects.filter(is_deleted=False).order_by("-id")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) 
        )
        title = "Product Category - %s" % query
        filter_data['q'] = query
    

    context = {
        'instances': instances,
        'page_name' : 'Product Category',
        'page_title' : 'Product Category',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/product/product_category.html', context)


@login_required
@role_required(['superadmin'])
def create_product_category(request):
    
    if request.method == 'POST':
        
        form = ProductCategoryForm(request.POST)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(ProductCategory)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Product Category Created Successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:product_category')
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
        
        form = ProductCategoryForm()

        context = {
            'form': form,
            'page_name' : 'Create Product Category',
            'page_title' : 'Create Product Category',
            'url' : reverse('product:create_product_category'),
        }

        return render(request, 'admin_panel/product/create_category.html',context)

    
@login_required
@role_required(['superadmin'])
def edit_product_category(request,pk):
    
    instance = get_object_or_404(ProductCategory, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST,instance=instance)
        
        if form.is_valid():
            
            #update meta keyword
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Product Category Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:product_category')
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
        
        form = ProductCategoryForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Create Product Category',
            'page_title' : 'Create Product Category',
            'is_need_select2' : True,
            'url' : reverse('product:product_category'),
        }

        return render(request, 'admin_panel/product/create_category.html',context)


@login_required
@role_required(['superadmin'])
def delete_product_category(request, pk):
    
    ProductCategory.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Category Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:product_category')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')



# @login_required
# @role_required(['superadmin'])
# def product_type(request):
#     instances = ProductType.objects.filter(is_deleted=False)
    
#     filter_data = {}
#     query = request.GET.get("q")
    
#     if query:

#         instances = instances.filter(
#             Q(auto_id__icontains=query) |
#             Q(name__icontains=query) 
#         )
#         title = "Product type - %s" % query
#         filter_data['q'] = query
    

#     context = {
#         'instances': instances,
#         'page_name' : 'Product Type',
#         'page_title' : 'Product Type',
#         'filter_data' :filter_data,
#     }
#     return render(request, 'admin_panel/product/product_type.html', context)


# @login_required
# @role_required(['superadmin'])
# def create_product_type(request):
    
#     if request.method == 'POST':
        
#         form = ProductTypeForm(request.POST)
            
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.auto_id = get_auto_id(ProductType)
#             data.creator = request.user
#             data.date_updated = datetime.datetime.today()
#             data.updater = request.user
#             data.save()

#             response_data = {
#                 "status": "true",
#                 "title": "Successfully Created",
#                 "message": "Product Type Created Successfully.",
#                 'redirect': 'true',
#                 "redirect_url": reverse('product:product_type')
#             }
    
#         else:
#             message =generate_form_errors(form , formset=False)
#             response_data = {
#                 "status": "false",
#                 "title": "Failed",
#                 "message": message,
#             }
#         return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
#     else:
        
#         form = ProductTypeForm()

#         context = {
#             'form': form,
#             'page_name' : 'Create Product Type',
#             'page_title' : 'Create Product Type',
#             'url' : reverse('product:create_product_type'),
#         }
#         return render(request, 'admin_panel/product/create_product_type.html',context)

    
# @login_required
# @role_required(['superadmin'])
# def edit_product_type(request,pk):
    
#     instance = get_object_or_404(ProductType, pk=pk)
        
#     message = ''
#     if request.method == 'POST':
#         form = ProductTypeForm(request.POST,instance=instance)
        
#         if form.is_valid():
            
#             #update meta keyword
#             data = form.save(commit=False)
#             data.date_updated = datetime.datetime.today()
#             data.updater = request.user
#             data.save()
                    
#             response_data = {
#                 "status": "true",
#                 "title": "Successfully Created",
#                 "message": "Product Type Updated successfully.",
#                 'redirect': 'true',
#                 "redirect_url": reverse('product:product_type')
#             }
    
#         else:
#             message = generate_form_errors(form ,formset=False)
            
#             response_data = {
#                 "status": "false",
#                 "title": "Failed",
#                 "message": message
#             }
#         return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
#     else:
        
#         form = ProductTypeForm(instance=instance)

#         context = {
#             'form': form,
#             'page_name' : 'Edit Product Type',
#             'page_title' : 'Edit Product Type',
#             'is_need_select2' : True,
#             'url' : reverse('product:product_type'),
#         }
#         return render(request, 'admin_panel/product/create_product_type.html.html',context)


# @login_required
# @role_required(['superadmin'])
# def delete_product_type(request, pk):
    
#     ProductType.objects.filter(pk=pk).update(is_deleted=True)

#     response_data = {
#         "status": "true",
#         "title": "Successfully Deleted",
#         "message": "Product Type Successfully Deleted.",
#         "redirect": "true",
#         "redirect_url": reverse('product:product_type')
#     }
#     return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def update_locations(request, pk):
    instance = get_object_or_404(Product.objects.filter(pk=pk, is_deleted=False))

    if request.method == 'POST':
        locations = request.POST.getlist('location')
        instance.delivery_locations.clear()

        for item in locations:
            p = Location.objects.get(pk=item)
            instance.delivery_locations.add(p)

        response_data = {
            "status": "true",
            "stable": "false",
            "title": "Successfully Updated",
            "message": "Locations Updated successfully.",
            "redirect": "true",
            "redirect_url": reverse('product:product_details', kwargs={'pk': instance.pk})
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        array_p = list(instance.delivery_locations.all().values_list('pk', flat=True))
        states = State.objects.all()
            
        context = {
            "is_edit": True,
            "array_p": array_p,
            "instance": instance,
            "states" : states,
            'page_name': 'Product Delivery Location',
            'app_name': 'Products',
            'page_title': 'Product Delivery Location',
            "url": reverse('product:update_locations', kwargs={'pk': pk}),
        }
        return render(request, 'admin_panel/product/set_locations.html', context)


