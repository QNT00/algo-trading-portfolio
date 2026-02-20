# config.py — AggressiveTradingSystem
# PUBLIC REPOSITORY VERSION
# All sensitive values (API keys, strategy parameters) are loaded from environment variables.
# Copy .env.example to .env and fill in your values before running.

import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))


class Config:
    """
    Aggressive system configuration.
    All tunable parameters are read from environment variables.
    See .env.example for the full list of required variables.
    """

    def __init__(self, mode='live'):
        self.mode = mode

        # --- Exchange ---
        self.exchange_config = {
            'exchange': 'bybit',
            'api_key': os.getenv('BYBIT_API_KEY'),
            'api_secret': os.getenv('BYBIT_API_SECRET'),
            'testnet': (mode == 'paper'),
            'use_take_profit': os.getenv('USE_TAKE_PROFIT', 'true').lower() == 'true',
        }

        # --- Trading Universe ---
        # Comma-separated in .env, e.g. SYMBOLS=ETH/USDT,SOL/USDT,BTC/USDT
        self.symbols = os.getenv('SYMBOLS', '').split(',')
        self.timeframe = os.getenv('TIMEFRAME', '5m')
        self.check_interval = int(os.getenv('CHECK_INTERVAL', 60))
        self.auto_trade = os.getenv('AUTO_TRADE', 'true').lower() == 'true'

        # --- ML / RL ---
        self.use_rl = os.getenv('USE_RL', 'true').lower() == 'true'

        # --- Risk Parameters ---
        self.risk_config = {
            'max_risk_per_trade':       float(os.getenv('MAX_RISK_PER_TRADE')),
            'max_leverage':             int(os.getenv('MAX_LEVERAGE')),
            'min_leverage':             int(os.getenv('MIN_LEVERAGE')),
            'atr_stop_multiplier':      float(os.getenv('ATR_STOP_MULTIPLIER')),
            'trailing_stop_distance':   float(os.getenv('TRAILING_STOP_DISTANCE')),
            'max_concurrent_positions': int(os.getenv('MAX_CONCURRENT_POSITIONS')),
            'target_exposure':          float(os.getenv('TARGET_EXPOSURE')),
            'dynamic_leverage_floor':   int(os.getenv('DYNAMIC_LEVERAGE_FLOOR')),
            'dynamic_leverage_ceiling': int(os.getenv('DYNAMIC_LEVERAGE_CEILING')),
            'risk_reward_target':       float(os.getenv('RISK_REWARD_TARGET')),
        }

        # --- Safety Limits ---
        self.daily_loss_limit = float(os.getenv('DAILY_LOSS_LIMIT'))
        self.consecutive_loss_limit = int(os.getenv('CONSECUTIVE_LOSS_LIMIT'))

        # --- Notifications ---
        self.enable_notifications = os.getenv('ENABLE_NOTIFICATIONS', 'true').lower() == 'true'
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

        os.makedirs('logs', exist_ok=True)

    def get_coin_names(self):
        return [s.replace('/USDT', '') for s in self.symbols]


class BacktestConfig(Config):
    def __init__(self):
        super().__init__(mode='backtest')
        self.initial_balance = float(os.getenv('BACKTEST_INITIAL_BALANCE', 10000))
        self.start_date = os.getenv('BACKTEST_START_DATE', '2024-07-01')
        self.end_date = os.getenv('BACKTEST_END_DATE', '2024-12-31')
        self.auto_trade = True
        self.enable_notifications = False
        self.symbols = os.getenv('BACKTEST_SYMBOLS', 'BTC/USDT').split(',')
