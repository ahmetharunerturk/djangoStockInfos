# views.py

from django.shortcuts import render
import yfinance as yf

def get_stock_info(request):
    if request.method == 'POST':
        ticker_symbol = request.POST.get('ticker_symbol', '').upper()

        if not ticker_symbol:
            error_message = "Lütfen geçerli bir hisse senedi simgesi girin."
            return render(request, 'error.html', {'error_message': error_message})

        try:
            stock_info = yf.Ticker(ticker_symbol)
            info = stock_info.info

            if not info:
                error_message = f"{ticker_symbol} simgesine sahip bir hisse senedi bulunamadı."
                return render(request, 'error.html', {'error_message': error_message})

            # Son temettü miktarını al
            dividends_data = stock_info.dividends.reset_index()
            if not dividends_data.empty:
                last_dividend = dividends_data.iloc[-1]['Dividends']
            else:
                last_dividend = None

            stock_name = info.get('longName', '')
            stock_symbol = info.get('symbol', '')
            stock_country = info.get('country', '')
            stock_industry = info.get('industry', '')

            return render(request, 'stock_info.html', {
                'stock_name': stock_name,
                'stock_symbol': stock_symbol,
                'stock_country': stock_country,
                'stock_industry': stock_industry,
                'last_dividend': last_dividend,
                'info': info,
            })

        except Exception as e:
            error_message = f"Hisse senedi bilgileri alınırken bir hata oluştu: {e}"
            return render(request, 'error.html', {'error_message': error_message})

    return render(request, 'stock_form.html')
