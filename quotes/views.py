from django.shortcuts import render, redirect
import requests
import json
from .models import Stock
from .forms import StockForm

def home(request):
	api_key = "MY3MTVDUHQCAAPS3"
	database_tickers = Stock.objects.all()

	# Handle POST request
	if request.method == 'POST':
		# Searching for a stock symbol
		if 'stock_symbol' in request.POST:
			ticker = request.POST.get('stock_symbol')
			api_url = f"https://www.alphavantage.co/query?function=DIVIDENDS&symbol={ticker}&apikey={api_key}"
			api_url2 = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"

			try:
				api_request = requests.get(api_url)
				api_data = api_request.json()
				api_request2 = requests.get(api_url2)
				api_data2 = api_request2.json()

				time_series = api_data2.get("Time Series (Daily)", {})

				if time_series:
					latest_date = max(time_series.keys())
					latest_close_price = time_series[latest_date]["4. close"]
				else:
					latest_close_price = "Data NA"

				return render(request, 'home.html', {
					'api_data': api_data,
					'latest_close_price': latest_close_price,
					'database_tickers': database_tickers,
				})

			except requests.exceptions.RequestException as e:
				return render(request, 'home.html', {"error": "API request error"})

		# Saving a stock symbol
		elif 'symbol' in request.POST:
			symbol = request.POST.get('symbol')
			dividend_amount = request.POST.get('dividend_amount')
			payment_date = request.POST.get('payment_date')
			last_closing_price = request.POST.get('latest_close_price')

			if dividend_amount and last_closing_price:
				annual_dividend = float(dividend_amount) * 4
				yield_percentage = (float(annual_dividend) / float(last_closing_price)) * 100
			else:
				annual_dividend = None
				yield_percentage = None

			stock = Stock(
				symbol=symbol,
				dividend_amount=dividend_amount,
				date=payment_date,
				last_closing_price=last_closing_price,
				annual_dividend=annual_dividend,
				yield_percentage=yield_percentage
				)
			stock.save()
			return redirect('home')

	return render(request, 'home.html', {
		'database_tickers': database_tickers,
	})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	return redirect(home)