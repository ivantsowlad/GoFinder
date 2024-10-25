from django.db import models


class Search(models.Model):
    search = models.CharField('Hledání', max_length=50)

    def __str__(self):
        return self.search
