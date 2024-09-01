from django.db import models
import json

class Position(models.Model):
    symbol = models.CharField(max_length=255, blank=False, default=None, help_text="The symbol of the stock.", verbose_name="Symbol")
    size = models.DecimalField(max_digits=36, default=0, decimal_places=2, help_text="The size of this stock.", verbose_name="Size")
    user_id = models.IntegerField(blank=True, null=True, help_text="The position owner.", verbose_name="User ID")

    class Meta:
        verbose_name = "Position information"
        verbose_name_plural = verbose_name
        models.Index(fields=['user_id', 'symbol', ]),
        ordering = ("user_id",)

    def __str__(self):
        return "user_id:" + str(self.user_id) + ", symbol:" + self.symbol + ", size:" + str(self.size)

class PositionPrice:
    symbol:str
    size:float
    price:float
    summary:float

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

class Statistic:
    prices:list[PositionPrice]
    summary:float

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)