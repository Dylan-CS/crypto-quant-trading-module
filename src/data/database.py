from typing import Optional, List
import pandas as pd
from sqlalchemy import create_engine
from ..config import Config
from ..utils.logger import Logger

class Database:
    def __init__(self, config: Config):
        self.config = config
        self.logger = Logger(__name__, "database.log")
        self.engine = create_engine('sqlite:///data/crypto_trading.db')
        
    def save_klines(self, df: pd.DataFrame, symbol: str):
        """Save K-line data"""
        try:
            table_name = f'klines_{symbol.lower()}'
            df.to_sql(table_name, self.engine, if_exists='append')
            self.logger.logger.info(f"Successfully saved K-line data: {symbol}")
        except Exception as e:
            self.logger.logger.error(f"Failed to save K-line data: {e}")
            
    def load_klines(self, symbol: str, 
                   start_time: Optional[str] = None, 
                   end_time: Optional[str] = None) -> pd.DataFrame:
        """Load K-line data"""
        table_name = f'klines_{symbol.lower()}'
        query = f"SELECT * FROM {table_name}"
        
        if start_time:
            query += f" WHERE timestamp >= '{start_time}'"
        if end_time:
            query += f" AND timestamp <= '{end_time}'" if start_time else f" WHERE timestamp <= '{end_time}'"
            
        return pd.read_sql(query, self.engine) 