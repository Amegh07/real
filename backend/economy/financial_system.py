"""
Financial System - E1 Asset Classes, E2 Market Mechanics, E3 Banking & Credit
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import random
import math


class AssetType(Enum):
    CASH = "cash"
    COMMODITY = "commodity"
    REAL_ESTATE = "real_estate"
    TOOLS = "tools"
    LIVESTOCK = "livestock"
    VEHICLE = "vehicle"
    BOND = "bond"
    EQUITY = "equity"
    OPTION = "option"
    INSURANCE = "insurance"
    IP = "intellectual_property"
    HUMAN_CAPITAL = "human_capital"
    NATURAL_RESOURCE = "natural_resource"
    MONOPOLY = "monopoly_right"
    DEBT = "debt"
    FOREIGN_CURRENCY = "foreign_currency"
    CRYPTO = "cryptographic_asset"
    ART = "collectible"


@dataclass
class Asset:
    asset_type: AssetType
    name: str
    value: float
    quantity: float = 1.0
    quality: float = 100.0
    metadata: Dict = field(default_factory=dict)


@dataclass
class FinancialInstrument:
    name: str
    instrument_type: str
    value: float
    yield_rate: float = 0.0
    maturity_ticks: int = 0
    risk_level: float = 0.5


@dataclass
class Portfolio:
    assets: Dict[AssetType, List[Asset]] = field(default_factory=dict)
    instruments: List[FinancialInstrument] = field(default_factory=list)
    total_value: float = 0.0
    liquidity: float = 0.0

    def calculate_total(self) -> float:
        total = self.liquidity
        for assets in self.assets.values():
            for a in assets:
                total += a.value * a.quantity
        for inst in self.instruments:
            total += inst.value
        self.total_value = total
        return total


class MarketMechanics:
    def __init__(self):
        self.bid_ask_spread = 0.02
        self.market_depth = 1000.0
        self.order_book_imbalance = 0.0
        self.vwap = 0.0
        self.volatility = 0.15
        self.mean_reversion_speed = 0.1
        self.momentum = 0.0
        self.correlations: Dict[str, float] = {}
        self.price_history: List[float] = []

    def tick(self, price: float, volume: float):
        if len(self.price_history) > 0:
            prev_price = self.price_history[-1]
            self.momentum = (price - prev_price) / prev_price if prev_price > 0 else 0

        self.price_history.append(price)
        if len(self.price_history) > 100:
            self.price_history.pop(0)

        self.volatility = self._calculate_volatility()
        self._update_order_book_imbalance()
        self._calculate_vwap(price, volume)

    def _calculate_volatility(self) -> float:
        if len(self.price_history) < 2:
            return 0.15
        returns = []
        for i in range(1, len(self.price_history)):
            ret = (self.price_history[i] - self.price_history[i-1]) / self.price_history[i-1]
            returns.append(ret)
        if not returns:
            return 0.15
        mean = sum(returns) / len(returns)
        variance = sum((r - mean) ** 2 for r in returns) / len(returns)
        return math.sqrt(variance)

    def _update_order_book_imbalance(self):
        buy_pressure = random.uniform(0.4, 0.6)
        sell_pressure = 1.0 - buy_pressure
        self.order_book_imbalance = (buy_pressure - sell_pressure) * 100

    def _calculate_vwap(self, price: float, volume: float):
        if self.vwap == 0:
            self.vwap = price
        else:
            self.vwap = (self.vwap * 0.7) + (price * 0.3)

    def calculate_slippage(self, order_size: float, is_buy: bool) -> float:
        impact = self._price_impact(order_size)
        return impact * order_size

    def _price_impact(self, order_size: float) -> float:
        base_impact = 0.01
        size_factor = math.sqrt(order_size / self.market_depth)
        volatility_factor = 1 + self.volatility
        return base_impact * size_factor * volatility_factor

    def detect_market_manipulation(self) -> Optional[str]:
        if abs(self.momentum) > 0.1 and abs(self.order_book_imbalance) > 40:
            if self.momentum > 0:
                return "pump_and_dump"
            return "short_squeeze"
        if self.volatility > 0.3:
            return "flash_crash_risk"
        return None


class BankingSystem:
    def __init__(self):
        self.reserve_ratio = 0.1
        self.money_multiplier = 1.0 / self.reserve_ratio
        self.net_interest_margin = 0.03
        self.non_performing_loans = 0.0
        self.deposit_insurance_limit = 100000.0
        self.repo_haircut = 0.1
        self.central_bank_rate = 0.02
        self.yield_curve: Dict[str, float] = {
            "overnight": 0.01,
            "1month": 0.015,
            "3month": 0.02,
            "1year": 0.025,
            "10year": 0.035
        }
        self.bank_runs: List[str] = []
        self.zombie_firms: int = 0
        self.shadow_banking_exposure = 0.0

    def tick(self, economy_stress: float = 0.0):
        self._update_money_multiplier()
        self._update_loan_quality(economy_stress)
        self._update_yield_curve(economy_stress)
        self._update_repo_haircut(economy_stress)
        self._detect_zombie_firms(economy_stress)

    def _update_money_multiplier(self):
        effective_ratio = max(0.01, self.reserve_ratio - (self.non_performing_loans * 0.05))
        self.money_multiplier = 1.0 / effective_ratio

    def _update_loan_quality(self, stress: float):
        target_npl = min(0.3, max(0.01, stress * 0.1))
        self.non_performing_loans = self.non_performing_loans * 0.9 + target_npl * 0.1

    def _update_yield_curve(self, stress: float):
        for term in self.yield_curve:
            if term == "overnight":
                base = self.central_bank_rate
            else:
                base = self.central_bank_rate + 0.015 * int(term.replace("month", "").replace("year", ""))
            
            if stress > 0.5:
                self.yield_curve[term] = base - 0.01
            else:
                self.yield_curve[term] = base

    def _update_repo_haircut(self, stress: float):
        base_haircut = 0.1
        self.repo_haircut = min(1.0, base_haircut + stress * 0.4)

    def _detect_zombie_firms(self, stress: float):
        self.zombie_firms = int(self.zombie_firms * 0.95 + stress * 100)

    def is_inverted(self) -> bool:
        if len(self.yield_curve) >= 2:
            short = self.yield_curve.get("1year", 0.02)
            long = self.yield_curve.get("10year", 0.03)
            return short > long
        return False

    def get_term_spread(self) -> float:
        return self.yield_curve.get("10year", 0.03) - self.yield_curve.get("2year", 0.025)


class FinancialSystem:
    def __init__(self):
        self.portfolios: Dict[int, Portfolio] = {}
        self.market = MarketMechanics()
        self.banking = BankingSystem()
        self.inflation_rate = 0.02
        self.treasury_holdings = 1000000.0

    def register_agent(self, agent_id: int):
        self.portfolios[agent_id] = Portfolio(liquidity=0.0)

    def add_cash(self, agent_id: int, amount: float):
        if agent_id in self.portfolios:
            self.portfolios[agent_id].liquidity += amount

    def get_liquidity(self, agent_id: int) -> float:
        if agent_id in self.portfolios:
            return self.portfolios[agent_id].liquidity
        return 0.0

    def get_net_worth(self, agent_id: int) -> float:
        if agent_id in self.portfolios:
            return self.portfolios[agent_id].calculate_total()
        return 0.0

    def tick(self, economy_stress: float = 0.0):
        self.market.tick(100.0, 1000.0)
        self.banking.tick(economy_stress)
        self._apply_inflation()

    def _apply_inflation(self):
        for portfolio in self.portfolios.values():
            portfolio.liquidity *= (1 - self.inflation_rate / 1000)
        self.inflation_rate = min(0.2, self.inflation_rate + 0.0001)

    def simulate_transaction(self, buyer_id: int, seller_id: int, price: float, quantity: float) -> Dict:
        order_size = price * quantity
        slippage = self.market.calculate_slippage(order_size, True)
        
        if buyer_id in self.portfolios and self.portfolios[buyer_id].liquidity >= price * quantity + slippage:
            self.portfolios[buyer_id].liquidity -= (price * quantity + slippage)
            if seller_id in self.portfolios:
                self.portfolios[seller_id].liquidity += price * quantity
            return {"success": True, "slippage": slippage}
        
        return {"success": False, "reason": "insufficient_funds"}