from typing import Dict
import pandas as pd
from ..config import Config

class TradingStrategy:
    def __init__(self, config: Config):
        self.config = config
    
    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算交易信号"""
        df = self._calculate_indicators(df)
        df = self._generate_signals(df)
        return df
    
    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算技术指标"""
        df['SMA_short'] = df['close'].rolling(
            window=self.config.trading.short_window).mean()
        df['SMA_long'] = df['close'].rolling(
            window=self.config.trading.long_window).mean()
        return df
    
    def _generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        df['signal'] = 0
        df.loc[df['SMA_short'] > df['SMA_long'], 'signal'] = 1
        df.loc[df['SMA_short'] < df['SMA_long'], 'signal'] = -1
        return df 