from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from core.managers import ActiveCategoryCustomManager


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
    price = models.DecimalField(
        verbose_name='Product price',
        max_digits=10,
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

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'Products'

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)