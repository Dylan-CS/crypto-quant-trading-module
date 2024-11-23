from typing import Optional
import pandas as pd
from binance.client import Client
from ..config import Config

class DataFetcher:
    def __init__(self, config: Config):
        self.config = config
        self.client = Client(config.api.api_key, config.api.api_secret)
    
    def get_historical_data(self, 
                          symbol: Optional[str] = None, 
                          interval: Optional[str] = None, 
                          limit: Optional[int] = None) -> pd.DataFrame:
        """Get historical candlestick data"""
        symbol = symbol or self.config.trading.symbol
        interval = interval or self.config.trading.interval
        limit = limit or self.config.trading.limit
        
        klines = self.client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )
        
        return self._process_klines(klines)
    
    def _process_klines(self, klines: list) -> pd.DataFrame:
        """Process candlestick data"""
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 
            'volume', 'close_time', 'quote_volume', 'trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
            
        return df 