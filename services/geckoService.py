import requests
import polars as pl

class GeckoService():
    def extract():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': 1
        }
        response = requests.get(url, params=params)
        elements = []
        if response.status_code == 200:
            data = response.json()
            elements = [coin for coin in data]
        else:
            print(f"Erro ao consultar a API: {response.status_code}")   
        return elements
    
    def processDate(elements):
        dataFrame = pl.DataFrame(elements)
        dataFrame = dataFrame.filter(pl.col('current_price').is_not_null())
        dataFrame = dataFrame.with_columns(pl.col('current_price').round(2))
        dataFrame = dataFrame.filter(pl.col('market_cap_rank') <= 100)
    
        dataFrame = dataFrame.with_columns(
            pl.when(pl.col('current_price') < 10)
                .then(pl.lit("Low"))
            .when((pl.col('current_price') >= 10) & (pl.col('current_price') <= 1000))
                .then(pl.lit("Medium"))
            .otherwise(pl.lit("High"))
            .alias('price_category'))
    
        processedData = dataFrame.to_dicts()
    
        return processedData