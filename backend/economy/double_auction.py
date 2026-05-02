"""
Continuous Double Auction Market — God-Tier Architecture
==================================================
Replaces simple treasury + wages with:
- Continuous double auction with order books
- Market impact for large orders
- Circuit breakers
- Heterogeneous trading strategies

Based on spec Section 5.1: Stock Market & Financial System
"""

import uuid
import random
import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto
from collections import defaultdict
from utils.logger import get_logger

logger = get_logger(__name__)


class OrderType(Enum):
    """Types of orders."""
    MARKET = auto()
    LIMIT = auto()
    STOP = auto()
    STOP_LIMIT = auto()


class OrderSide(Enum):
    """Buy or sell."""
    BUY = auto()
    SELL = auto()


class OrderStatus(Enum):
    """Order status."""
    PENDING = 0
    FILLED = 1
    PARTIALLY_FILLED = 2
    CANCELLED = 3
    EXPIRED = 4


@dataclass
class Order:
    """A single order in the market."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:10])
    agent_id: str = ""
    side: OrderSide = OrderSide.BUY
    order_type: OrderType = OrderType.LIMIT
    
    # Price (for limit orders)
    limit_price: float = 0.0
    
    # Quantity
    quantity: float = 0.0
    filled_quantity: float = 0.0
    
    # Timestamps
    tick_created: int = 0
    tick_expires: int = -1
    
    # Status
    status: OrderStatus = OrderStatus.PENDING
    
    def remaining(self) -> float:
        return max(0, self.quantity - self.filled_quantity)
    
    def is_active(self) -> bool:
        return self.status in (OrderStatus.PENDING, OrderStatus.PARTIALLY_FILLED)


@dataclass
class OrderBook:
    """
    Fully featured order book with price-time priority.
    Implements continuous double auction.
    """
    # Orders indexed by price
    buy_orders: Dict[float, List[Order]] = field(default_factory=lambda: defaultdict(list))
    sell_orders: Dict[float, List[Order]] = field(default_factory=lambda: defaultdict(list))
    
    # All orders
    orders: Dict[str, Order] = field(default_factory=dict)
    
    # Price-time priority: oldest at each price gets filled first
    def add_order(self, order: Order):
        """Add order to book."""
        self.orders[order.id] = order
        
        if order.side == OrderSide.BUY:
            # Buy orders: highest price first (descending)
            self.buy_orders[order.limit_price].append(order)
            self.buy_orders[order.limit_price].sort(key=lambda o: o.tick_created)
        else:
            # Sell orders: lowest price first (ascending)
            self.sell_orders[order.limit_price].append(order)
            self.sell_orders[order.limit_price].sort(key=lambda o: o.tick_created)
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        order.status = OrderStatus.CANCELLED
        return True
    
    def get_best_bid(self) -> Tuple[float, Order]:
        """Highest buy price."""
        if not self.buy_orders:
            return 0.0, None
        
        best_price = max(self.buy_orders.keys())
        if self.buy_orders[best_price]:
            return best_price, self.buy_orders[best_price][0]
        return 0.0, None
    
    def get_best_ask(self) -> Tuple[float, Order]:
        """Lowest sell price."""
        if not self.sell_orders:
            return float('inf'), None
        
        best_price = min(self.sell_orders.keys())
        if self.sell_orders[best_price]:
            return best_price, self.sell_orders[best_price][0]
        return float('inf'), None
    
    def get_spread(self) -> float:
        """Bid-ask spread."""
        bid_price, _ = self.get_best_bid()
        ask_price, _ = self.get_best_ask()
        
        if bid_price == 0.0 or ask_price == float('inf'):
            return float('inf')
        
        return ask_price - bid_price
    
    def get_market_depth(self, levels: int = 5) -> Dict[str, list]:
        """Get market depth (orders at each price level)."""
        buy_depth = []
        sell_depth = []
        
        # Top N buy prices
        sorted_bids = sorted(self.buy_orders.keys(), reverse=True)
        for price in sorted_bids[:levels]:
            total_qty = sum(o.remaining() for o in self.buy_orders[price] if o.is_active())
            if total_qty > 0:
                buy_depth.append({"price": price, "quantity": total_qty})
        
        # Top N sell prices  
        sorted_asks = sorted(self.sell_orders.keys())
        for price in sorted_asks[:levels]:
            total_qty = sum(o.remaining() for o in self.sell_orders[price] if o.is_active())
            if total_qty > 0:
                sell_depth.append({"price": price, "quantity": total_qty})
        
        return {"bids": buy_depth, "asks": sell_depth}
    
    def tick(self, current_tick: int):
        """Expire old orders."""
        for order in list(self.orders.values()):
            if order.status == OrderStatus.PENDING:
                if order.tick_expires > 0 and current_tick > order.tick_expires:
                    order.status = OrderStatus.EXPIRED


@dataclass
class TradingStrategy(Enum):
    """Different agent trading strategies."""
    VALUE = auto()          # DCF analysis, buy dips
    MOMENTUM = auto()        # Buy rising, sell falling
    MEAN_REVERSION = auto()  # Bet on average
    NOISE = auto()           # Random trading
    INSIDER = auto()        # Trade on non-public info
    MARKET_MAKER = auto()    # Provide liquidity


@dataclass
class Market:
    """
    Complete continuous double auction market.
    Handles order books, matching, circuit breakers.
    """
    name: str = "default"
    tick: int = 0
    
    # Order books by symbol
    books: Dict[str, OrderBook] = field(default_factory=dict)
    
    # Price history
    price_history: Dict[str, List[dict]] = field(default_factory=dict)
    
    # Market statistics
    price: float = 100.0
    previous_price: float = 100.0
    volume: float = 0.0
    openinterest: float = 0.0
    
    # Circuit breaker
    circuit_breaker_active: bool = False
    circuit_breaker_limit: float = 0.10  # 10% move triggers
    
    # Trading halts
    halted: bool = False
    halt_reason: str = ""
    
    # Market maker
    market_maker_spread: float = 0.02
    
    def register_symbol(self, symbol: str):
        """Register new trading symbol."""
        if symbol not in self.books:
            self.books[symbol] = OrderBook()
            self.price_history[symbol] = []
    
    def submit_order(
        self,
        symbol: str,
        agent_id: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: float,
        limit_price: float = None,
        tick_expires: int = -1
    ) -> Order:
        """Submit order to market."""
        if symbol not in self.books:
            self.register_symbol(symbol)
        
        order = Order(
            agent_id=agent_id,
            side=side,
            order_type=order_type,
            limit_price=limit_price or 0,
            quantity=quantity,
            tick_created=self.tick,
            tick_expires=tick_expires
        )
        
        # Market orders get executed immediately
        if order_type == OrderType.MARKET:
            order.limit_price = self._get_market_price(side, symbol)

        self.books[symbol].add_order(order)
        
        # Match if possible
        if not self.halted:
            self._match_orders(symbol)
        
        return order
    
    def _get_market_price(self, side: OrderSide, symbol: str) -> float:
        """Get price for market order."""
        book = self.books.get(symbol, OrderBook())
        
        if side == OrderSide.BUY:
            _, best_ask = book.get_best_ask()
            if best_ask:
                return best_ask.limit_price
            return self.price * 1.01  # Slippage
        else:
            _, best_bid = book.get_best_bid()
            if best_bid:
                return best_bid.limit_price
            return self.price * 0.99
    
    def _match_orders(self, symbol: str):
        """Match buy/sell orders (continuous double auction)."""
        book = self.books[symbol]
        
        # Get best bid and ask
        bid_price, bid_order = book.get_best_bid()
        ask_price, ask_order = book.get_best_ask()
        
        # Check if can match
        if bid_price >= ask_price and bid_price > 0:
            # Determine fill price (price-time priority: oldest order at best price)
            fill_price = min(bid_price, ask_price)
            
            # Calculate quantity
            bid_rem = bid_order.remaining()
            ask_rem = ask_order.remaining()
            fill_qty = min(bid_rem, ask_rem)
            
            # Apply market impact for large orders
            impact = self._calculate_market_impact(fill_qty)
            fill_price *= (1 + impact) if bid_order.side == OrderSide.BUY else (1 - impact)
            
            # Fill orders
            bid_order.filled_quantity += fill_qty
            ask_order.filled_quantity += fill_qty
            
            # Update status
            if bid_order.remaining() <= 0:
                bid_order.status = OrderStatus.FILLED
            else:
                bid_order.status = OrderStatus.PARTIALLY_FILLED
            
            if ask_order.remaining() <= 0:
                ask_order.status = OrderStatus.FILLED
            else:
                ask_order.status = OrderStatus.PARTIALLY_FILLED
            
            # Update market price
            self.previous_price = self.price
            self.price = fill_price
            self.volume += fill_qty
            
            # Record history
            self._record_price(symbol)
            
            # Check circuit breaker
            self._check_circuit_breaker()
    
    def _calculate_market_impact(self, order_quantity: float) -> float:
        """Calculate price impact for large orders."""
        # Square root law
        if self.volume == 0:
            return 0.0
        
        impact = 0.1 * (order_quantity / (self.volume + 1)) ** 0.5
        return min(0.1, impact)  # Cap at 10%
    
    def _check_circuit_breaker(self):
        """Check circuit breaker limits."""
        if self.previous_price == 0:
            return
        
        pct_change = abs(self.price - self.previous_price) / self.previous_price
        
        if pct_change > self.circuit_breaker_limit:
            self.halted = True
            self.circuit_breaker_active = True
            self.halt_reason = f"Circuit breaker triggered: {pct_change:.2%} move"
            logger.warning(self.halt_reason)
    
    def resume_trading(self):
        """Resume after halt."""
        self.halted = False
        self.circuit_breaker_active = False
        self.halt_reason = ""
    
    def _record_price(self, symbol: str):
        """Record price history."""
        self.price_history[symbol].append({
            "tick": self.tick,
            "price": self.price,
            "volume": self.volume
        })
        
        # Keep last 1000
        if len(self.price_history[symbol]) > 1000:
            self.price_history[symbol] = self.price_history[symbol][-1000:]
    
    def advance_tick(self):
        """Advance market time."""
        self.tick += 1
        
        # Expire old orders
        for book in self.books.values():
            book.tick(self.tick)
    
    def get_statistics(self) -> dict:
        """Market statistics."""
        total_orders = sum(len(b.orders) for b in self.books.values())
        active_orders = sum(
            sum(1 for o in b.orders.values() if o.is_active())
            for b in self.books.values()
        )
        
        spreads = [book.get_spread() for book in self.books.values() if book.get_spread() > 0]
        avg_spread = round(sum(spreads) / len(spreads), 2) if spreads else 0.0

        return {
            "price": round(self.price, 2),
            "previous_price": round(self.previous_price, 2),
            "volume": round(self.volume, 2),
            "spread": avg_spread,
            "total_orders": total_orders,
            "active_orders": active_orders,
            "halted": self.halted,
            "halt_reason": self.halt_reason
        }


# Trading strategies for agents
def generate_agent_order(
    market: Market,
    agent_id: str,
    symbol: str,
    strategy: TradingStrategy,
    current_price: float
) -> Tuple[OrderSide, float, float]:
    """Generate order based on strategy."""
    if strategy == TradingStrategy.MOMENTUM:
        # Trend following
        momentum = 0
        if len(market.price_history.get(symbol, [])) > 5:
            recent = market.price_history[symbol][-5:]
            if recent[-1]["price"] > recent[0]["price"]:
                momentum = 1
            else:
                momentum = -1
        
        if momentum > 0:
            return OrderSide.BUY, current_price * 1.01, 10.0
        elif momentum < 0:
            return OrderSide.SELL, current_price * 0.99, 10.0
    
    elif strategy == TradingStrategy.MEAN_REVERSION:
        # Buy low, sell high
        if len(market.price_history.get(symbol, [])) > 20:
            avg = sum(h["price"] for h in market.price_history[symbol][-20:]) / 20
            if current_price < avg * 0.95:
                return OrderSide.BUY, current_price * 0.98, 15.0
            elif current_price > avg * 1.05:
                return OrderSide.SELL, current_price * 1.02, 15.0
    
    elif strategy == TradingStrategy.NOISE:
        # Random
        if random.random() < 0.5:
            return OrderSide.BUY, current_price * random.uniform(0.98, 1.02), random.uniform(1, 10)
        else:
            return OrderSide.SELL, current_price * random.uniform(0.98, 1.02), random.uniform(1, 10)
    
    return None, current_price, 0.0