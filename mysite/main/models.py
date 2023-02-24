from django.db import models




class MAIN_INDICES_TICKERS(models.Model):
    symbol = models.CharField(max_length=10, null=False,unique=True)
    name = models.CharField(max_length = 100, null=True, blank=True)

    def __str__(self):
        return self.symbol

class MAIN_INDICES(models.Model):
    date = models.DateField()
    symbol = models.CharField(max_length=10, null=False)
    close = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    high = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    low = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    open = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    volume = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    def __str__(self):
        return self.symbol


class GPW(models.Model):
    date = models.DateField()
    symbol = models.CharField(max_length=10, null=False)
    close = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    high = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    low = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    open = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    volume = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return self.symbol
class GPW_TICKERS(models.Model):
    symbol = models.CharField(max_length=10, null=False, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    symbol_stooq = models.CharField(max_length=10, null=True,unique=True)
    def __str__(self):
        return self.name

class GPW_OPTIONS(models.Model):
    date = models.DateField()
    symbol = models.CharField(max_length=10, null=False)
    close = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    high = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    low = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    open = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    volume = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    def __str__(self):
        return self.symbol
