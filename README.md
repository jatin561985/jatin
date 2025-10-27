# Short Straddle Trading Bot

This project is a production-ready Python application that implements, backtests, and runs a short straddle workflow for NIFTY and SENSEX weekly indices.

## Project Structure

```
├─ README.md
├─ requirements.txt
├─ .env.example
├─ config/
│ ├─ base.yaml
│ ├─ nifty_tuesday.yaml
│ └─ sensex_thursday.yaml
├─ data/
├─ src/
│ ├─ cfg/
│ ├─ data/
│ ├─ features/
│ ├─ strategy/
│ ├─ costs/
│ ├─ risk/
│ ├─ broker/
│ ├─ backtest/
│ ├─ exec/
│ ├─ reporting/
│ └─ utils/
├─ scripts/
│ ├─ run_backtest.py
│ ├─ run_live_paper.py
│ └─ run_live_trade.py
└─ tests/
```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure your environment variables:**
    - Copy the `.env.example` file to `.env`.
    - Fill in your Zerodha Kite Connect API key, secret, and access token in the `.env` file.

## Configuration

The application is configured through YAML files in the `config/` directory.

-   `base.yaml`: Contains global settings like account capital and risk parameters.
-   `nifty_tuesday.yaml` / `sensex_thursday.yaml`: Contain strategy-specific parameters for each underlying.

## Usage

### Running the Backtester

To run a backtest, use the `run_backtest.py` script:

```bash
python3 scripts/run_backtest.py --config-path config/nifty_tuesday.yaml --data-path data/nifty_ticks.csv
```

The backtest results, including an equity curve plot, will be saved to the `data/` directory.

### Running in Live Paper Trading Mode

To run the bot in a simulated live environment, use the `run_live_paper.py` script:

```bash
python3 scripts/run_live_paper.py --config-path config/nifty_tuesday.yaml
```

### Running in Live Trading Mode

To run the bot with a real Zerodha account, use the `run_live_trade.py` script:

```bash
python3 scripts/run_live_trade.py --config-path config/nifty_tuesday.yaml
```

**Note:** The live trading script is currently a placeholder and not yet fully implemented.

## Running Tests

To run the unit tests, use `pytest`:

```bash
pytest
```
