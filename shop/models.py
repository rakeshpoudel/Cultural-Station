import datetime
import uuid
from datetime import datetime as dt

from django.db import models


# --------------------------------
from django.urls import reverse


class ProductSize(models.Model):
    SIZE_CATEGORY = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('3XL', '3XL'),
    )

    size = models.CharField(max_length=50, choices=SIZE_CATEGORY, default=0)

    def __str__(self):
        return self.size

    # def get_products(self):
    #     return Product.objects.filter(categories__name=self.name)


class Dresse(models.Model):
    GENDER = (
        ('----', '----'),
        ('men', 'men'),
        ('women', 'women')
    )

    dress = models.CharField(max_length=200, default='', unique=True, help_text='write in lowercase')
    gender = models.CharField(max_length=50, choices=GENDER, default='')

    def __str__(self):
        return self.dress


class Caste(models.Model):
    caste = models.CharField(max_length=200, default='', unique=True, help_text='write in lowercase')

    def __str__(self):
        return self.caste


class DressColor(models.Model):
    color = models.CharField(max_length=200, default='', unique=True, help_text='write in lowercase')

    def __str__(self):
        return self.color


class ProductDesigner(models.Model):
    designer = models.CharField(max_length=200, default='', unique=True, help_text='write in lowercase')

    def __str__(self):
        return self.designer


class Product(models.Model):
    PERSON_CATEGORY = (
        ('men', 'men'),
        ('women', 'women')
    )
    ELEMENT_CATEGORY = (
        ('dress', 'dress'),
    )

    name = models.CharField(max_length=50)
    slug = models.SlugField(null=False, default='', unique=True, help_text='')
    dress_type = models.ForeignKey(Dresse, related_name='dress_type', to_field='dress', on_delete=models.CASCADE, default="", blank=True, null=True, help_text='Choose the dress_type for the product')
    designer = models.ForeignKey(ProductDesigner, related_name='product_designer', to_field='designer', on_delete=models.CASCADE,
                                   default="", blank=True, null=True, help_text='Choose the designer for the product, if any else leave blank')
    caste_category = models.ForeignKey(Caste, related_name='Caste', to_field='caste', on_delete=models.CASCADE, default="", blank=True, null=True, help_text='Choose the caste type for product, if any else leave blank')
    person_category = models.CharField(max_length=50, choices=PERSON_CATEGORY, default="", help_text='Choose the '
                                                                                                     'gender '
                                                                                                     'the product '
                                                                                                     'belongs to')
    element_category = models.CharField(max_length=50, choices=ELEMENT_CATEGORY, default="",
                                        help_text='Choose the Element')
    size = models.ManyToManyField(ProductSize, help_text='Choose sizes available for the product')
    dress_color = models.ForeignKey(DressColor, related_name='dress_color', to_field='color', on_delete=models.CASCADE, default="", blank=True,
                                       null=True,
                                       help_text='Choose the color or add the color of the product, leave blank if the dress is traditional')
    rent_price = models.IntegerField(default=0)
    refund_amount = models.IntegerField(default=0)
    stock_size_s = models.IntegerField(default=0, help_text='Enter stock of product with size "S"')
    stock_size_m = models.IntegerField(default=0, help_text='Enter stock of product with size "M"')
    stock_size_l = models.IntegerField(default=0, help_text='Enter stock of product with size "L"')
    stock_size_xl = models.IntegerField(default=0, help_text='Enter stock of product with size "XL"')
    stock_size_xxl = models.IntegerField(default=0, help_text='Enter stock of product with size "XXL"')
    stock_size_3xl = models.IntegerField(default=0, help_text='Enter stock of product with size "3XL"')
    # product_details = models.CharField(max_length=500, default="", help_text='Enter products details like available '
    #                                                                          'color, size, '
    #                                                                          'ect')
    pub_date = models.DateField()
    main_image = models.ImageField(upload_to='img/prod_img', default="",
                                   help_text='Choose image to display as main display '
                                             'image '
                                             'of product')
    sub_image1 = models.ImageField(upload_to='img/prod_img', default="", help_text='Choose other image for the product')
    sub_image2 = models.ImageField(upload_to='img/prod_img', default="", help_text='Choose other image for the product')

    # size = models.ForeignKey(ProductSize, related_name='ProductSIze', on_delete=models.CASCADE, default="")

    def get_absolute_url(self):
        return reverse('product_view', kwargs={'slug': self.slug})


class UserDetail(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=100, default='')
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=50, default='')
    contact = models.IntegerField(default='')
    shipping_city = models.CharField(max_length=50, default='')
    shipping_area = models.CharField(max_length=50, default='')
    shipping_address = models.CharField(max_length=200, default='')
    verification = models.CharField(max_length=100, default="")


class Cart(models.Model):
    slug = models.SlugField(null=False, default='', help_text='')
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100, default='')
    caste_type = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=100, default='')
    designer = models.CharField(max_length=100, default='')
    dress_type = models.CharField(max_length=100, default='')
    renting_way = models.CharField(max_length=20)
    product_size = models.CharField(max_length=20)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    refund = models.IntegerField(default=0)
    renting_days = models.CharField(max_length=50)
    delivery_date = models.CharField(max_length=50)
    returning_date = models.CharField(max_length=50)
    image = models.CharField(max_length=100, default='')
    added_datetime = models.DateTimeField(default=dt.now, blank=True)


class Wishlist(models.Model):
    user_name = models.CharField(max_length=200)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100, default='')
    caste_type = models.CharField(max_length=100, default='')
    designer = models.CharField(max_length=100, default='')
    dress_type = models.CharField(max_length=100, default='')
    renting_way = models.CharField(max_length=20)
    product_size = models.CharField(max_length=20)
    image = models.CharField(max_length=100, default='')


class Rating(models.Model):
    user_name = models.CharField(max_length=100, default='')
    product_id = models.IntegerField()
    ratings = models.IntegerField()
    review = models.CharField(max_length=2038, default='', blank=True)
    posted_date = models.DateTimeField(default=dt.now, blank=True)
    check_status = models.CharField(max_length=100, default='not checked')
    image = models.ImageField(upload_to='img', null=True, default="")


class ProductQuery(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    publish_date = models.DateField(default=datetime.date.today)
    question = models.CharField(max_length=2038)
    answer = models.CharField(max_length=2038, default='')
    image = models.ImageField(upload_to='img', null=True, default="")


class ShippingCity(models.Model):
    CITY = (
        ('Bhaktapur', 'Bhaktapur'),
        ('Kathmandu Metro 10 - New Baneshwor Area', 'Kathmandu Metro 10 - New Baneshwor Area'),
        ('Kathmandu Metro 11 - Maitighar Area', 'Kathmandu Metro 11 - Maitighar Area'),
        ('Kathmandu Metro 12 - Teku Area', 'Kathmandu Metro 12 - Teku Area'),
        ('Kathmandu Metro 13 - Kalimati Area', 'Kathmandu Metro 13 - Kalimati Area'),
        ('Kathmandu Metro 14 - Kuleshwor Area', 'Kathmandu Metro 14 - Kuleshwor Area'),
        ('Kathmandu Metro 15 - Swayambhu Area', 'Kathmandu Metro 15 - Swayambhu Area'),
        ('Kathmandu Metro 16 - Nayabazar Area', 'Kathmandu Metro 16 - Nayabazar Area'),
        ('Kathmandu Metro 17 - Chhetrapati Area', 'Kathmandu Metro 17 - Chhetrapati Area'),
        ('Kathmandu Metro 18 - Raktakali Area', 'Kathmandu Metro 18 - Raktakali Area'),
        ('Kathmandu Metro 19 - Hanumandhoka Area', 'Kathmandu Metro 19 - Hanumandhoka Area'),
        ('Kathmandu Metro 1 - Naxal Area', 'Kathmandu Metro 1 - Naxal Area'),
        ('Kathmandu Metro 20 - Marutol Area', 'Kathmandu Metro 20 - Marutol Area'),
        ('Kathmandu Metro 21 - Lagantol Area', 'Kathmandu Metro 21 - Lagantol Area'),
        ('Kathmandu Metro 22 - Newroad Area', 'Kathmandu Metro 22 - Newroad Area'),
        ('Kathmandu Metro 23 - Basantapur Area', 'Kathmandu Metro 23 - Basantapur Area'),
        ('Kathmandu Metro 24 - Indrachowk Area', 'Kathmandu Metro 24 - Indrachowk Area'),
        ('Kathmandu Metro 25 - Ason Area', 'Kathmandu Metro 25 - Ason Area'),
        ('Kathmandu Metro 26 - Lainchor Area', 'Kathmandu Metro 26 - Lainchor Area'),
        ('Kathmandu Metro 27 - Bhotahiti Area', 'Kathmandu Metro 27 - Bhotahiti Area'),
        ('Kathmandu Metro 28 - Bagbazar Area', 'Kathmandu Metro 28 - Bagbazar Area'),
        ('Kathmandu Metro 28 - Kamaladi Area', 'Kathmandu Metro 28 - Kamaladi Area'),
        ('Kathmandu Metro 29 - Anamnagar Area', 'Kathmandu Metro 29 - Anamnagar Area'),
        ('Kathmandu Metro 29 - Putalisadak Area', 'Kathmandu Metro 29 - Putalisadak Area'),
        ('Kathmandu Metro 2 - Lazimpat Area', 'Kathmandu Metro 2 - Lazimpat Area'),
        ('Kathmandu Metro 30 - Maitidevi Area', 'Kathmandu Metro 30 - Maitidevi Area'),
        ('Kathmandu Metro 31 - Min Bhavan Area', 'Kathmandu Metro 31 - Min Bhavan Area'),
        ('Kathmandu Metro 32 - Koteshwor Area', 'Kathmandu Metro 32 - Koteshwor Area'),
        ('Kathmandu Metro 32 - Tinkune Area', 'Kathmandu Metro 32 - Tinkune Area'),
        ('Kathmandu Metro 3 - Baluwatar Area', 'Kathmandu Metro 3 - Baluwatar Area'),
        ('Kathmandu Metro 3 - Maharajganj Area', 'Kathmandu Metro 3 - Maharajganj Area'),
        ('Kathmandu Metro 4 - Bishalnagar Area', 'Kathmandu Metro 4 - Bishalnagar Area'),
        ('Kathmandu Metro 5 - Tangal Area', 'Kathmandu Metro 5 - Tangal Area'),
        ('Kathmandu Metro 7 - Chabahil Area', 'Kathmandu Metro 7 - Chabahil Area'),
        ('Kathmandu Metro 8 - Gausala Area', 'Kathmandu Metro 8 - Gausala Area'),
        ('Kathmandu Metro 9 - Sinamangal Area', 'Kathmandu Metro 9 - Sinamangal Area'),
        ('Kathmandu Outside Ring Road', 'Kathmandu Outside Ring Road'),
        ('Lalitpur Inside Ring Road', 'Lalitpur Inside Ring Road'),
        ('Lalitpur Outside Ring Road', 'Lalitpur Outside Ring Road')
    )

    city = models.CharField(max_length=100, choices=CITY)
    shipping_charge = models.IntegerField()


class OrderDetail(models.Model):
    ORDER_STATUS = (
        ('Rental Reserved', 'Rental Reserved'),
        ('Rental Returned', 'Rental Returned')
    )

    product_name = models.CharField(max_length=100)
    order_number = models.IntegerField()
    product_id = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    customer_id = models.IntegerField()
    customer_user_name = models.CharField(max_length=100, default='')
    customer_email = models.CharField(max_length=200, default='')
    customer_contact = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=100)
    caste_type = models.CharField(max_length=100)
    designer = models.CharField(max_length=100, default='')
    dress_type = models.CharField(max_length=100)
    renting_way = models.CharField(max_length=20)
    product_size = models.CharField(max_length=20)
    gender = models.CharField(max_length=100, default='')
    quantity = models.IntegerField()
    amount = models.IntegerField()
    refund = models.IntegerField(default=0)
    renting_days = models.CharField(max_length=50)
    delivery_date = models.CharField(max_length=50)
    returning_date = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=2038)
    shipping_charge = models.IntegerField()
    prod_image = models.ImageField(upload_to='img')
    ordered_date = models.DateTimeField(default=dt.now, blank=True)
    order_status_date = models.DateTimeField(default=dt.now, blank=True)
    payment_method = models.CharField(max_length=100, default='Cash On Delivery')
    payment_status = models.CharField(max_length=100, default='Pending')
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Rental Reserved')


class OrderSummary(models.Model):
    ORDER_STATUS = (
        ('Processing', 'Processing'),
        ('Shipping', 'Shipping'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned')
    )
    order_number = models.IntegerField()
    user_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=100, default='')
    user_full_name = models.CharField(max_length=200, default='')
    user_email = models.CharField(max_length=255, default='')
    user_contact = models.IntegerField(default=0)
    total_items = models.IntegerField(default=0)
    sub_total_amount = models.IntegerField()
    total_refund = models.IntegerField()
    shipping_charge = models.IntegerField()
    grand_total = models.IntegerField()
    delivery_date = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=2038, default='')
    payment_method = models.CharField(max_length=100, default='Cash On Delivery')
    payment_status = models.CharField(max_length=100, default='Pending')
    ordered_date = models.DateTimeField(default=dt.now, blank=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Processing',
                                    help_text='Change order status date and time when you change order status')
    order_status_date = models.DateTimeField(default=dt.now, blank=True)
    review_status = models.CharField(max_length=100, default='pending')
    check_status = models.CharField(max_length=100, default='not checked')
    

class Notification(models.Model):
    user_id = models.IntegerField()
    order_number = models.IntegerField()
    total_items = models.IntegerField()
    order_status = models.CharField(max_length=100)
    order_status_date = models.DateTimeField(default=dt.now, blank=True)


class Cancellation(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    product_link = models.CharField(max_length=2038, default='')
    product_id = models.IntegerField()
    product_category = models.CharField(max_length=100)
    product_dress_type = models.CharField(max_length=100)
    image = models.ImageField(upload_to='img')


class Event(models.Model):
    event_text = models.CharField(max_length=255)
    event_image = models.ImageField(upload_to='img/event')
    event_days = models.IntegerField()
    event_status = models.CharField(max_length=100)
    event_posted = models.DateField(auto_now_add=True)


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)
