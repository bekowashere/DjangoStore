from django.db import models, transaction
from django.db.models import F, JSONField, Max, Q
from django.utils.crypto import get_random_string

class SortableModel(models.Model):
    sort_order = models.IntegerField(null=True)

    class Meta:
        abstract = True

    # Miras alınan sınıflar tarafından tanımlanması gerekiyor
    # Eğer bir sınıf bu methodu tanımlamazsa NotImplementError hatası fırlatılır.
    def get_ordering_queryset(self):
        raise NotImplementedError("Unknown ordering queryset")

    @staticmethod
    def get_max_sort_order(qs):
        # En yüksek değeri bulur
        existing_max = qs.aggregate(Max("sort_order"))
        existing_max = existing_max.get("sort_order__max")
        return existing_max

    def save(self, *args, **kwargs):
        # Model yeni kaydediliyorsa yani self.pk = None
        if self.pk is None:
            qs = self.get_ordering_queryset()
            existing_max = self.get_max_sort_order(qs)
            # Model ilk kez ekleniyorsa  0, aksi halde en yüksek sıralama değerine 1 eklenir
            self.sort_order = 0 if existing_max is None else existing_max + 1
        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.sort_order is not None:
            qs = self.get_ordering_queryset()
            # Silinen nesnenin sort_order deperinden büyük olan diğer nesneler bulunur
            # update ile bulunan nesnelerin sıralama değeri 1 azaltılır böylece boşluklar doldurulmuş olur
            qs.filter(sort_order__gt=self.sort_order).update(
                sort_order=F("sort_order") - 1
            )
        super().delete(*args, **kwargs)