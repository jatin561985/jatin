"""Catalog of option strategies used by the trading bot.

The module keeps a structured representation of the strategy playbook
provided by the user so it can be consumed by both the automated
decision-making engine and the spreadsheet reporting layer.  Each
strategy stores the key characteristics that traders typically track –
market view, payoff profile, breakeven maths, margin impact, and the
qualitative pros/cons that drive discretionary selection.

Only high level descriptions are included here; pricing models and
precise position management rules are handled elsewhere in the system.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Strategy:
    """Metadata container describing a single option strategy."""

    name: str
    market_view: str
    max_profit: str
    max_loss: str
    premium: str
    strategy_type: str
    breakeven: str = ""
    margin: str = ""
    effect_of_time: str = ""
    effect_of_volatility: str = ""
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    setup: str = ""
    description: str = ""

    def to_record(self) -> Dict[str, str]:
        """Converts the dataclass into a flat dictionary for DataFrames."""

        return {
            "Name": self.name,
            "Market View": self.market_view,
            "Setup": self.setup,
            "Breakeven": self.breakeven,
            "Max Profit": self.max_profit,
            "Max Loss": self.max_loss,
            "Premium": self.premium,
            "Margin": self.margin,
            "Effect of Time": self.effect_of_time,
            "Effect of Volatility": self.effect_of_volatility,
            "Pros": "\n".join(self.pros),
            "Cons": "\n".join(self.cons),
            "Description": self.description,
            "Category": self.strategy_type,
        }


_all_strategies: List[Strategy] = [
    # ------------------------------------------------------------------
    # Bullish directional structures
    # ------------------------------------------------------------------
    Strategy(
        name="Buy Call",
        market_view="Bullish – expecting a strong upside move before expiry.",
        setup="Buy an at-the-money or slightly out-of-the-money call option.",
        breakeven="Strike Price + Premium Paid",
        max_profit="Unlimited",
        max_loss="Limited to the premium paid",
        premium="Pay",
        margin="Not required",
        effect_of_time="Negative theta – loses value every passing day without a rally.",
        effect_of_volatility="Higher IV lifts the option price and helps the trade.",
        pros=[
            "Unlimited upside participation.",
            "Risk strictly limited to the premium paid.",
        ],
        cons=[
            "Premium can decay to zero if the index fails to finish above the strike.",
            "Time decay hurts when the expected move is slow to arrive.",
        ],
        description="A simple long call used when conviction on upside momentum is high.",
        strategy_type="bullish",
    ),
    Strategy(
        name="Sell Put",
        market_view="Moderately bullish – expecting price stability or a gentle rise.",
        setup="Sell a put option near or slightly below the current index level.",
        breakeven="Strike Price - Premium Received",
        max_profit="Limited to the premium received",
        max_loss="Substantial downside risk if the index collapses",
        premium="Receive",
        margin="Required",
        effect_of_time="Positive theta – the sold option decays in favour of the seller.",
        effect_of_volatility="Rising IV inflates option value and hurts the short position.",
        pros=[
            "Generates income when the index holds steady or moves up modestly.",
            "Allows profit even if the market drifts mildly lower.",
        ],
        cons=[
            "Large losses possible on sharp downside moves.",
            "Requires margin and the ability to take assignment risk.",
        ],
        description="A classic premium-collection approach for moderately bullish views.",
        strategy_type="bullish",
    ),
    Strategy(
        name="Bull Call Spread",
        market_view="Moderately bullish with expectation of a capped upside move.",
        setup="Buy a call near the money and sell a higher strike call with same expiry.",
        breakeven="Bought Strike + Net Premium Paid",
        max_profit="Higher Strike - Lower Strike - Net Premium Paid",
        max_loss="Net Premium Paid",
        premium="Pay",
        margin="Required",
        effect_of_time="Mild negative theta – reduced decay versus naked long call.",
        effect_of_volatility="Effects partially offset between long and short call legs.",
        pros=[
            "Lower capital outlay compared with buying a single call.",
            "Risk capped at the net premium paid.",
            "Less sensitive to IV swings than a naked long option.",
        ],
        cons=[
            "Upside profit is capped by the short call.",
            "Requires margin for the short leg.",
        ],
        description="Debit call spread targeting a controlled upside move.",
        strategy_type="bullish",
    ),
    Strategy(
        name="Bull Put Spread",
        market_view="Mildly bullish – expecting the index to hold or drift higher.",
        setup="Sell a put near the money and buy a lower strike put for protection.",
        breakeven="Sold Strike - Net Premium Received",
        max_profit="Net Premium Received",
        max_loss="Higher Strike - Lower Strike - Net Premium Received",
        premium="Receive",
        margin="Required",
        effect_of_time="Positive theta with reduced decay risk thanks to the hedge.",
        effect_of_volatility="Changes largely offset between the short and long puts.",
        pros=[
            "Earns income while keeping downside risk defined.",
            "Profitable even if the index moves slightly lower.",
            "Less volatile P&L than a naked short put.",
        ],
        cons=[
            "Limited upside – max gain equals the net credit.",
            "Still requires margin for the spread.",
        ],
        description="Credit put spread used for range-bound to mildly bullish markets.",
        strategy_type="bullish",
    ),
    Strategy(
        name="Call Ratio Back Spread",
        market_view="Very bullish – seeking gains from explosive upside moves.",
        setup="Sell one lower-strike call and buy two higher-strike calls of same expiry.",
        breakeven=(
            "If net credit: Lower Strike + Net Premium Received and Higher Strike + "
            "(Higher Strike - Lower Strike) - Net Premium Received. "
            "If net debit: Higher Strike + (Higher Strike - Lower Strike) + Net Premium Paid"
        ),
        max_profit="Unlimited",
        max_loss=(
            "If debit: Higher Strike - Lower Strike + Net Premium Paid. "
            "If credit: Higher Strike - Lower Strike - Net Premium Received"
        ),
        premium="Pay/Receive depending on structure",
        margin="Required",
        effect_of_time="Mixed – long options decay while the short call benefits.",
        effect_of_volatility="Higher IV benefits the excess long calls.",
        pros=[
            "Unlimited profit potential in sharp rallies.",
            "Downside risk limited by the ratio structure.",
            "Possibility of entering for a small credit or zero cost.",
        ],
        cons=[
            "Can suffer moderate losses if the market grinds higher slowly.",
            "Complex payoff that requires active monitoring.",
        ],
        description="Ratioed call spread designed for breakout scenarios.",
        strategy_type="bullish",
    ),
    Strategy(
        name="Long Calendar (Call)",
        market_view="Neutral to moderately bullish around the near-term expiry.",
        setup="Buy a far expiry call and sell a near expiry call at the same strike.",
        breakeven="Depends on volatility and time decay – use a strategy builder for precision.",
        max_profit=(
            "Occurs when spot settles at the strike at near expiry: "
            "Value of long call at expiry - entry cost + premium from short call"
        ),
        max_loss="Net Premium Paid",
        premium="Pay",
        margin="Required",
        effect_of_time="Benefits from faster decay of the short near-term call.",
        effect_of_volatility="Higher IV boosts the long-dated option more than the short leg.",
        pros=[
            "Generates income from theta decay while maintaining upside optionality.",
            "Limited risk due to owning the far-month call.",
            "Flexible – short leg can be rolled across expiries.",
        ],
        cons=[
            "Requires monitoring as P&L is path dependent.",
            "Limited profit window if price drifts far from the strike.",
        ],
        description="Calendar spread leveraging different expiry profiles.",
        strategy_type="bullish",
    ),
    Strategy(
        name="Bull Condor",
        market_view="Bullish with expectation of expiry between the short call strikes.",
        setup="Buy call (strike1), sell call (strike2), sell call (strike3), buy call (strike4) with equal spacing.",
        breakeven="Lower: Strike1 + Net Premium Paid; Upper: Strike4 - Net Premium Paid",
        max_profit="Strike2 - Strike1 - Net Premium Paid",
        max_loss="Net Premium Paid",
        premium="Usually Pay",
        margin="Required",
        effect_of_time="Negative while below lower strike; positive when price sits between the short strikes.",
        effect_of_volatility="Relatively muted due to multiple legs.",
        pros=[
            "Capped risk with an attractive reward-to-risk ratio.",
            "Profits grow as expiry approaches if price remains in target zone.",
        ],
        cons=[
            "Losses occur if price finishes outside the defined corridor.",
            "More complex to manage owing to four option legs.",
        ],
        description="A four-leg debit structure targeting a specific bullish expiry range.",
        strategy_type="bullish",
    ),
    Strategy(
        name="Bull Butterfly",
        market_view="Bullish with expectation of expiry near the middle short strike.",
        setup="Buy call (strike1), sell two calls (strike2), buy call (strike3) – equidistant strikes.",
        breakeven="Lower: Strike1 + Net Premium Paid; Upper: Strike3 - Net Premium Paid",
        max_profit="Strike2 - Strike1 - Net Premium Paid",
        max_loss="Net Premium Paid",
        premium="Usually Pay",
        margin="Required",
        effect_of_time="Negative outside the body; positive as price gravitates to the middle strike.",
        effect_of_volatility="Low sensitivity due to opposing legs.",
        pros=[
            "Defined risk with favourable payoff when the forecast price is precise.",
            "Cheaper than buying a single call for the same price target.",
        ],
        cons=[
            "Requires price to finish near the middle strike for max payoff.",
            "Involves three option legs and associated execution costs.",
        ],
        description="Classic butterfly tailored for bullish directional targets.",
        strategy_type="bullish",
    ),
    Strategy(
        name="Range Forward",
        market_view="Bullish with willingness to finance upside via selling downside risk.",
        setup="Buy an out-of-the-money call and sell a put below spot to create near-zero cost.",
        breakeven="Put Strike - Net Premium Received or Call Strike + Net Premium Paid",
        max_profit="Unlimited on the upside",
        max_loss="Substantial downside if index falls below short put",
        premium="Typically zero cost (small debit/credit possible)",
        margin="Required",
        effect_of_time="Largely neutral as long and short legs offset.",
        effect_of_volatility="Minimal net effect with opposing exposures.",
        pros=[
            "Participate in upside with little or no upfront premium.",
            "Short put provides income to finance the long call.",
        ],
        cons=[
            "Significant downside risk through the naked short put.",
            "Margin intensive due to short option exposure.",
        ],
        description="Synthetic bullish structure combining a long call with short put financing.",
        strategy_type="bullish",
    ),
    Strategy(
        name="Buy Future",
        market_view="Bullish conviction on directional move.",
        setup="Buy index futures contract.",
        breakeven="Entry price of the future",
        max_profit="Unlimited",
        max_loss="Unlimited",
        premium="No premium",
        margin="Required",
        effect_of_time="No theta impact on futures.",
        effect_of_volatility="Unaffected by IV changes.",
        pros=[
            "Straightforward high-delta exposure to the index.",
            "Highly liquid with transparent pricing.",
        ],
        cons=[
            "Leverage can magnify losses quickly.",
            "Requires margin and diligent risk control.",
        ],
        description="Directional futures position replicating index movement one-for-one.",
        strategy_type="bullish",
    ),
    Strategy(
        name="Long Synthetic Future",
        market_view="Bullish – replicating futures using options.",
        setup="Buy a call and sell a put at the same strike to synthetically go long.",
        breakeven="Strike ± Net Premium (depends on net debit/credit)",
        max_profit="Unlimited",
        max_loss="Unlimited",
        premium="Can be debit, credit or near zero",
        margin="Required",
        effect_of_time="Nearly neutral as long and short theta offset.",
        effect_of_volatility="Nearly neutral given matched options.",
        pros=[
            "Mimics a future with potentially lower transaction costs.",
            "Can be structured with little or no upfront premium.",
        ],
        cons=[
            "Carries the same directional risk as futures.",
            "Requires liquid options on both sides and margin for the short put.",
        ],
        description="Synthetic long future constructed from options.",
        strategy_type="bullish",
    ),
    # ------------------------------------------------------------------
    # Bearish directional structures
    # ------------------------------------------------------------------
    Strategy(
        name="Buy Put",
        market_view="Bearish – expecting a sharp downward move before expiry.",
        setup="Buy an at-the-money or slightly out-of-the-money put option.",
        breakeven="Strike Price - Premium Paid",
        max_profit="Substantial as the index falls",
        max_loss="Premium Paid",
        premium="Pay",
        margin="Not required",
        effect_of_time="Negative theta – value erodes without a quick sell-off.",
        effect_of_volatility="Higher IV inflates the put's value.",
        pros=[
            "Unlimited profit potential as markets slide.",
            "Risk capped at the premium paid.",
        ],
        cons=[
            "Loses entire premium if price stays above strike at expiry.",
            "Time decay accelerates near expiry.",
        ],
        description="A straightforward bearish bet via long puts.",
        strategy_type="bearish",
    ),
    Strategy(
        name="Sell Call",
        market_view="Moderately bearish – expecting the index to stay flat or decline slightly.",
        setup="Sell a call option near or slightly above current price.",
        breakeven="Strike Price + Premium Received",
        max_profit="Premium Received",
        max_loss="Unlimited if index rallies sharply",
        premium="Receive",
        margin="Required",
        effect_of_time="Positive theta – the option decay benefits the seller.",
        effect_of_volatility="Rising IV inflates call price and hurts the short.",
        pros=[
            "Generates income when price remains capped.",
            "Profits even if the market drifts modestly higher.",
        ],
        cons=[
            "Unlimited upside risk without hedging.",
            "May require stock delivery for single-stock options.",
        ],
        description="Premium-selling approach for a mildly bearish stance.",
        strategy_type="bearish",
    ),
    Strategy(
        name="Bear Call Spread",
        market_view="Mildly bearish – expecting the index to stay below a ceiling.",
        setup="Sell a call near the money and buy a higher strike call for protection.",
        breakeven="Sold Strike + Net Premium Received",
        max_profit="Net Premium Received",
        max_loss="Higher Strike - Lower Strike - Net Premium Received",
        premium="Receive",
        margin="Required",
        effect_of_time="Positive theta with reduced risk due to protective long call.",
        effect_of_volatility="Largely hedged because both legs respond similarly.",
        pros=[
            "Capped risk versus a naked short call.",
            "Earns income even if price rises slightly.",
        ],
        cons=[
            "Profit limited to the net credit.",
            "Requires margin for the spread.",
        ],
        description="Bearish credit spread suited for capped upside scenarios.",
        strategy_type="bearish",
    ),
    Strategy(
        name="Bear Put Spread",
        market_view="Moderately bearish with expectation of a controlled sell-off.",
        setup="Buy a near strike put and sell a lower strike put of same expiry.",
        breakeven="Bought Strike - Net Premium Paid",
        max_profit="Higher Strike - Lower Strike - Net Premium Paid",
        max_loss="Net Premium Paid",
        premium="Pay",
        margin="Required",
        effect_of_time="Negative but less severe than a naked long put.",
        effect_of_volatility="Impacts largely offset across the spread.",
        pros=[
            "Cheaper bearish exposure than buying a standalone put.",
            "Risk capped to the net debit paid.",
            "Less volatile P&L thanks to short put hedge.",
        ],
        cons=[
            "Profit potential capped by the lower strike short put.",
            "Requires margin for the short leg.",
        ],
        description="Debit put spread for measured bearish views.",
        strategy_type="bearish",
    ),
    Strategy(
        name="Put Ratio Back Spread",
        market_view="Very bearish – seeking gains from a sharp decline.",
        setup="Sell one higher strike put and buy two lower strike puts.",
        breakeven=(
            "If debit: Lower Strike - (Higher Strike - Lower Strike) - Net Premium Paid. "
            "If credit: Lower Breakeven = Lower Strike - (Lower Strike - Higher Strike) + Net Premium Received; "
            "Upper Breakeven = Higher Strike - Net Premium Received"
        ),
        max_profit="Unlimited on the downside",
        max_loss=(
            "If debit: Higher Strike - Lower Strike + Net Premium Paid. "
            "If credit: Higher Strike - Lower Strike - Net Premium Received"
        ),
        premium="Pay/Receive depending on structure",
        margin="Required",
        effect_of_time="Mixed – long puts decay while the short put earns theta.",
        effect_of_volatility="Higher IV benefits the extra long puts.",
        pros=[
            "Unlimited profit if the index collapses.",
            "Can be initiated for little or no cost.",
            "Limited risk if the market moves slightly higher.",
        ],
        cons=[
            "Moderate losses possible if price drifts lower slowly.",
            "Requires diligent management of the ratioed exposure.",
        ],
        description="Ratioed put spread for crash protection or event hedging.",
        strategy_type="bearish",
    ),
    Strategy(
        name="Long Calendar (Put)",
        market_view="Neutral to moderately bearish around the near expiry.",
        setup="Buy a far expiry put and sell a near expiry put at same strike.",
        breakeven="Path dependent – analyse using an option strategy builder.",
        max_profit=(
            "Realised when spot expires at strike and short put decays to zero: "
            "Value of long put at expiry - entry cost + premium from short put"
        ),
        max_loss="Greater than net premium if price swings far from strike",
        premium="Pay",
        margin="Required",
        effect_of_time="Positive if price hovers near the strike due to rapid decay of short put.",
        effect_of_volatility="Higher IV favours the long-dated option.",
        pros=[
            "Harvests theta while keeping downside optionality alive.",
            "Limited risk through ownership of the far-month put.",
            "Rolling the short put provides flexibility.",
        ],
        cons=[
            "Requires monitoring; payoff varies with price path.",
            "Losses possible if price drifts too far from the strike.",
        ],
        description="Calendar spread expressing a slightly bearish bias.",
        strategy_type="bearish",
    ),
    Strategy(
        name="Bear Condor",
        market_view="Bearish with expectation of expiry between the short put strikes.",
        setup="Buy put (strike1), sell put (strike2), sell put (strike3), buy put (strike4) with equal spacing.",
        breakeven="Lower: Strike1 - Net Premium Paid; Upper: Strike4 + Net Premium Paid",
        max_profit="Strike1 - Strike2 - Net Premium Paid",
        max_loss="Net Premium Paid",
        premium="Usually Pay",
        margin="Required",
        effect_of_time="Negative if price stays above highest strike, positive inside target range.",
        effect_of_volatility="Subdued response thanks to multiple offsetting legs.",
        pros=[
            "Defined risk structure with attractive reward-to-risk within target zone.",
            "Earnings accelerate as expiry approaches when price is within the plateau.",
        ],
        cons=[
            "Losses realised if price ends outside the designed corridor.",
            "Managing four legs adds operational complexity.",
        ],
        description="Four-leg debit structure aimed at bearish expiry targets.",
        strategy_type="bearish",
    ),
    Strategy(
        name="Bear Butterfly",
        market_view="Bearish with expectation of expiry near middle short strike.",
        setup="Buy put (strike1), sell two puts (strike2), buy put (strike3) – equidistant strikes.",
        breakeven="Lower: Strike1 - Net Premium Paid; Upper: Strike3 + Net Premium Paid",
        max_profit="Strike1 - Strike2 - Net Premium Paid",
        max_loss="Net Premium Paid",
        premium="Usually Pay",
        margin="Required",
        effect_of_time="Negative outside the body; positive when price sits near the middle strike.",
        effect_of_volatility="Low due to offsetting long/short legs.",
        pros=[
            "Lower cost bearish play with defined risk.",
            "High reward-to-risk if expiry lands on the centre strike.",
        ],
        cons=[
            "Needs precise forecasting of expiry price.",
            "Execution complexity from multiple legs.",
        ],
        description="Classic bearish butterfly construction.",
        strategy_type="bearish",
    ),
    Strategy(
        name="Risk Reversal",
        market_view="Bearish with willingness to finance the put via a short call.",
        setup="Sell an out-of-the-money call and buy an out-of-the-money put.",
        breakeven="Depends on net premium; analyse using actual strikes.",
        max_profit="Unlimited on the downside",
        max_loss="Unlimited on the upside due to short call",
        premium="Typically near zero cost",
        margin="Required",
        effect_of_time="Neutral as theta from long put offsets short call decay.",
        effect_of_volatility="Net effect small with opposing exposures.",
        pros=[
            "Finances downside protection without upfront cost.",
            "Provides leveraged returns if the market sells off.",
        ],
        cons=[
            "Unlimited risk if the index rallies sharply.",
            "Requires margin to hold the short call.",
        ],
        description="Synthetic short exposure combining long puts with a short call.",
        strategy_type="bearish",
    ),
    Strategy(
        name="Sell Future",
        market_view="Bearish conviction on directional move.",
        setup="Sell index futures contract.",
        breakeven="Entry price of the future",
        max_profit="Unlimited as price falls",
        max_loss="Unlimited if price rallies",
        premium="No premium",
        margin="Required",
        effect_of_time="No theta impact on futures.",
        effect_of_volatility="Futures unaffected by IV.",
        pros=[
            "Direct high-delta short exposure.",
            "Liquid and simple to execute.",
        ],
        cons=[
            "Unlimited loss potential if move goes against the trader.",
            "Leverage requires disciplined risk management.",
        ],
        description="Directional short futures position.",
        strategy_type="bearish",
    ),
    Strategy(
        name="Short Synthetic Future",
        market_view="Bearish – replicating a short future using options.",
        setup="Sell a call and buy a put at the same strike.",
        breakeven="Strike ± Net Premium (depending on net debit/credit)",
        max_profit="Unlimited on the downside",
        max_loss="Unlimited on the upside",
        premium="Can be debit, credit or near zero",
        margin="Required",
        effect_of_time="Nearly neutral thanks to offsetting theta.",
        effect_of_volatility="Nearly neutral with matched options.",
        pros=[
            "Replicates short futures payoff while staying in options market.",
            "Can be structured with low upfront cost.",
        ],
        cons=[
            "Carries unlimited upside risk without additional hedges.",
            "Needs liquid options at the chosen strike.",
        ],
        description="Synthetic short future built from options.",
        strategy_type="bearish",
    ),
    # ------------------------------------------------------------------
    # Neutral income and range-bound structures
    # ------------------------------------------------------------------
    Strategy(
        name="Short Straddle",
        market_view="Neutral – expecting very low volatility around a single strike.",
        setup="Sell at-the-money call and put with the same strike and expiry.",
        breakeven="Strike ± Net Premium Received",
        max_profit="Net Premium Received",
        max_loss="Unlimited on either side",
        premium="Receive",
        margin="Required",
        effect_of_time="Strongly positive – profits accrue as options decay.",
        effect_of_volatility="Higher IV hurts as option values increase.",
        pros=[
            "Collects premium rapidly when price stays stable.",
            "Delta-neutral at inception.",
        ],
        cons=[
            "Unlimited loss potential if a large move occurs.",
            "High margin requirement.",
        ],
        description="Classic neutral income strategy betting on low realised volatility.",
        strategy_type="neutral",
    ),
    Strategy(
        name="Iron Butterfly",
        market_view="Neutral – expecting price to finish near the sold strike.",
        setup="Sell ATM call and put; buy protective wings equidistant away.",
        breakeven="Middle Strike ± Net Premium Received",
        max_profit="Net Premium Received",
        max_loss="Distance between wing and body strikes minus net premium",
        premium="Receive",
        margin="Required",
        effect_of_time="Positive theta from short body options.",
        effect_of_volatility="Higher IV hurts as short options become costlier.",
        pros=[
            "Limited risk compared with a naked straddle.",
            "Income focused while remaining delta neutral.",
        ],
        cons=[
            "Narrow profit range.",
            "Four-leg structure increases execution effort.",
        ],
        description="Credit strategy combining a short straddle with protective wings.",
        strategy_type="neutral",
    ),
    Strategy(
        name="Short Strangle",
        market_view="Neutral – expecting price to stay within a broader range.",
        setup="Sell out-of-the-money put and call with same expiry.",
        breakeven="Put Strike - Net Premium Received and Call Strike + Net Premium Received",
        max_profit="Net Premium Received",
        max_loss="Unlimited beyond either breakeven",
        premium="Receive",
        margin="Required",
        effect_of_time="Positive theta as both options decay.",
        effect_of_volatility="Higher IV increases risk as option prices rise.",
        pros=[
            "Wider profit zone than a straddle.",
            "Income generation from two option premiums.",
        ],
        cons=[
            "Unlimited risk if the market trends strongly.",
            "Margin intensive due to naked options.",
        ],
        description="Range-trading premium collection strategy.",
        strategy_type="neutral",
    ),
    Strategy(
        name="Short Iron Condor",
        market_view="Neutral – expecting price to stay within defined bounds.",
        setup="Sell OTM put and call; buy further OTM options on both sides for protection.",
        breakeven="Put Side: Short Put Strike - Net Premium; Call Side: Short Call Strike + Net Premium",
        max_profit="Net Premium Received",
        max_loss="Width between strikes - Net Premium Received",
        premium="Receive",
        margin="Required",
        effect_of_time="Positive theta from short middle options.",
        effect_of_volatility="Higher IV hurts as option values increase.",
        pros=[
            "Limited risk with clearly defined max loss.",
            "Income generation while remaining delta neutral.",
        ],
        cons=[
            "Losses occur if price exits the inner strikes.",
            "Needs monitoring to manage adjustments.",
        ],
        description="Four-leg credit spread capturing premium in range-bound markets.",
        strategy_type="neutral",
    ),
    Strategy(
        name="Batman",
        market_view="Neutral – expecting consolidation within a tight zone.",
        setup="Buy a call slightly above spot, sell two higher calls; buy a put slightly below, sell two lower puts.",
        breakeven="Strike dependent – evaluate with a strategy builder (credit/debit possible).",
        max_profit="For net credit: Higher Call - Lower Call + Net Premium Received; for net debit: Higher Call - Lower Call - Net Premium Paid",
        max_loss="Unlimited without proper sizing",
        premium="Can be credit or debit",
        margin="Required",
        effect_of_time="Positive theta as the double short options decay.",
        effect_of_volatility="Declining IV is favourable; rising IV hurts.",
        pros=[
            "Profits from stable markets with potentially zero upfront cost.",
            "Customisable wings allow tailoring to expected range.",
        ],
        cons=[
            "Complex to structure and manage due to multiple legs.",
            "Unlimited risk if market breaks out strongly.",
        ],
        description="Multi-leg neutral income structure resembling a double short condor.",
        strategy_type="neutral",
    ),
    Strategy(
        name="Double Plateau",
        market_view="Neutral to moderately directional – combines bull and bear condors.",
        setup="Overlay a bull condor and bear condor to create two profit plateaus.",
        breakeven=(
            "Four points: Lower Put Long + Net Premium, Higher Put Long - Net Premium, "
            "Lower Call Long + Net Premium, Higher Call Long - Net Premium"
        ),
        max_profit="Difference between adjacent strikes minus net premium on either side",
        max_loss="Net Premium Paid",
        premium="Pay",
        margin="Required",
        effect_of_time="Depends on where price sits relative to plateaus; profits accelerate near expiry when in range.",
        effect_of_volatility="Outcome depends on price location; moderate sensitivity.",
        pros=[
            "Risk capped at entry cost.",
            "Ability to profit from moderate bullish or bearish outcomes.",
        ],
        cons=[
            "Losses occur if price moves outside defined regions.",
            "Complex to monitor due to multiple legs.",
        ],
        description="Hybrid condor structure delivering two profit zones.",
        strategy_type="neutral",
    ),
    Strategy(
        name="Jade Lizard",
        market_view="Neutral to moderately bullish with no upside risk if structured correctly.",
        setup="Sell an OTM put, sell an OTM call, and buy a further OTM call as protection.",
        breakeven="Lower: Short Put Strike - Net Premium; Upper: None if premium exceeds call spread width",
        max_profit="Net Premium Received",
        max_loss="Unlimited downside if not hedged by long put",
        premium="Receive",
        margin="Required",
        effect_of_time="Positive theta from short options.",
        effect_of_volatility="Higher IV hurts as short options gain value.",
        pros=[
            "Can eliminate upside risk when structured with sufficient credit.",
            "Generates steady income in stable to mildly bullish markets.",
        ],
        cons=[
            "Significant downside risk due to short put.",
            "Requires margin and disciplined adjustment tactics.",
        ],
        description="Credit strategy combining a short put with a call credit spread.",
        strategy_type="neutral",
    ),
    Strategy(
        name="Reverse Jade Lizard",
        market_view="Neutral to moderately bearish with limited downside risk if structured correctly.",
        setup="Sell an OTM call, sell an OTM put, and buy a further OTM put as protection.",
        breakeven="Upper: Short Call Strike + Net Premium; Lower: None if premium exceeds put spread width",
        max_profit="Net Premium Received",
        max_loss="Unlimited upside if price rallies strongly",
        premium="Receive",
        margin="Required",
        effect_of_time="Positive theta from short options.",
        effect_of_volatility="Higher IV hurts as short options appreciate.",
        pros=[
            "Potentially eliminates downside risk when structured correctly.",
            "Premium income while leaning slightly bearish.",
        ],
        cons=[
            "Unlimited risk on strong upside breakouts.",
            "Requires margin and active management.",
        ],
        description="Mirror image of the jade lizard tailored for mild bearish views.",
        strategy_type="neutral",
    ),
    Strategy(
        name="Delta Neutral",
        market_view="Market neutral – focus on hedging directional exposure while harvesting theta.",
        setup="Continuously adjust option/futures mix to keep portfolio delta near zero.",
        breakeven="Depends on hedging frequency and premium collected.",
        max_profit="Limited to premium harvested over the life of the trade",
        max_loss="Depends on hedging efficacy; theoretically large if adjustments lag",
        premium="Receive",
        margin="Required",
        effect_of_time="Positive theta is the primary profit driver.",
        effect_of_volatility="Higher IV can help by boosting option premiums but increases hedging costs.",
        pros=[
            "Minimises directional exposure while collecting time decay.",
            "Adaptable to changing market regimes.",
        ],
        cons=[
            "Requires constant monitoring and active re-hedging.",
            "Transaction costs can erode returns.",
        ],
        description="Framework rather than a single structure – maintain near-zero delta via adjustments.",
        strategy_type="neutral",
    ),
    # ------------------------------------------------------------------
    # Volatility and event-driven structures
    # ------------------------------------------------------------------
    Strategy(
        name="Call Ratio Spread",
        market_view="Neutral to moderately bullish with expectation of slow grind higher.",
        setup="Buy one lower strike call and sell two higher strike calls.",
        breakeven=(
            "If debit: Lower Breakeven = Bought Strike + Net Premium Paid; "
            "Upper Breakeven = Sold Strike + Strike Difference - Net Premium Paid. "
            "If credit: Upper Breakeven = Sold Strike + Strike Difference - Net Premium Received"
        ),
        max_profit="Higher Strike - Lower Strike ± Net Premium (depending on credit/debit)",
        max_loss="Unlimited if price rallies far beyond short strikes",
        premium="Debit or credit depending on strikes",
        margin="Required",
        effect_of_time="Depends on net premium orientation; generally benefits from slow moves.",
        effect_of_volatility="Moderate sensitivity; excess short call exposure suffers if IV spikes.",
        pros=[
            "Can be initiated for little or no cost.",
            "Benefits from gradual upward moves toward the short strike.",
        ],
        cons=[
            "Unlimited risk on explosive rallies.",
            "Requires margin due to uncovered short call.",
        ],
        description="Ratio spread that favours a controlled bullish grind.",
        strategy_type="volatile",
    ),
    Strategy(
        name="Put Ratio Spread",
        market_view="Neutral to moderately bearish with expectation of slow drift lower.",
        setup="Buy one higher strike put and sell two lower strike puts.",
        breakeven=(
            "If debit: Upper Breakeven = Bought Strike - Net Premium Paid; Lower Breakeven = Sold Strike - (Strike Difference - Net Premium Paid). "
            "If credit: Lower Breakeven = Sold Strike - (Strike Difference - Net Premium Received)"
        ),
        max_profit="Higher Strike - Lower Strike ± Net Premium (depending on credit/debit)",
        max_loss="Unlimited if index collapses far below short puts",
        premium="Debit or credit depending on construction",
        margin="Required",
        effect_of_time="Works best with slow price action near short strikes.",
        effect_of_volatility="Higher IV after entry can hurt because of extra short put exposure.",
        pros=[
            "Potential to enter with small or zero cost.",
            "Rewards controlled downward moves.",
        ],
        cons=[
            "Unlimited tail risk on severe sell-offs.",
            "Margin heavy due to naked short put exposure.",
        ],
        description="Ratio spread favouring a measured bearish move.",
        strategy_type="volatile",
    ),
    Strategy(
        name="Long Straddle",
        market_view="Highly volatile – expecting a large move in either direction.",
        setup="Buy at-the-money call and put with same strike and expiry.",
        breakeven="Strike ± Net Premium Paid",
        max_profit="Unlimited",
        max_loss="Net Premium Paid",
        premium="Pay",
        margin="Not required",
        effect_of_time="Negative theta – needs a big move quickly.",
        effect_of_volatility="Higher IV benefits the position.",
        pros=[
            "Unlimited profit in either direction.",
            "Simple structure for event-driven trades.",
        ],
        cons=[
            "Expensive due to double premium outlay.",
            "Time decay erodes value rapidly if market stays calm.",
        ],
        description="Pure volatility bet requiring significant movement.",
        strategy_type="volatile",
    ),
    Strategy(
        name="Long Iron Butterfly",
        market_view="Volatile – expecting a sharp move away from the centre strike.",
        setup="Buy a call and put at centre strike; sell wings further out to reduce cost.",
        breakeven="Call Side: Long Call Strike + Net Premium Paid; Put Side: Long Put Strike - Net Premium Paid",
        max_profit="Width between long and short strikes minus net premium paid",
        max_loss="Net Premium Paid",
        premium="Pay",
        margin="Required",
        effect_of_time="Negative due to long options ownership.",
        effect_of_volatility="Slightly positive as higher IV inflates long options.",
        pros=[
            "Defined risk while positioning for a big move.",
            "Cheaper than a long straddle due to short wings.",
        ],
        cons=[
            "Profits capped compared to plain long straddle.",
            "Requires significant move beyond breakevens.",
        ],
        description="Debit version of the iron butterfly targeting breakout scenarios.",
        strategy_type="volatile",
    ),
    Strategy(
        name="Long Strangle",
        market_view="Volatile – expecting a large move but unsure of direction.",
        setup="Buy out-of-the-money call and put with same expiry.",
        breakeven="Lower Strike - Net Premium Paid and Higher Strike + Net Premium Paid",
        max_profit="Unlimited",
        max_loss="Net Premium Paid",
        premium="Pay",
        margin="Not required",
        effect_of_time="Negative theta – needs large move quickly.",
        effect_of_volatility="Higher IV boosts premiums and helps the trade.",
        pros=[
            "Cheaper than a straddle while keeping unlimited payoff.",
            "Profits from large moves in either direction.",
        ],
        cons=[
            "Requires substantial price movement to breakeven.",
            "Premium decays rapidly in quiet markets.",
        ],
        description="Long volatility play using out-of-the-money options.",
        strategy_type="volatile",
    ),
    Strategy(
        name="Long Iron Condor",
        market_view="Volatile – expecting price to break out beyond the wings.",
        setup="Buy OTM put and call; sell further OTM options to offset cost.",
        breakeven="Put Side: Long Put Strike - Net Premium Paid; Call Side: Long Call Strike + Net Premium Paid",
        max_profit="Width between long and short strikes minus net premium paid",
        max_loss="Net Premium Paid",
        premium="Pay",
        margin="Required",
        effect_of_time="Negative because of long outer options.",
        effect_of_volatility="Slightly positive as higher IV aids long options.",
        pros=[
            "Defined risk with lower cost than pure long strangle/straddle.",
            "Targets large moves while partially financing via short legs.",
        ],
        cons=[
            "Payoff capped relative to unlimited structures.",
            "Needs significant move to overcome debit.",
        ],
        description="Debit condor that profits from volatility expansion.",
        strategy_type="volatile",
    ),
    Strategy(
        name="Strip",
        market_view="Volatile with bullish bias – expecting big move with preference for upside.",
        setup="Buy two call options and one put at the same strike and expiry.",
        breakeven="Lower: Strike - Net Premium Paid; Upper: Strike + (Net Premium Paid / 2)",
        max_profit="Unlimited, weighted more to upside moves",
        max_loss="Net Premium Paid",
        premium="Pay",
        margin="Not required",
        effect_of_time="Negative theta – requires large move.",
        effect_of_volatility="Higher IV increases option prices and helps.",
        pros=[
            "Generates greater gains on upside breakouts while still profiting from downside.",
            "Risk capped at premium paid.",
        ],
        cons=[
            "Expensive structure requiring sizeable movement.",
            "Time decay erodes value quickly without action.",
        ],
        description="Volatility strategy skewed to benefit more from upside rallies.",
        strategy_type="volatile",
    ),
    Strategy(
        name="Strap",
        market_view="Volatile with bearish bias – expecting big move favouring downside.",
        setup="Buy two put options and one call at the same strike and expiry.",
        breakeven="Lower: Strike - (Net Premium Paid / 2); Upper: Strike + Net Premium Paid",
        max_profit="Unlimited with larger gains on downside moves",
        max_loss="Net Premium Paid",
        premium="Pay",
        margin="Not required",
        effect_of_time="Negative theta – needs a large move.",
        effect_of_volatility="Higher IV boosts options and helps the position.",
        pros=[
            "Greater payoff on downside breaks while keeping upside participation.",
            "Loss capped at premium paid.",
        ],
        cons=[
            "Requires significant movement to overcome premium cost.",
            "Time decay is unfavourable when the move is delayed.",
        ],
        description="Volatility strategy skewed to profit more from declines.",
        strategy_type="volatile",
    ),
]


# Dictionaries for quick lookup and grouping by directional bias
ALL_STRATEGIES: Dict[str, Strategy] = {s.name: s for s in _all_strategies}
BULLISH_STRATEGIES: Dict[str, Strategy] = {
    s.name: s for s in _all_strategies if s.strategy_type == "bullish"
}
BEARISH_STRATEGIES: Dict[str, Strategy] = {
    s.name: s for s in _all_strategies if s.strategy_type == "bearish"
}
NEUTRAL_STRATEGIES: Dict[str, Strategy] = {
    s.name: s for s in _all_strategies if s.strategy_type == "neutral"
}
VOLATILE_STRATEGIES: Dict[str, Strategy] = {
    s.name: s for s in _all_strategies if s.strategy_type == "volatile"
}


def get_strategies_by_view(market_view: str) -> List[Strategy]:
    """Return strategies matching a generalised market view string."""

    view_lower = market_view.lower()

    if "bull" in view_lower:
        return list(BULLISH_STRATEGIES.values())
    if "bear" in view_lower:
        return list(BEARISH_STRATEGIES.values())
    if "neutral" in view_lower:
        return list(NEUTRAL_STRATEGIES.values())
    if "volat" in view_lower or "event" in view_lower:
        return list(VOLATILE_STRATEGIES.values())

    return []


if __name__ == "__main__":
    print("--- Strategy Catalog Overview ---")
    for category_name, catalog in (
        ("Bullish", BULLISH_STRATEGIES),
        ("Bearish", BEARISH_STRATEGIES),
        ("Neutral", NEUTRAL_STRATEGIES),
        ("Volatile", VOLATILE_STRATEGIES),
    ):
        print(f"\n{category_name} Strategies ({len(catalog)} items)")
        for strategy in catalog.values():
            print(f"  - {strategy.name}")
