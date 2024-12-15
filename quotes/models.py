from django.db import models

class Stock(models.Model):
	symbol = models.CharField(max_length=10)
	dividend_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	date = models.DateField(null=True, blank=True)
	last_closing_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	annual_dividend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	yield_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

	def __str__(self):
		return self.symbol