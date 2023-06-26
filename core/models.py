from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from core.managers import ActiveCategoryCustomManager, AvailabledProducts


def min_value_validator(value):
    if value < 0:
        raise ValidationError(
            '%(value)s must be greater than or equal to 0',
            params={'value': value},
        )


class BaseModel(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return 'Base Model'


class Category(BaseModel):
    StockOut = '0'
    StockIn = '1'

    STATUSES = (
        (StockOut, 'Stack-out'),
        (StockIn, 'Stack-in')
    )

    name = models.CharField(
        max_length=255,
        verbose_name='Category name'
    )
    slug = models.SlugField(
        max_length=255,
        null=True, blank=True
    )
    icon = models.TextField()
    description = models.TextField(
        verbose_name='Category description'
    )
    status = models.CharField(
        verbose_name='Category status',
        max_length=10,
        choices=STATUSES,
        default=STATUSES[0][0]
    )

    objects = models.Manager()
    objects_in_stock = ActiveCategoryCustomManager()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)


class ProductSeller(BaseModel):
    seller_name = models.CharField(
        max_length=15,
        verbose_name='Product Seller'
    )

    class Meta:
        verbose_name = 'ProductSeller'
        verbose_name_plural = 'ProductSellers'
        db_table = 'ProductSeller'

    def __str__(self):
        return self.seller_name


class Product(BaseModel):
    StockOut = '0'
    StockIn = '1'

    STATUSES = (
        (StockOut, 'Stack-out'),
        (StockIn, 'Stack-in')
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='Category'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Product name'
    )
    slug = models.SlugField(
        max_length=255,
        null=True, blank=True
    )
    description = models.TextField(
        verbose_name='Product description'
    )
    seller = models.ManyToManyField(
        to=ProductSeller
    )
    price = models.DecimalField(
        verbose_name='Product price',
        max_digits=10,
        decimal_places=2,
        validators=[min_value_validator]
    )
    discount = models.DecimalField(
        verbose_name='Product discount',
        max_digits=5,
        decimal_places=2,
        validators=[min_value_validator]
    )
    status = models.CharField(
        verbose_name='Product status',
        max_length=10,
        choices=STATUSES,
        default=STATUSES[0][0]
    )

    objects = models.Manager()
    objects_availabled = AvailabledProducts()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'Products'

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(BaseModel):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        verbose_name='Product Image',
        upload_to='products/%Y/%m/%d'
    )

    class Meta:
        verbose_name = 'ProductImage'
        verbose_name_plural = 'ProductImages'
        db_table = 'ProductImage'


class Stock(BaseModel):
    StockOut = '0'
    StockIn = '1'

    STATUSES = (
        (StockOut, 'Stack-out'),
        (StockIn, 'Stack-in')
    )

    product = models.OneToOneField(
        to=Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name='Product Quantity',
        default=0,
        validators=[min_value_validator]
    )
    type = models.CharField(
        max_length=20,
        choices=STATUSES,
        default=STATUSES[0][0]
    )

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'
        db_table = 'Stock'
        ordering = ['-date_created']

    def save(self, commit=True, *args, **kwargs):
        product = Product.objects.filter(id=self.product.pk)
        if product.exists():
            if not self.pk:
                if self.quantity > 0:
                    self.type = self.StockIn
                    product = Product.objects.get(id=product.first().pk)
                    product.status = '1'
                    product.save()

                else:
                    self.type = self.StockOut
                    product = Product.objects.get(id=product.first().pk)
                    product.status = '0'
                    product.save()

                super(Stock, self).save(*args, **kwargs)
                stock = Stock.objects.get(id=self.pk)
                if commit:
                    History.objects.create(
                        stock=stock, quantity=self.quantity, type=self.type)

            else:
                stock = Stock.objects.get(id=self.pk)
                if self.quantity > stock.quantity:
                    if commit:
                        History.objects.create(
                            stock=stock, quantity=self.quantity - stock.quantity, type='1')

                elif self.quantity == stock.quantity:
                    pass

                else:
                    if commit:
                        History.objects.create(
                            stock=stock, quantity=stock.quantity - self.quantity, type='0')

                super(Stock, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name


class History(BaseModel):
    STOCK_IN = '1'
    STOCK_OUT = '0'

    TYPES = (
        (STOCK_IN, 'stock-in'),
        (STOCK_OUT, 'stock-out')
    )

    stock = models.ForeignKey(
        to=Stock,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name='Quantity'
    )
    type = models.CharField(
        verbose_name='Type',
        choices=TYPES,
        max_length=12
    )

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'Histories'
        db_table = 'History'
        ordering = ['date_created']

    def save(self, *args, **kwargs):
        if self.pk:
            history = History.objects.get(id=self.pk)
            if history.quantity < self.quantity:
                self.stock.quantity += self.quantity - history.quantity
                self.stock.save(commit=True)

            else:
                self.stock.quantity -= history.quantity - self.quantity
                self.stock.save(commit=False)

        elif self.quantity == 0:
            pass
        super(History, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.type == self.STOCK_IN:
            if self.stock.quantity - self.quantity >= 0:
                self.stock.quantity -= self.quantity
                self.stock.save(commit=False)
            else:
                raise ValueError("Haven't got enought product!")
        else:
            if self.stock.quantity + self.quantity >= 0:
                self.stock.quantity += self.quantity
                self.stock.save(commit=False)

            else:
                raise ValueError("Haven't got enought product!")

        super(History, self).delete(*args, **kwargs)

    def __str__(self):
        return self.stock.product.name
