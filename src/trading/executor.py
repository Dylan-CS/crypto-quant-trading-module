from typing import Optional, Dict, Any
from binance.client import Client
from binance.enums import *
from ..config import Config

class OrderExecutor:
    def __init__(self, config: Config):
        self.config = config
        self.client = Client(config.api.api_key, config.api.api_secret)
        self.position = None
    
    def place_order(self, side: str, quantity: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """执行订单"""
        quantity = quantity or self.config.trading.quantity
        
        try:
            order = self.client.create_order(
                symbol=self.config.trading.symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            self.position = 'LONG' if side == SIDE_BUY else 'SHORT'
            return order
        except Exception as e:
            print(f"订单执行错误: {e}")
            return None 