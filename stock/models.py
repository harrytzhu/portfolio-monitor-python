from django.conf import settings
from django.db import models


class Stock(models.Model):
    symbol = models.CharField(max_length=255, unique=True, help_text="The symbol of the stock.", verbose_name="Symbol")
    expected_return = models.DecimalField(max_digits=6, decimal_places=2, help_text="The expected annual gaining percentage.", verbose_name="Expected Return")
    volatility = models.DecimalField(max_digits=6, decimal_places=2, help_text="The supposed annual changing percentage for the expected return.", verbose_name="Volatility")
    initial_price = models.DecimalField(max_digits=6, decimal_places=2, help_text="The initial price of this stock.", verbose_name="Initial Price")

    class Meta:
        verbose_name = "Stock information"
        verbose_name_plural = verbose_name
        ordering = ("symbol",)

    def __str__(self):
        return self.symbol