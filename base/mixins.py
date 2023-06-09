import django_bulk

class BulkMixin:
    def create(self,obj):
        django_bulk.create(obj)

    def delete(self,obj):
        django_bulk.delete(obj)

    def update(self,obj,**kwargs):
        return django_bulk.update(obj,**kwargs)
