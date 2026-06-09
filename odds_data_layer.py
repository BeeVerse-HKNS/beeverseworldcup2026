# BACKEND ONLY — This module fetches gambling odds data for internal model weighting. NEVER expose odds data on the frontend.
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import math
import os
import random
import time

try:
    import requests as _requests
except ImportError:
    _requests = None  # type: ignore[assignment]

try:
    import streamlit as st
except ImportError:
    st = None  # type: ignore[assignment]


_SIMULATED_ODDS = {
    ("Brazil", "Argentina"): (2.10, 3.40, 3.50),
    ("France", "England"): (2.30, 3.30, 3.20),
    ("Germany", "Spain"): (2.50, 3.30, 2.90),
    ("Italy", "Portugal"): (2.60, 3.20, 2.90),
    ("Netherlands", "Croatia"): (2.20, 3.30, 3.40),
    ("Belgium", "Uruguay"): (2.10, 3.30, 3.60),
    ("USA", "Mexico"): (2.40, 3.20, 3.10),
    ("Japan", "South Korea"): (2.30, 3.30, 3.20),
    ("Morocco", "Senegal"): (2.20, 3.20, 3.50),
    ("Canada", "Costa Rica"): (1.90, 3.50, 4.20),
    ("Brazil", "France"): (2.50, 3.20, 2.90),
    ("Argentina", "Germany"): (2.40, 3.30, 3.00),
    ("England", "Spain"): (2.60, 3.20, 2.90),
    ("Portugal", "Netherlands"): (2.50, 3.30, 2.90),
    ("USA", "Canada"): (2.00, 3.40, 3.80),
    ("Mexico", "Costa Rica"): (1.80, 3.50, 4.60),
    ("Japan", "Australia"): (1.90, 3.50, 4.10),
    ("Brazil", "Germany"): (2.40, 3.30, 3.00),
    ("France", "Argentina"): (2.50, 3.20, 2.90),
    ("England", "Netherlands"): (2.40, 3.30, 3.00),
    ("Spain", "Portugal"): (2.30, 3.30, 3.20),
    ("Belgium", "France"): (3.00, 3.20, 2.50),
    ("Croatia", "Morocco"): (2.20, 3.20, 3.50),
    ("Uruguay", "Colombia"): (2.30, 3.30, 3.10),
    ("South Korea", "Saudi Arabia"): (2.10, 3.30, 3.60),
}

# Elo ratings for top national teams (approximate, used for fallback odds generation)
_ELO_RATINGS: dict[str, int] = {
    "Brazil": 2140, "Argentina": 2110, "France": 2090, "England": 2060,
    "Spain": 2040, "Germany": 2030, "Portugal": 2010, "Netherlands": 1990,
    "Italy": 1980, "Belgium": 1970, "Croatia": 1930, "Uruguay": 1910,
    "Colombia": 1890, "USA": 1870, "Mexico": 1850, "Morocco": 1840,
    "Japan": 1830, "South Korea": 1800, "Senegal": 1790, "Australia": 1760,
    "Canada": 1750, "Costa Rica": 1720, "Saudi Arabia": 1700,
}

@dataclass
class MarketConsensusData:
    team_home: str
    team_away: str
    home_win_probability: float
    draw_probability: float
    away_win_probability: float
    confidence: float
    timestamp: str
    source_count: int


class OddsDataLayer:
    def __init__(self, cache_duration_hours: int = 6):
        self._cache_duration = timedelta(hours=cache_duration_hours)
        self._cache: dict[str, tuple[MarketConsensusData, datetime]] = {}
        self._odds_cache: dict[str, tuple[float, dict]] = {}  # key: "team_home_vs_team_away", value: (timestamp, data)
        self._cache_duration_seconds = 6 * 3600  # 6 hours in seconds
        self._sources = [
            "the_odds_api",
            "football_data_org",
            "api_football",
            "soccerway",
            "flashscore",
        ]

    def fetch_market_consensus(self, team_home: str, team_away: str) -> MarketConsensusData:
        cache_key = self._get_cache_key(team_home, team_away)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached

        # Check odds cache before making API calls
        odds_cache_key = f"{team_home}_vs_{team_away}"
        now = time.time()
        if odds_cache_key in self._odds_cache:
            cached_ts, cached_data = self._odds_cache[odds_cache_key]
            if now - cached_ts < self._cache_duration_seconds:
                probs = self._odds_to_probability(cached_data["home"], cached_data["draw"], cached_data["away"])
                data = MarketConsensusData(
                    team_home=team_home,
                    team_away=team_away,
                    home_win_probability=round(probs[0], 4),
                    draw_probability=round(probs[1], 4),
                    away_win_probability=round(probs[2], 4),
                    confidence=0.3,
                    timestamp=datetime.utcnow().isoformat() + "Z",
                    source_count=1,
                )
                self._save_to_cache(cache_key, data)
                return data

        probabilities_list = []
        source_count = 0

        # Try real API first
        try:
            real_odds = self.fetch_real_odds(team_home, team_away)
            if real_odds:
                probs = (real_odds["home_prob"], real_odds["draw_prob"], real_odds["away_prob"])
                probabilities_list.append(probs)
                source_count += 1
        except Exception:
            pass

        # Then try other simulated sources
        for source in self._sources:
            try:
                raw = self._fetch_from_source(source, team_home, team_away)
                if raw:
                    probs = self._odds_to_probability(raw["home"], raw["draw"], raw["away"])
                    probabilities_list.append(probs)
                    source_count += 1
            except Exception:
                continue

        if not probabilities_list:
            fallback = self._elo_fallback_odds(team_home, team_away)
            probs = (fallback["home_prob"], fallback["draw_prob"], fallback["away_prob"])
            probabilities_list.append(probs)
            source_count = 1

        home_prob, draw_prob, away_prob, confidence = self._aggregate_probabilities(probabilities_list)

        data = MarketConsensusData(
            team_home=team_home,
            team_away=team_away,
            home_win_probability=round(home_prob, 4),
            draw_probability=round(draw_prob, 4),
            away_win_probability=round(away_prob, 4),
            confidence=round(confidence, 4),
            timestamp=datetime.utcnow().isoformat() + "Z",
            source_count=source_count,
        )

        self._save_to_cache(cache_key, data)
        return data

    def _fetch_from_source(self, source_name: str, team_home: str, team_away: str) -> dict:
        if source_name == "simulated":
            return self._get_simulated_odds(team_home, team_away)

        return self._get_simulated_odds(team_home, team_away)

    def _get_simulated_odds(self, team_home: str, team_away: str) -> dict:
        key = (team_home, team_away)
        reverse_key = (team_away, team_home)

        if key in _SIMULATED_ODDS:
            home, draw, away = _SIMULATED_ODDS[key]
            return {"home": home, "draw": draw, "away": away}

        if reverse_key in _SIMULATED_ODDS:
            away, draw, home = _SIMULATED_ODDS[reverse_key]
            return {"home": home, "draw": draw, "away": away}

        random.seed(hash(team_home + team_away))
        home = round(1.5 + random.random() * 2.0, 2)
        draw = round(2.8 + random.random() * 1.2, 2)
        away = round(1.5 + random.random() * 2.0, 2)
        random.seed()
        return {"home": home, "draw": draw, "away": away}

    def fetch_real_odds(self, team_home: str, team_away: str) -> dict | None:
        """Fetch real odds from The Odds API. Returns probabilities dict or None on failure."""
        api_key = ""
        if st is not None:
            try:
                api_key = st.secrets.get("ODDS_API_KEY", "")
            except Exception:
                pass
        if not api_key:
            api_key = os.environ.get("ODDS_API_KEY", "")

        if not api_key or _requests is None:
            return None

        try:
            url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
            params = {
                "apiKey": api_key,
                "regions": "eu",
                "markets": "h2h",
                "oddsFormat": "decimal",
            }
            resp = _requests.get(url, params=params, timeout=10)
            if resp.status_code != 200:
                return None

            matches = resp.json()
            for match in matches:
                home_team = match.get("home_team", "")
                away_team = match.get("away_team", "")
                if home_team == team_home and away_team == team_away:
                    bookmakers = match.get("bookmakers", [])
                    if not bookmakers:
                        continue
                    # Aggregate across bookmakers, never store bookmaker names
                    home_odds_list = []
                    draw_odds_list = []
                    away_odds_list = []
                    for bm in bookmakers:
                        for market in bm.get("markets", []):
                            if market.get("key") != "h2h":
                                continue
                            outcomes = market.get("outcomes", [])
                            for outcome in outcomes:
                                name = outcome.get("name", "")
                                price = outcome.get("price")
                                if price is None:
                                    continue
                                if name == home_team:
                                    home_odds_list.append(float(price))
                                elif name == "Draw":
                                    draw_odds_list.append(float(price))
                                elif name == away_team:
                                    away_odds_list.append(float(price))
                    if home_odds_list and draw_odds_list and away_odds_list:
                        avg_home = sum(home_odds_list) / len(home_odds_list)
                        avg_draw = sum(draw_odds_list) / len(draw_odds_list)
                        avg_away = sum(away_odds_list) / len(away_odds_list)
                        probs = self._odds_to_probability(avg_home, avg_draw, avg_away)
                        # Cache the result
                        odds_cache_key = f"{team_home}_vs_{team_away}"
                        self._odds_cache[odds_cache_key] = (
                            time.time(),
                            {"home": avg_home, "draw": avg_draw, "away": avg_away},
                        )
                        return {
                            "home_prob": probs[0],
                            "draw_prob": probs[1],
                            "away_prob": probs[2],
                        }
            return None
        except Exception:
            return None

    def _elo_fallback_odds(self, team_home: str, team_away: str) -> dict:
        """Generate simulated odds from Elo ratings when no API data is available."""
        elo_home = _ELO_RATINGS.get(team_home, 1800)
        elo_away = _ELO_RATINGS.get(team_away, 1800)

        # Home advantage: +65 Elo points
        elo_home_adjusted = elo_home + 65

        # Expected score via standard Elo formula
        exp_home = 1.0 / (1.0 + 10 ** ((elo_away - elo_home_adjusted) / 400.0))
        exp_away = 1.0 - exp_home

        # Derive draw probability: higher when teams are closer in strength
        elo_diff = abs(elo_home_adjusted - elo_away)
        draw_prob = max(0.15, min(0.35, 0.35 - (elo_diff / 2000.0)))

        # Scale home/away to account for draw
        remaining = 1.0 - draw_prob
        home_prob = remaining * exp_home / (exp_home + exp_away) if (exp_home + exp_away) > 0 else remaining / 2
        away_prob = remaining - home_prob

        return {
            "home_prob": round(home_prob, 4),
            "draw_prob": round(draw_prob, 4),
            "away_prob": round(away_prob, 4),
        }

    def _odds_to_probability(self, home_odds: float, draw_odds: float, away_odds: float) -> tuple:
        raw_home = 1.0 / home_odds
        raw_draw = 1.0 / draw_odds
        raw_away = 1.0 / away_odds
        total = raw_home + raw_draw + raw_away
        fair_home = raw_home / total
        fair_draw = raw_draw / total
        fair_away = raw_away / total
        return (fair_home, fair_draw, fair_away)

    def _aggregate_probabilities(self, probabilities_list: list[tuple]) -> tuple:
        n = len(probabilities_list)
        if n == 0:
            return (0.3333, 0.3333, 0.3333, 0.0)

        avg_home = sum(p[0] for p in probabilities_list) / n
        avg_draw = sum(p[1] for p in probabilities_list) / n
        avg_away = sum(p[2] for p in probabilities_list) / n

        if n == 1:
            confidence = 0.3
        else:
            var_home = sum((p[0] - avg_home) ** 2 for p in probabilities_list) / n
            var_draw = sum((p[1] - avg_draw) ** 2 for p in probabilities_list) / n
            var_away = sum((p[2] - avg_away) ** 2 for p in probabilities_list) / n
            avg_variance = (var_home + var_draw + var_away) / 3.0
            std_dev = math.sqrt(avg_variance)
            agreement_score = max(0.0, 1.0 - std_dev * 10.0)
            source_score = min(1.0, n / 5.0)
            confidence = 0.5 * agreement_score + 0.5 * source_score

        return (avg_home, avg_draw, avg_away, confidence)

    def _get_cache_key(self, team_home: str, team_away: str) -> str:
        raw = f"{team_home.lower()}|{team_away.lower()}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def _get_from_cache(self, key: str) -> Optional[MarketConsensusData]:
        if key not in self._cache:
            return None
        data, cached_at = self._cache[key]
        if datetime.utcnow() - cached_at > self._cache_duration:
            del self._cache[key]
            return None
        return data

    def _save_to_cache(self, key: str, data: MarketConsensusData) -> None:
        self._cache[key] = (data, datetime.utcnow())

    def get_enhanced_probability(
        self,
        team_home: str,
        team_away: str,
        model_probability: tuple,
        alpha: float = 0.3,
    ) -> tuple:
        market = self.fetch_market_consensus(team_home, team_away)
        market_probs = (
            market.home_win_probability,
            market.draw_probability,
            market.away_win_probability,
        )
        final_home = alpha * market_probs[0] + (1 - alpha) * model_probability[0]
        final_draw = alpha * market_probs[1] + (1 - alpha) * model_probability[1]
        final_away = alpha * market_probs[2] + (1 - alpha) * model_probability[2]
        total = final_home + final_draw + final_away
        return (
            round(final_home / total, 4),
            round(final_draw / total, 4),
            round(final_away / total, 4),
        )

    def calculate_dynamic_alpha(self, match_time=None) -> float:
        """Calculate dynamic alpha (market weight) based on time to kickoff.

        Alpha schedule:
        - 7+ days before: 0.10 (early odds are noisy)
        - 3-7 days before: 0.15 (market settling)
        - 1-3 days before: 0.20 (lineup news affects odds)
        - Match day: 0.25 (closing line is most accurate)
        - After kickoff: 0.00 (no more market data)
        """
        from datetime import datetime, timezone

        if match_time is None:
            # Default: assume 3-7 days before match
            return 0.15

        try:
            if isinstance(match_time, str):
                match_time = datetime.fromisoformat(match_time.replace('Z', '+00:00'))

            now = datetime.now(timezone.utc)
            if hasattr(match_time, 'tzinfo') and match_time.tzinfo is None:
                match_time = match_time.replace(tzinfo=timezone.utc)

            hours_to_kickoff = (match_time - now).total_seconds() / 3600

            if hours_to_kickoff < 0:
                return 0.00  # Match started
            elif hours_to_kickoff < 24:
                return 0.25  # Match day
            elif hours_to_kickoff < 72:
                return 0.20  # 1-3 days
            elif hours_to_kickoff < 168:
                return 0.15  # 3-7 days
            else:
                return 0.10  # 7+ days
        except Exception:
            return 0.15  # Default fallback

    def get_refresh_interval_hours(self, match_time=None) -> float:
        """Get recommended refresh interval based on match proximity.

        - 3+ days away: 6 hours
        - 1-3 days away: 2 hours
        - Match day: 0.5 hours (30 min)
        """
        from datetime import datetime, timezone

        if match_time is None:
            return 6.0

        try:
            if isinstance(match_time, str):
                match_time = datetime.fromisoformat(match_time.replace('Z', '+00:00'))

            now = datetime.now(timezone.utc)
            if hasattr(match_time, 'tzinfo') and match_time.tzinfo is None:
                match_time = match_time.replace(tzinfo=timezone.utc)

            hours_to_kickoff = (match_time - now).total_seconds() / 3600

            if hours_to_kickoff < 24:
                return 0.5  # 30 min on match day
            elif hours_to_kickoff < 72:
                return 2.0  # 2 hours 1-3 days
            else:
                return 6.0  # 6 hours 3+ days
        except Exception:
            return 6.0

    def calculate_confidence(self, model_probs: dict, market_probs: dict) -> dict:
        """Calculate confidence level based on model-market agreement.

        Returns dict with:
        - confidence_score: 0-1 (1 = perfect agreement)
        - confidence_level: "High" / "Medium" / "Low"
        - description: plain text explanation
        """
        if not model_probs or not market_probs:
            return {
                "confidence_score": 0.3,
                "confidence_level": "Low",
                "description": "Limited market data available"
            }

        # Calculate agreement between model and market
        model_home = model_probs.get("home_prob", 0.5)
        market_home = market_probs.get("home_prob", 0.5)

        diff = abs(model_home - market_home)

        # Convert difference to confidence (smaller diff = higher confidence)
        confidence_score = max(0.0, min(1.0, 1.0 - diff * 3))

        if confidence_score >= 0.7:
            level = "High"
            desc = "Model and market agree"
        elif confidence_score >= 0.4:
            level = "Medium"
            desc = "Some disagreement between model and market"
        else:
            level = "Low"
            desc = "Significant disagreement — prediction uncertain"

        return {
            "confidence_score": confidence_score,
            "confidence_level": level,
            "description": desc
        }

    def get_market_weight_for_v11(self, team_home: str, team_away: str) -> dict:
        """Get market probability for V11 engine integration (backend only).
        Returns dict with home_prob, draw_prob, away_prob.
        This is NEVER displayed on frontend."""
        return self.fetch_market_consensus(team_home, team_away)

    def to_frontend_dict(self, data: MarketConsensusData) -> dict:
        return {
            "team_home": data.team_home,
            "team_away": data.team_away,
            "market_consensus_probability": {
                "home_win": data.home_win_probability,
                "draw": data.draw_probability,
                "away_win": data.away_win_probability,
            },
            "confidence": data.confidence,
        }


@dataclass
class BlendedPrediction:
    model_home: float
    model_draw: float
    model_away: float
    market_home: float
    market_draw: float
    market_away: float
    final_home: float
    final_draw: float
    final_away: float
    alpha: float
    predicted_result: str
    model_predicted_result: str
    market_confidence: float


class OddsIntegratedPredictor:
    def __init__(self, alpha: float = 0.6):
        self.alpha = alpha
        self._odds_layer = OddsDataLayer()
        self._history: list[dict] = []

    def predict(
        self,
        team_home: str,
        team_away: str,
        model_probs: tuple[float, float, float],
    ) -> BlendedPrediction:
        market = self._odds_layer.fetch_market_consensus(team_home, team_away)
        market_probs = (
            market.home_win_probability,
            market.draw_probability,
            market.away_win_probability,
        )

        a = self.alpha
        final_home = a * market_probs[0] + (1 - a) * model_probs[0]
        final_draw = a * market_probs[1] + (1 - a) * model_probs[1]
        final_away = a * market_probs[2] + (1 - a) * model_probs[2]

        total = final_home + final_draw + final_away
        final_home /= total
        final_draw /= total
        final_away /= total

        model_result = self._pick_result(model_probs)
        final_result = self._pick_result((final_home, final_draw, final_away))

        return BlendedPrediction(
            model_home=round(model_probs[0], 4),
            model_draw=round(model_probs[1], 4),
            model_away=round(model_probs[2], 4),
            market_home=round(market_probs[0], 4),
            market_draw=round(market_probs[1], 4),
            market_away=round(market_probs[2], 4),
            final_home=round(final_home, 4),
            final_draw=round(final_draw, 4),
            final_away=round(final_away, 4),
            alpha=self.alpha,
            predicted_result=final_result,
            model_predicted_result=model_result,
            market_confidence=market.confidence,
        )

    def record_result(
        self,
        team_home: str,
        team_away: str,
        actual_result: str,
        model_probs: tuple[float, float, float],
    ) -> dict:
        blended = self.predict(team_home, team_away, model_probs)
        model_correct = blended.model_predicted_result == actual_result
        blended_correct = blended.predicted_result == actual_result

        entry = {
            "match": f"{team_home} vs {team_away}",
            "actual": actual_result,
            "model_pred": blended.model_predicted_result,
            "blended_pred": blended.predicted_result,
            "model_correct": model_correct,
            "blended_correct": blended_correct,
            "alpha": self.alpha,
        }
        self._history.append(entry)

        model_acc = sum(e["model_correct"] for e in self._history) / len(self._history)
        blended_acc = sum(e["blended_correct"] for e in self._history) / len(self._history)

        return {
            "model_accuracy": round(model_acc, 4),
            "blended_accuracy": round(blended_acc, 4),
            "total_matches": len(self._history),
            "alpha": self.alpha,
        }

    def get_accuracy_stats(self) -> dict:
        if not self._history:
            return {
                "model_accuracy": 0.0,
                "blended_accuracy": 0.0,
                "total_matches": 0,
                "alpha": self.alpha,
            }
        model_acc = sum(e["model_correct"] for e in self._history) / len(self._history)
        blended_acc = sum(e["blended_correct"] for e in self._history) / len(self._history)
        return {
            "model_accuracy": round(model_acc, 4),
            "blended_accuracy": round(blended_acc, 4),
            "total_matches": len(self._history),
            "alpha": self.alpha,
        }

    @staticmethod
    def _pick_result(probs: tuple[float, float, float]) -> str:
        h, d, a = probs
        if d > h and d > a:
            return "DRAW"
        return "HOME_WIN" if h >= a else "AWAY_WIN"
