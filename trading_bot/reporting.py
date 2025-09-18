"""Spreadsheet reporting utilities for the trading bot."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from . import strategies, workflow


def _to_dataframe(data: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Utility helper that safely converts a list of dictionaries into a DataFrame."""

    if not data:
        return pd.DataFrame(columns=columns)
    df = pd.DataFrame(data)
    if columns:
        missing_cols = [col for col in columns if col not in df.columns]
        for col in missing_cols:
            df[col] = ""
        return df[columns]
    return df


class SpreadsheetReporter:
    """Exports trading session artefacts to Excel/Google Sheets."""

    def __init__(self, output_path: str = "trading_bot_report.xlsx", google_sheet_id: Optional[str] = None):
        self.output_path = Path(output_path)
        self.google_sheet_id = google_sheet_id

    # ------------------------------------------------------------------
    # Data preparation helpers
    # ------------------------------------------------------------------
    def _analysis_summary(self, analysis_report: Dict[str, Any], market_view: str) -> pd.DataFrame:
        summary = {
            "Timestamp": analysis_report.get("timestamp"),
            "Market View": market_view,
            "Spot Price": analysis_report.get("spot_price"),
            "Future Price": analysis_report.get("future_price"),
            "Spot-Future Diff (pts)": analysis_report.get("spot_future_diff_pts"),
            "India VIX": analysis_report.get("india_vix"),
            "IV Percentile": analysis_report.get("ivp"),
            "Put/Call Ratio": analysis_report.get("pcr"),
            "Max Pain": analysis_report.get("max_pain"),
            "OI Buildup": analysis_report.get("buildup"),
        }
        return pd.DataFrame([summary])

    def _participant_table(self, analysis_report: Dict[str, Any]) -> pd.DataFrame:
        participant_data = analysis_report.get("participant_data", {}) or {}
        if not participant_data:
            return pd.DataFrame(columns=["Participant"])
        df = pd.DataFrame(participant_data).T.reset_index().rename(columns={"index": "Participant"})
        return df

    def _option_chain(self, analysis_report: Dict[str, Any]) -> pd.DataFrame:
        chain = analysis_report.get("raw_option_chain")
        if isinstance(chain, pd.DataFrame):
            return chain.copy().sort_values(["type", "strike"]).reset_index(drop=True)
        return pd.DataFrame()

    def _strategies_for_view(
        self,
        market_view: str,
        chosen_strategy: Optional[str],
    ) -> pd.DataFrame:
        records: List[Dict[str, Any]] = []
        for strat in strategies.get_strategies_by_view(market_view):
            row = strat.to_record()
            row["Chosen"] = "Yes" if chosen_strategy and strat.name == chosen_strategy else ""
            records.append(row)
        return _to_dataframe(records)

    def _strategy_catalog(self) -> pd.DataFrame:
        records = [strat.to_record() for strat in strategies.ALL_STRATEGIES.values()]
        return _to_dataframe(records)

    def _trade_log(self, portfolio) -> pd.DataFrame:
        log_records: List[Dict[str, Any]] = []
        for entry in getattr(portfolio, "trade_log", []):
            record = entry.copy()
            timestamp = record.get("timestamp")
            if isinstance(timestamp, pd.Timestamp):
                record["timestamp"] = timestamp.to_pydatetime()
            log_records.append(record)
        df = _to_dataframe(log_records)
        if not df.empty:
            df.rename(columns=str.title, inplace=True)
        return df

    def _risk_snapshot(self, portfolio) -> pd.DataFrame:
        snapshot = {}
        if hasattr(portfolio, "get_risk_snapshot"):
            snapshot = portfolio.get_risk_snapshot()
        else:
            snapshot = {
                "initial_capital": getattr(portfolio, "initial_capital", None),
                "cash_on_hand": getattr(portfolio, "cash", None),
                "daily_pnl": getattr(portfolio, "daily_pnl", None),
            }
            snapshot["profit_target"] = snapshot.get("initial_capital", 0) * 0.01
            snapshot["stop_loss"] = -snapshot.get("initial_capital", 0) * 0.005

        formatted = [
            {"Metric": "Initial Capital", "Value": snapshot.get("initial_capital")},
            {"Metric": "Cash on Hand", "Value": snapshot.get("cash_on_hand")},
            {"Metric": "Daily PnL", "Value": snapshot.get("daily_pnl")},
            {"Metric": "Daily Profit Target", "Value": snapshot.get("profit_target")},
            {"Metric": "Daily Stop Loss", "Value": snapshot.get("stop_loss")},
            {"Metric": "Trading Halted", "Value": snapshot.get("day_over")},
        ]
        return _to_dataframe(formatted)

    def _workflow_tables(self) -> Dict[str, pd.DataFrame]:
        workflow_df = _to_dataframe(workflow.WORKFLOW_PHASES, columns=["phase", "category", "task"])
        workflow_df.rename(columns={"phase": "Phase", "category": "Category", "task": "Task"}, inplace=True)

        trading_params_df = _to_dataframe(workflow.TRADING_PARAMETERS, columns=["parameter", "details"])
        trading_params_df.rename(columns={"parameter": "Parameter", "details": "Details"}, inplace=True)

        risk_rules_df = _to_dataframe(workflow.RISK_MANAGEMENT_RULES, columns=["category", "rule"])
        risk_rules_df.rename(columns={"category": "Category", "rule": "Rule"}, inplace=True)

        considerations_df = _to_dataframe(workflow.IMPORTANT_CONSIDERATIONS, columns=["category", "item"])
        considerations_df.rename(columns={"category": "Category", "item": "Item"}, inplace=True)

        return {
            "Workflow_Checklist": workflow_df,
            "Trading_Parameters": trading_params_df,
            "Risk_Management_Rules": risk_rules_df,
            "Important_Considerations": considerations_df,
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def build_tables(
        self,
        analysis_report: Dict[str, Any],
        market_view: str,
        portfolio,
        chosen_strategy: Optional[str] = None,
    ) -> Dict[str, pd.DataFrame]:
        tables: Dict[str, pd.DataFrame] = {}

        tables["Market_Analysis"] = self._analysis_summary(analysis_report, market_view)

        participants = self._participant_table(analysis_report)
        if not participants.empty:
            tables["Participant_Positioning"] = participants

        option_chain = self._option_chain(analysis_report)
        if not option_chain.empty:
            tables["Option_Chain"] = option_chain

        tables["Strategy_Selection"] = self._strategies_for_view(market_view, chosen_strategy)
        tables["Strategy_Catalog"] = self._strategy_catalog()
        tables["Trade_Log"] = self._trade_log(portfolio)
        tables["Risk_Snapshot"] = self._risk_snapshot(portfolio)

        tables.update(self._workflow_tables())

        return tables

    def export_to_excel(self, tables: Dict[str, pd.DataFrame]) -> Path:
        """Writes the provided tables into an Excel workbook.

        Falls back to CSV exports when neither ``xlsxwriter`` nor
        ``openpyxl`` is available in the environment.  The fallback keeps
        the automation usable inside restricted sandboxes while guiding
        users to install the recommended Excel engines for richer output.
        """

        engine = None
        for candidate in ("xlsxwriter", "openpyxl"):
            if importlib.util.find_spec(candidate):
                engine = candidate
                break

        if engine:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            with pd.ExcelWriter(self.output_path, engine=engine) as writer:
                for sheet_name, df in tables.items():
                    safe_name = sheet_name[:31]  # Excel sheet name limit
                    df.to_excel(writer, sheet_name=safe_name, index=False)
            return self.output_path

        # Fallback: export each sheet as an individual CSV file
        fallback_dir = self.output_path.with_suffix("")
        if fallback_dir.suffix:
            fallback_dir = Path(str(self.output_path).replace(self.output_path.suffix, ""))
        fallback_dir.mkdir(parents=True, exist_ok=True)

        for sheet_name, df in tables.items():
            csv_path = fallback_dir / f"{sheet_name}.csv"
            df.to_csv(csv_path, index=False)

        print(
            "Excel writer engines not available. Exported CSV bundle instead at "
            f"{fallback_dir.resolve()}. Install 'xlsxwriter' or 'openpyxl' for native Excel output."
        )
        return fallback_dir

    def export_to_google_sheet(self, tables: Dict[str, pd.DataFrame]) -> Optional[str]:
        """Attempts to export the tables to Google Sheets using gspread.

        The method is optional.  It gracefully warns if gspread or the
        required Google credentials are not available.  Users can supply a
        service-account JSON and share the sheet with the service account
        email to make this work.
        """

        if not self.google_sheet_id:
            return None

        try:
            import gspread
            from google.oauth2.service_account import Credentials
        except ImportError:
            print("gspread/google-auth not installed. Skipping Google Sheets export.")
            return None

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        credentials_path = Path("google_service_account.json")
        if not credentials_path.exists():
            print("Service account credentials 'google_service_account.json' not found. Skipping Google Sheets export.")
            return None

        creds = Credentials.from_service_account_file(str(credentials_path), scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(self.google_sheet_id)

        for sheet_name, df in tables.items():
            safe_name = sheet_name[:99]  # Google Sheets allows longer names
            try:
                worksheet = sheet.worksheet(safe_name)
                sheet.del_worksheet(worksheet)
            except gspread.exceptions.WorksheetNotFound:
                pass
            worksheet = sheet.add_worksheet(title=safe_name, rows=str(len(df) + 10), cols=str(len(df.columns) + 5))
            if df.empty:
                continue
            worksheet.update([df.columns.values.tolist()] + df.fillna("").astype(str).values.tolist())

        return self.google_sheet_id

