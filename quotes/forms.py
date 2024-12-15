from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ["symbol", "dividend_amount", "date", "last_closing_price"]