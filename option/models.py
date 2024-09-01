from django.conf import settings
from django.db import models


class Option(models.Model):
    symbol = models.CharField(max_length=255, unique=True, help_text="The symbol of the option.", verbose_name="Symbol")
    stock_symbol = models.CharField(max_length=255, help_text="The symbol of the original stock.", verbose_name="Stock Symbol")
    option_type = models.CharField(max_length=255, help_text="Call option or put option.", verbose_name="Option Type")
    volatility = models.DecimalField(max_digits=6, decimal_places=2, help_text="The supposed annual changing percentage for the expected return.", verbose_name="Volatility")
    strike_price = models.DecimalField(max_digits=6, decimal_places=2, help_text="The strike price of this option.", verbose_name="Strike Price")
    days_to_maturity = models.IntegerField(help_text="The days before the settlement day.", verbose_name="Days to Maturity")

    class Meta:
        verbose_name = "Option information"
        verbose_name_plural = verbose_name
        ordering = ("symbol",)

    def __str__(self):
        return self.symbol