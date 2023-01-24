from django import template
from django.db.models import Sum
from product.models import Product, ProductSizeChart, ProductVariant
from offers.models import Offers

register = template.Library()

@register.simple_tag
def get_product_varient_in_product(pk):
    if ProductVariant.objects.filter(product__pk=pk,is_deleted=False).exists():
        product_varients = ProductVariant.objects.filter(product__pk=pk,is_deleted=False)
        total_stock = product_varients.aggregate(total=Sum('stock')).get('total')
        available_sizes = product_varients.filter(stock__gte=1).values('size')
        return {
            'total_stock' : total_stock,
            'available_sizes' : available_sizes,
        }
    
@register.filter
def load_products(typ,products):
    
    return products.filter(Product_type=typ)


@register.simple_tag
def get_offer_in_product(p_pk):
    if Offers.objects.filter(product__pk=p_pk,is_deleted=False).exists():
        # offer = Offers.objects.filter(product__pk=p_pk,is_deleted=False)
        return True
    
# checking product price and if have any offer price in this product
# @register.simple_tag
# def get_product_price(p_pk):
#     if Offers.objects.filter(product__pk=p_pk,is_deleted=False).exists():
#         offer_percentage = Offers.objects.filter(product__pk=p_pk,is_deleted=False).first()
#         price = Product.objects.get(pk=p_pk,is_deleted=False)
#         offer_price = price.price - (price.price * offer_percentage.offer_price / 100)
#         print(offer_price,"offe price")
        
#         return {
#             'price' : float(offer_price),
#             'actual_rate' : float(price.price),
#             'offer_percentage' : float(offer_percentage.offer_price),
#             'is_offer' : True,
#             }
#     else:
#         product_price = Product.objects.get(pk=p_pk,is_deleted=False)
        
#         return product_price.price
    
    
# @register.simple_tag
# def get_price_in_cart(varient_pk):
#     pro_varient = ProductVariant.objects.filter(=sub_pk,is_deleted=False).count()
#     lesson_instances_count = Lesson.objects.filter(subject__pk=sub_pk,is_deleted=False).count()
#     latest_added_topic = Topic.objects.filter(lesson__subject__pk=sub_pk,is_deleted=False).first()
#     return {
#         'lesson_instances_count' : lesson_instances_count,
#         'topic_instances_count' : topic_instances_count,
#         'latest_added_topic' : latest_added_topic,
#     }
    
# # @register.simple_tag
# # def get_topic_percentage(student_pk,sub_pk):
# #     profile_instance = Profile.objects.get(pk=student_pk)
# #     total_topic = Topic.objects.filter(lesson__subject__grade__pk=profile_instance.grade_batch.grade.pk,is_deleted=False).count()
# #     encrolled_topic = StudentTopic.objects.filter(topic__lesson__subject__pk=sub_pk,is_deleted=False,is_completed=True).count()
    
# #     # perscentage = total_topic/encrolled_topic
# #     perscentage = encrolled_topic/total_topic*100
    
# #     return perscentage