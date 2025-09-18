"""Structured representation of the trading workflow and guardrails.

The definitions here are consumed by the reporting layer so that every
trading session can be exported to Google Sheets or Excel with the
complete operating checklist alongside market analytics and trade
decisions.  Keeping the workflow in code allows the bot to surface
contextual guidance without relying on external documentation.
"""

from typing import List, Dict


WORKFLOW_PHASES: List[Dict[str, str]] = [
    # Phase 1
    {
        "phase": "Phase 1: Prerequisites & Setup",
        "category": "Trading Platforms",
        "task": "Set up broker trading terminal (e.g., Zerodha Kite).",
    },
    {
        "phase": "Phase 1: Prerequisites & Setup",
        "category": "Trading Platforms",
        "task": "Configure charting platform such as TradingView for indices.",
    },
    {
        "phase": "Phase 1: Prerequisites & Setup",
        "category": "Trading Platforms",
        "task": "Prepare option chain analysis tools for NIFTY and SENSEX.",
    },
    {
        "phase": "Phase 1: Prerequisites & Setup",
        "category": "Knowledge Requirements",
        "task": "Study option Greeks (Delta, Gamma, Theta, Vega) and their impact.",
    },
    {
        "phase": "Phase 1: Prerequisites & Setup",
        "category": "Knowledge Requirements",
        "task": "Understand implied volatility dynamics and percentile interpretation.",
    },
    {
        "phase": "Phase 1: Prerequisites & Setup",
        "category": "Knowledge Requirements",
        "task": "Analyze historical index behaviour patterns for NIFTY and SENSEX.",
    },
    {
        "phase": "Phase 1: Prerequisites & Setup",
        "category": "Knowledge Requirements",
        "task": "Review SEBI regulations, margin rules, and broker-specific policies.",
    },
    # Phase 2
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Technical Analysis",
        "task": "Scan daily, weekly, and monthly charts for prevailing trends.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Technical Analysis",
        "task": "Mark key support and resistance zones on the indices.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Technical Analysis",
        "task": "Evaluate moving averages for trend confirmation.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Technical Analysis",
        "task": "Check momentum indicators (RSI, MACD) for strength/weakness cues.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Technical Analysis",
        "task": "Identify chart patterns or breakout levels to monitor intraday.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Fundamental Analysis",
        "task": "Review the economic calendar and note upcoming high-impact events.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Fundamental Analysis",
        "task": "Track central bank communication (e.g., RBI policy updates).",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Fundamental Analysis",
        "task": "Observe global market cues such as SGX Nifty and major US indices.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Fundamental Analysis",
        "task": "Assess FII/DII participation data and directional bias.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Fundamental Analysis",
        "task": "Monitor India VIX levels for volatility regime insights.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Option Chain Analysis",
        "task": "Identify max pain strike to gauge expiry magnet levels.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Option Chain Analysis",
        "task": "Study open interest concentration on calls and puts for S/R zones.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Option Chain Analysis",
        "task": "Calculate put-call ratio and monitor changes from previous sessions.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Option Chain Analysis",
        "task": "Check IV percentiles to understand richness or cheapness of options.",
    },
    {
        "phase": "Phase 2: Pre-Market Analysis",
        "category": "Option Chain Analysis",
        "task": "Derive support and resistance levels from aggregated OI data.",
    },
    # Phase 3
    {
        "phase": "Phase 3: Strategy Selection",
        "category": "Directional Strategies",
        "task": "Match bullish/bearish outlook with appropriate strategy from catalog.",
    },
    {
        "phase": "Phase 3: Strategy Selection",
        "category": "Neutral & Volatility Strategies",
        "task": "Consider neutral or volatile plays when range-bound or event-driven.",
    },
    {
        "phase": "Phase 3: Strategy Selection",
        "category": "Selection Criteria",
        "task": "Align chosen structure with time to expiry (weekly vs monthly).",
    },
    {
        "phase": "Phase 3: Strategy Selection",
        "category": "Selection Criteria",
        "task": "Evaluate risk-reward, breakeven, and margin requirement for each idea.",
    },
    {
        "phase": "Phase 3: Strategy Selection",
        "category": "Selection Criteria",
        "task": "Confirm maximum profit/loss scenarios and stress test assumptions.",
    },
    # Phase 4
    {
        "phase": "Phase 4: Trade Execution",
        "category": "Pre-Trade Checklist",
        "task": "Validate that market view, data, and strategy remain aligned.",
    },
    {
        "phase": "Phase 4: Trade Execution",
        "category": "Pre-Trade Checklist",
        "task": "Size the position based on 0.5% risk-per-trade rule.",
    },
    {
        "phase": "Phase 4: Trade Execution",
        "category": "Pre-Trade Checklist",
        "task": "Select strike criteria and define entry/exit triggers.",
    },
    {
        "phase": "Phase 4: Trade Execution",
        "category": "Pre-Trade Checklist",
        "task": "Outline stop-loss and profit target before placing orders.",
    },
    {
        "phase": "Phase 4: Trade Execution",
        "category": "Order Placement",
        "task": "Pick strikes, expiry (weekly/monthly) and lot size (NIFTY 75, SENSEX 20).",
    },
    {
        "phase": "Phase 4: Trade Execution",
        "category": "Order Placement",
        "task": "Enter using limit orders and leg-in spreads when beneficial.",
    },
    {
        "phase": "Phase 4: Trade Execution",
        "category": "Order Placement",
        "task": "Note weekly expiries (NIFTY Tuesday, SENSEX Thursday) and monthly rollovers.",
    },
    {
        "phase": "Phase 4: Trade Execution",
        "category": "Position Documentation",
        "task": "Record entry time, rationale, and prevailing market context.",
    },
    {
        "phase": "Phase 4: Trade Execution",
        "category": "Position Documentation",
        "task": "Set alerts for critical management levels and log breakeven.",
    },
    # Phase 5
    {
        "phase": "Phase 5: Risk Management",
        "category": "Position Sizing",
        "task": "Risk 0.5% of capital per trade; cap simultaneous exposure at 1%.",
    },
    {
        "phase": "Phase 5: Risk Management",
        "category": "Position Sizing",
        "task": "Maintain 20-30% margin buffer and diversify expiries when possible.",
    },
    {
        "phase": "Phase 5: Risk Management",
        "category": "Stop Loss Rules",
        "task": "Anchor stops to technical levels and respect option Greek signals.",
    },
    {
        "phase": "Phase 5: Risk Management",
        "category": "Stop Loss Rules",
        "task": "Implement time-based exits for theta decay and cap loss at 0.5%.",
    },
    {
        "phase": "Phase 5: Risk Management",
        "category": "Hedging Techniques",
        "task": "Deploy opposing positions or delta-neutral hedges when volatility shifts.",
    },
    {
        "phase": "Phase 5: Risk Management",
        "category": "Hedging Techniques",
        "task": "Use VIX hedges or keep cash to fund defensive adjustments.",
    },
    # Phase 6
    {
        "phase": "Phase 6: Trade Monitoring",
        "category": "Intraday Monitoring",
        "task": "Track index price action versus planned scenario.",
    },
    {
        "phase": "Phase 6: Trade Monitoring",
        "category": "Intraday Monitoring",
        "task": "Watch option Greeks and implied volatility swings.",
    },
    {
        "phase": "Phase 6: Trade Monitoring",
        "category": "Intraday Monitoring",
        "task": "Keep an eye on open interest changes and breaking news.",
    },
    {
        "phase": "Phase 6: Trade Monitoring",
        "category": "Key Metrics",
        "task": "Evaluate realised/unrealised P&L, delta exposure, theta burn, and vega risk.",
    },
    {
        "phase": "Phase 6: Trade Monitoring",
        "category": "Key Metrics",
        "task": "Monitor margin utilisation and ensure limits are respected.",
    },
    {
        "phase": "Phase 6: Trade Monitoring",
        "category": "Adjustment Triggers",
        "task": "Adjust if support/resistance breaks, IV spikes, or stops near.",
    },
    {
        "phase": "Phase 6: Trade Monitoring",
        "category": "Adjustment Triggers",
        "task": "Account for time decay acceleration and structural market changes.",
    },
    # Phase 7
    {
        "phase": "Phase 7: Exit Management",
        "category": "Profit Taking",
        "task": "Scale out at predefined targets or near technical levels.",
    },
    {
        "phase": "Phase 7: Exit Management",
        "category": "Profit Taking",
        "task": "Consider rolling winners to next expiry if thesis persists.",
    },
    {
        "phase": "Phase 7: Exit Management",
        "category": "Loss Management",
        "task": "Respect stop losses, avoid averaging into losers, and close before expiry to sidestep STT.",
    },
    {
        "phase": "Phase 7: Exit Management",
        "category": "Expiry Day",
        "task": "Square positions before 3:00 PM and be aware of physical settlement risks.",
    },
    # Phase 8
    {
        "phase": "Phase 8: Post-Trade Analysis",
        "category": "Performance Review",
        "task": "Compare realised versus expected returns and review win-rate statistics.",
    },
    {
        "phase": "Phase 8: Post-Trade Analysis",
        "category": "Performance Review",
        "task": "Evaluate strategy effectiveness and execution quality.",
    },
    {
        "phase": "Phase 8: Post-Trade Analysis",
        "category": "Journal Maintenance",
        "task": "Document lessons learned, emotional state, and future improvements.",
    },
]


TRADING_PARAMETERS: List[Dict[str, str]] = [
    {"parameter": "NIFTY Lot Size", "details": "75 units per lot."},
    {"parameter": "SENSEX Lot Size", "details": "20 units per lot."},
    {"parameter": "NIFTY Weekly Expiry", "details": "Tuesday."},
    {"parameter": "SENSEX Weekly Expiry", "details": "Thursday."},
    {"parameter": "NIFTY Monthly Expiry", "details": "Last Tuesday of the month."},
    {"parameter": "SENSEX Monthly Expiry", "details": "Last Thursday of the month."},
    {"parameter": "Order Preference", "details": "Use limit orders; leg into spreads when appropriate."},
]


RISK_MANAGEMENT_RULES: List[Dict[str, str]] = [
    {"category": "Position Sizing", "rule": "Risk only 0.5% of capital per trade."},
    {"category": "Position Sizing", "rule": "Ensure total open risk stays below 1% of capital."},
    {"category": "Position Sizing", "rule": "Maintain 20-30% excess margin buffer."},
    {"category": "Position Sizing", "rule": "Distribute exposure across different expiries when possible."},
    {"category": "Stop Loss", "rule": "Place technical stops and honour them without exception."},
    {"category": "Stop Loss", "rule": "Incorporate option Greeks for dynamic stop evaluation."},
    {"category": "Stop Loss", "rule": "Use time-based exits for theta decay sensitive trades."},
    {"category": "Stop Loss", "rule": "Respect the 0.5% max loss threshold per position."},
    {"category": "Hedging", "rule": "Use opposing positions to neutralise sudden risk."},
    {"category": "Hedging", "rule": "Consider delta-neutral adjustments when exposure drifts."},
    {"category": "Hedging", "rule": "Deploy VIX hedges or keep cash reserve for adjustments."},
]


IMPORTANT_CONSIDERATIONS: List[Dict[str, str]] = [
    {"category": "Tax Implications", "item": "Options income is treated as business income – maintain books."},
    {"category": "Tax Implications", "item": "Account for applicable slab rates, STT, and transaction costs."},
    {"category": "Common Pitfalls", "item": "Avoid over-leveraging positions."},
    {"category": "Common Pitfalls", "item": "Respect time decay impact when holding long options."},
    {"category": "Common Pitfalls", "item": "Do not trade against the prevailing trend."},
    {"category": "Common Pitfalls", "item": "Keep emotions in check and trade the plan."},
    {"category": "Common Pitfalls", "item": "Hedge around major events instead of ignoring risk."},
    {"category": "Regulatory Compliance", "item": "Adhere to SEBI position limits and broker RMS rules."},
    {"category": "Regulatory Compliance", "item": "Understand margin requirements and documentation needs."},
    {"category": "Tools & Resources", "item": "NSE website for option chain and market data."},
    {"category": "Tools & Resources", "item": "Sensibull/Opstra for strategy analytics and scenario testing."},
    {"category": "Tools & Resources", "item": "Excel/Google Sheets dashboards for tracking and journaling."},
    {"category": "Tools & Resources", "item": "Economic calendar apps for macro event awareness."},
]

