import time
from src.config import Config
from src.data.fetcher import DataFetcher
from src.data.database import Database
from src.trading.strategy import TradingStrategy
from src.trading.executor import OrderExecutor
from src.trading.risk import RiskManager
from src.monitor.performance import PerformanceMonitor
from src.utils.logger import Logger

class CryptoQuantTrading:
    def __init__(self, api_key: str, api_secret: str):
        self.config = Config(api_key, api_secret)
        self.logger = Logger(__name__, "trading.log")
        self.data_fetcher = DataFetcher(self.config)
        self.database = Database(self.config)
        self.strategy = TradingStrategy(self.config)
        self.executor = OrderExecutor(self.config)
        self.risk_manager = RiskManager(self.config)
        self.performance_monitor = PerformanceMonitor(self.config)
        
    def run(self):
        """运行交易策略"""
        while True:
            try:
                # 获取并保存市场数据
                df = self.data_fetcher.get_historical_data()
                self.database.save_klines(df, self.config.trading.symbol)
                
                # 计算信号
                df = self.strategy.calculate_signals(df)
                
                # 获取最新信号
                current_signal = df['signal'].iloc[-1]
                current_price = df['close'].iloc[-1]
                
                # 风险检查和交易执行
                if current_signal == 1 and self.executor.position != 'LONG':
                    if self.risk_manager.check_order(
                        self.config.trading.symbol,
                        'BUY',
                        self.config.trading.quantity,
                        current_price
                    ):
                        order = self.executor.place_order('BUY')
                        if order:
                            self.logger.logger.info(f"执行买入: {order}")
                            self.risk_manager.update_position(
                                self.config.trading.symbol,
                                self.config.trading.quantity,
                                current_price
                            )
                
                # 更新性能指标
                self.performance_monitor.log_metrics()
                
                time.sleep(60)
                
            except Exception as e:
                self.logger.logger.error(f"策略运行错误: {e}")
                time.sleep(60)

