from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TradingConfig:
    symbol: str = 'BTCUSDT'
    quantity: float = 0.001
    short_window: int = 20
    long_window: int = 50
    interval: str = '1h'
    limit: int = 500

@dataclass
class ApiConfig:
    api_key: str
    api_secret: str

class Config:
    def __init__(self, api_key: str, api_secret: str):
        self.api = ApiConfig(api_key, api_secret)
        self.trading = TradingConfig() 