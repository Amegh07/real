"""
Economic Feature Registry — Sections E1, E2, E3
==============================================
Features 341-400 covering:
- E1: Asset Classes (20 features)
- E2: Market Mechanics (25 features)
- E3: Banking & Credit (15 features)

Total: 60 economic features
"""

from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto


class EconomicSystem(Enum):
    ASSET_CLASSES = auto()
    MARKET_MECHANICS = auto()
    BANKING_CREDIT = auto()


@dataclass
class EconomicFeature:
    feature_id: str
    feature_name: str
    system: EconomicSystem
    normal_range: tuple
    unit: str
    description: str
    measurement: str
    tags: List[str] = field(default_factory=list)


ECONOMIC_FEATURES: dict = {}


def _register_economic_features():
    global ECONOMIC_FEATURES
    
    features = [
        # ============ E1. ASSET CLASSES (20 features) ============
        EconomicFeature("econ.liquid_cash", "Liquid Cash Holdings", EconomicSystem.ASSET_CLASSES,
                        (0, 1000000), "currency", "Currency and demand deposits - inflation erodes",
                        "Balance sheet"),
        EconomicFeature("econ.commodity_stockpiles", "Commodity Stockpiles", EconomicSystem.ASSET_CLASSES,
                        (0, 10000), "units", "Grain, metals, oil - storage costs and spoilage",
                        "Inventory"),
        EconomicFeature("econ.real_estate_quality", "Real Estate Quality", EconomicSystem.ASSET_CLASSES,
                        (0, 1), "score", "Structural condition, location premium, title clarity",
                        "Appraisal"),
        EconomicFeature("econ.real_estate_location", "Real Estate Location Score", EconomicSystem.ASSET_CLASSES,
                        (0, 100), "score", "Access to markets, defense, water, fertility",
                        "Location analysis"),
        EconomicFeature("econ.productive_capital", "Productive Capital (Tools)", EconomicSystem.ASSET_CLASSES,
                        (0, 1), "condition", "Wear state, technological vintage, skill requirement",
                        "Asset assessment"),
        EconomicFeature("econ.livestock_holdings", "Livestock Holdings", EconomicSystem.ASSET_CLASSES,
                        (0, 1000), "animals", "Breeding stock vs. consumption animals",
                        "Census"),
        EconomicFeature("econ.ship_fleet", "Ship/Vehicle Fleet", EconomicSystem.ASSET_CLASSES,
                        (0, 100), "vessels", "Transport capacity, maintenance state, crew",
                        "Fleet registry"),
        EconomicFeature("econ.bonds", "Financial Instruments (Bonds)", EconomicSystem.ASSET_CLASSES,
                        (0, 1000000), "value", "Coupon rate, maturity, issuer credit rating",
                        "Portfolio"),
        EconomicFeature("econ.equity_shares", "Equity Shares", EconomicSystem.ASSET_CLASSES,
                        (0, 100), "%", "Ownership percentage, voting rights, dividends",
                        "Stock holdings"),
        EconomicFeature("econ.options_contracts", "Options Contracts", EconomicSystem.ASSET_CLASSES,
                        (0, 1000), "contracts", "Strike price, expiration, premium, Greeks",
                        "Options chain"),
        EconomicFeature("econ.insurance_policies", "Insurance Policies", EconomicSystem.ASSET_CLASSES,
                        (0, 1), "coverage", "Coverage type, premium, deductible, exclusions",
                        "Policy review"),
        EconomicFeature("econ.intellectual_property", "Intellectual Property", EconomicSystem.ASSET_CLASSES,
                        (0, 1000000), "value", "Patent strength, trade secret, licensing",
                        "IP valuation"),
        EconomicFeature("econ.social_capital", "Social Capital (Network Value)", EconomicSystem.ASSET_CLASSES,
                        (0, 1), "scale", "Connections to powerful agents - convertible",
                        "Network analysis"),
        EconomicFeature("econ.human_capital", "Human Capital (Skill Portfolio)", EconomicSystem.ASSET_CLASSES,
                        (0, 1000000), "value", "Transferable vs. firm-specific; depreciation rate",
                        "Earnings potential"),
        EconomicFeature("econ.natural_resource_rights", "Natural Resource Rights", EconomicSystem.ASSET_CLASSES,
                        (0, 1), "scale", "Water, mineral, timber, grazing; extraction limits",
                        "Rights allocation"),
        EconomicFeature("econ.monopoly_privileges", "Monopoly Privileges", EconomicSystem.ASSET_CLASSES,
                        (0, 1), "binary", "Guild membership, royal charter, patent exclusivity",
                        "Charter review"),
        EconomicFeature("econ.debt_instruments", "Debt Instruments Held", EconomicSystem.ASSET_CLASSES,
                        (0, 1000000), "value", "Loans to others - default risk and collection",
                        "Loan portfolio"),
        EconomicFeature("econ.foreign_currency", "Foreign Currency Holdings", EconomicSystem.ASSET_CLASSES,
                        (0, 1000000), "value", "Exchange rate risk; safe haven demand",
                        "FX holdings"),
        EconomicFeature("econ.cryptographic_assets", "Cryptographic Assets", EconomicSystem.ASSET_CLASSES,
                        (0, 1000000), "value", "Blockchain-based - volatility and regulatory",
                        "Wallet balance"),
        EconomicFeature("econ.collectibles_art", "Collectibles & Art", EconomicSystem.ASSET_CLASSES,
                        (0, 1000000), "value", "Aesthetic value, provenance, liquidity, forgery",
                        "Appraisal"),

        # ============ E2. MARKET MECHANICS (25 features) ============
        EconomicFeature("market.bid_ask_spread", "Bid-Ask Spread", EconomicSystem.MARKET_MECHANICS,
                        (0, 10), "%", "Liquidity measure - widens in uncertainty",
                        "Order book"),
        EconomicFeature("market.market_depth", "Market Depth", EconomicSystem.MARKET_MECHANICS,
                        (0, 1000000), "volume", "Volume available at each price level",
                        "Level 2 data"),
        EconomicFeature("market.order_book_imbalance", "Order Book Imbalance", EconomicSystem.MARKET_MECHANICS,
                        (-1, 1), "ratio", "Buy vs. sell pressure - predicts direction",
                        "Book analysis"),
        EconomicFeature("market.vwap", "Volume-Weighted Average Price", EconomicSystem.MARKET_MECHANICS,
                        (0, 10000), "price", "Benchmark for large trades",
                        "Calculation"),
        EconomicFeature("market.slippage", "Slippage", EconomicSystem.MARKET_MECHANICS,
                        (0, 10), "%", "Executed price vs. expected - increases with order size",
                        "Trade analysis"),
        EconomicFeature("market.price_impact", "Price Impact Function", EconomicSystem.MARKET_MECHANICS,
                        (0, 1), "elasticity", "How much a trade moves the market - square root law",
                        "Impact model"),
        EconomicFeature("market.volatility_clustering", "Volatility Clustering", EconomicSystem.MARKET_MECHANICS,
                        (0, 1), "scale", "High volatility periods cluster - GARCH models",
                        "GARCH fit"),
        EconomicFeature("market.mean_reversion", "Mean Reversion Speed", EconomicSystem.MARKET_MECHANICS,
                        (0, 1), "rate", "How fast prices return to trend",
                        "Half-life estimation"),
        EconomicFeature("market.momentum_persistence", "Momentum Persistence", EconomicSystem.MARKET_MECHANICS,
                        (0, 1), "scale", "Trend continuation - 3-12 month horizon",
                        "Return regression"),
        EconomicFeature("market.cross_asset_correlation", "Cross-Asset Correlation", EconomicSystem.MARKET_MECHANICS,
                        (-1, 1), "r", "Stocks, bonds, commodities co-movement - increases in crisis",
                        "Correlation matrix"),
        EconomicFeature("market.liquidity_spiral", "Liquidity Spiral", EconomicSystem.MARKET_MECHANICS,
                        (0, 1), "scale", "Forced selling → price drop → more margin calls",
                        "Crisis analysis"),
        EconomicFeature("market.flash_crash", "Flash Crash Dynamics", EconomicSystem.MARKET_MECHANICS,
                        (0, 100), "%", "Algorithmic feedback loops - 2010 Dow 1000-point drop",
                        "Event analysis"),
        EconomicFeature("market.hft_latency", "High-Frequency Trading Latency", EconomicSystem.MARKET_MECHANICS,
                        (0, 1000), "microseconds", "Microsecond advantage - colocation at exchanges",
                        "Latency measurement"),
        EconomicFeature("market.front_running", "Front-Running", EconomicSystem.MARKET_MECHANICS,
                        (0, 1), "binary", "Trading ahead of known large orders - illegal",
                        "Regulatory detection"),
        EconomicFeature("market.spoofing", "Spoofing", EconomicSystem.MARKET_MECHANICS,
                        (0, 1), "binary", "Fake orders to manipulate price - layering",
                        "Pattern detection"),
        EconomicFeature("market.wash_trading", "Wash Trading", EconomicSystem.MARKET_MECHANICS,
                        (0, 1), "binary", "Fake volume between same party - inflates interest",
                        "Volume analysis"),
        EconomicFeature("market.pump_dump", "Pump and Dump Scheme", EconomicSystem.MARKET_MECHANICS,
                        (0, 1), "binary", "Hype then sell - penny stock classic",
                        "Price pattern"),
        EconomicFeature("market.short_squeeze", "Short Squeeze", EconomicSystem.MARKET_MECHANICS,
                        (0, 100), "%", "Forced buying to cover shorts - GameStop 2021",
                        "Short interest"),
        EconomicFeature("market.contango_backwardation", "Contango vs. Backwardation", EconomicSystem.MARKET_MECHANICS,
                        (-10, 10), "%", "Futures price above or below spot - storage cost signal",
                        "Curve shape"),
        EconomicFeature("market.carry_trade", "Carry Trade", EconomicSystem.MARKET_MECHANICS,
                        (0, 20), "%", "Borrow low-yield currency, invest high-yield",
                        "Currency pairs"),
        EconomicFeature("market.currency_peg", "Currency Peg Defense", EconomicSystem.MARKET_MECHANICS,
                        (0, 1000000000), "reserves", "Central bank selling reserves - Soros vs BoE",
                        "Reserve level"),
        EconomicFeature("market.sovereign_default", "Sovereign Default Risk", EconomicSystem.MARKET_MECHANICS,
                        (0, 100), "%", "Government bond haircuts - Argentina serial defaulter",
                        "CDS spread"),
        EconomicFeature("market.cds_spread", "Credit Default Swap Spread", EconomicSystem.MARKET_MECHANICS,
                        (0, 10000), "bps", "Insurance cost against default - Lehman indicator",
                        "CDS market"),
        EconomicFeature("market.repo_freeze", "Repo Market Freeze", EconomicSystem.MARKET_MECHANICS,
                        (0, 1), "binary", "Collateralized lending stops - 2008 crisis mechanism",
                        "Repo rate"),
        EconomicFeature("market.qe_impact", "Quantitative Easing Impact", EconomicSystem.MARKET_MECHANICS,
                        (0, 1000000000000), "value", "Central bank asset purchases - wealth inequality",
                        "Balance sheet"),

        # ============ E3. BANKING & CREDIT (15 features) ============
        EconomicFeature("bank.reserve_requirement", "Reserve Requirement Ratio", EconomicSystem.BANKING_CREDIT,
                        (0, 20), "%", "Fraction banks must hold - affects money multiplier",
                        "Central bank policy"),
        EconomicFeature("bank.money_multiplier", "Money Multiplier", EconomicSystem.BANKING_CREDIT,
                        (1, 50), "ratio", "Deposit creation from reserves - 1/reserve ratio",
                        "Calculated"),
        EconomicFeature("bank.net_interest_margin", "Net Interest Margin", EconomicSystem.BANKING_CREDIT,
                        (0, 10), "%", "Lending rate minus deposit rate - bank profitability",
                        "Income statement"),
        EconomicFeature("bank.npl_ratio", "Non-Performing Loan Ratio", EconomicSystem.BANKING_CREDIT,
                        (0, 30), "%", "Bad debt percentage - bank solvency threat",
                        "Portfolio quality"),
        EconomicFeature("bank.bank_run", "Bank Run Dynamics", EconomicSystem.BANKING_CREDIT,
                        (0, 1), "scale", "Self-fulfilling panic - Diamond-Dybvig model",
                        "Withdrawal rate"),
        EconomicFeature("bank.deposit_insurance", "Deposit Insurance Limit", EconomicSystem.BANKING_CREDIT,
                        (0, 1000000), "currency", "Government guarantee - prevents runs up to limit",
                        "Policy coverage"),
        EconomicFeature("bank.too_big_to_fail", "Too Big To Fail Subsidy", EconomicSystem.BANKING_CREDIT,
                        (0, 1), "scale", "Implicit guarantee lowers borrowing costs - moral hazard",
                        "Cost of funds"),
        EconomicFeature("bank.shadow_banking", "Shadow Banking Leverage", EconomicSystem.BANKING_CREDIT,
                        (0, 50), "ratio", "Off-balance-sheet exposure - systemic risk",
                        "Leverage ratio"),
        EconomicFeature("bank.repo_haircut", "Repo Haircut", EconomicSystem.BANKING_CREDIT,
                        (0, 100), "%", "Collateral discount - increases in stress (GFC to 100%)",
                        "Collateral valuation"),
        EconomicFeature("bank.libor_manipulation", "LIBOR Manipulation", EconomicSystem.BANKING_CREDIT,
                        (0, 1), "binary", "Benchmark rate rigging - scandal and replacement",
                        "Investigation"),
        EconomicFeature("bank.negative_rates", "Negative Interest Rates", EconomicSystem.BANKING_CREDIT,
                        (-2, 0), "%", "Central bank charges deposits - bank profitability squeeze",
                        "Policy rate"),
        EconomicFeature("bank.yield_curve", "Yield Curve Inversion", EconomicSystem.BANKING_CREDIT,
                        (-2, 5), "%", "Short rates above long - recession predictor",
                        "Treasury yield"),
        EconomicFeature("bank.term_spread", "Term Spread", EconomicSystem.BANKING_CREDIT,
                        (-2, 5), "%", "10-year minus 2-year Treasury - strongest recession signal",
                        "Spread calculation"),
        EconomicFeature("bank.credit_crunch", "Credit Crunch Transmission", EconomicSystem.BANKING_CREDIT,
                        (0, 1), "scale", "Banks stop lending → business investment falls → recession",
                        "Lending survey"),
        EconomicFeature("bank.zombie_firms", "Zombie Firm Proliferation", EconomicSystem.BANKING_CREDIT,
                        (0, 30), "%", "Kept alive by cheap credit - productivity drag",
                        "Firm classification"),
    ]
    
    for f in features:
        ECONOMIC_FEATURES[f.feature_id] = f


_register_economic_features()


def get_economic_feature(feature_id: str) -> EconomicFeature:
    return ECONOMIC_FEATURES.get(feature_id)


def get_features_by_economic_system(system: EconomicSystem) -> list:
    return [f for f in ECONOMIC_FEATURES.values() if f.system == system]


def get_all_economic_feature_ids() -> list:
    return list(ECONOMIC_FEATURES.keys())


def get_economic_feature_count() -> int:
    return len(ECONOMIC_FEATURES)


class MarketFeature:
    pass