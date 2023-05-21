from django.db import models
from django.db.models import Q
from . import models as model


class ActiveCategoryCustomQuerySet(models.QuerySet):
    def all(self):
        all_active_categories = self.filter(status='1')
        return all_active_categories

    def info(self, name):
        try:
            category = self.get(name=name)
        except Exception:
            raise ValueError('Category doesn\'t exist')
        else:
            category_date_created = category.date_created
            category_date_updated = category.date_updated
            category_date_created = category.date_created
            category_date_updated = category.date_updated
            category_name = name
            category_description = category.description
            category_status = 'Stock-in' if category.status == '1' else 'Stock-out'
            category_verbose_name = self.model._meta.verbose_name
            category_verbose_name_plural = self.model._meta.verbose_name_plural
            category_DB_table_name = self.model._meta.db_table
            return f'----- {category} -----\n' \
                   f'Name - {category_name}\n' \
                   f'Description - {category_description}\n' \
                   f'Status - {category_status}\n' \
                   f'Verbose name - {category_verbose_name}\n' \
                   f'Verbose name plural - {category_verbose_name_plural}\n' \
                   f'DB table name - {category_DB_table_name}\n' \
                   f'Created - {category_date_created}\n' \
                   f'Updated - {category_date_updated}'

    def count_of_products(self):
        try:
            categories = self.all()
        except Exception:
            raise ValueError('Somthing went wrong')
        else:
            result = ''
            for category in categories:
                products = model.Product.objects.filter(category__id=category.id)
                result += f'\n----- {category} -----\n'
                iter_count = 0
                for product in products:
                    iter_count += 1
                    result += f'{iter_count} - {product}'
            if result != '':
                return result
            else:
                return 'empty'

    def get_product(self, name):
        try:
            category = self.get(name=name)
        except Exception:
            return 'Category not found'
        else:
            products = model.Product.objects.filter(category__id=category.id)
            if products:
                result = f'\n----- {category} -----\n'
                iter_count = 0
                for product in products:
                    iter_count += 1
                    product_status = 'Active' if product.status == '1' else 'Inactive'
                    result += f'{iter_count} - {product} - {product_status}'
                return result
            else:
                return 'Haven\'t got any product in this category'

    def search(self, query=None):
        bad_request = ('', None, [], {}, ())
        if query not in bad_request:
            lookups = Q(name__icontains=query) | Q(description__icontains=query)
            result = self.filter(lookups, status='1')
            if result:
                return result
            else:
                return 'Nothing found'
        return self.none()


class ActiveCategoryCustomManager(models.Manager):
    def get_queryset(self):
        return ActiveCategoryCustomQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def info(self, name):
        return self.get_queryset().info(name=name)

    def count_of_products(self):
        return self.get_queryset().count_of_products()

    def get_product(self, name):
        return self.get_queryset().get_product(name=name)

    def search(self, query):
        return self.get_queryset().search(query=query)


