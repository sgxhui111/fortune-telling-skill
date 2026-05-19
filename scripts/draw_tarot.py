#!/usr/bin/env python3
"""Draw tarot cards for an entertainment-oriented reading."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from datetime import datetime, timezone


MAJOR = [
    ("The Fool", ["beginning", "risk", "trust"]),
    ("The Magician", ["agency", "tools", "skill"]),
    ("The High Priestess", ["intuition", "hidden knowledge", "silence"]),
    ("The Empress", ["care", "abundance", "embodiment"]),
    ("The Emperor", ["structure", "authority", "boundaries"]),
    ("The Hierophant", ["tradition", "learning", "institution"]),
    ("The Lovers", ["choice", "values", "union"]),
    ("The Chariot", ["direction", "will", "control"]),
    ("Strength", ["courage", "patience", "inner power"]),
    ("The Hermit", ["solitude", "study", "inner light"]),
    ("Wheel of Fortune", ["cycle", "turning point", "timing"]),
    ("Justice", ["truth", "balance", "consequence"]),
    ("The Hanged Man", ["pause", "surrender", "new perspective"]),
    ("Death", ["ending", "transition", "clearing"]),
    ("Temperance", ["integration", "moderation", "rhythm"]),
    ("The Devil", ["attachment", "temptation", "shadow"]),
    ("The Tower", ["disruption", "revelation", "release"]),
    ("The Star", ["hope", "renewal", "guidance"]),
    ("The Moon", ["uncertainty", "dream", "projection"]),
    ("The Sun", ["clarity", "joy", "vitality"]),
    ("Judgement", ["calling", "review", "awakening"]),
    ("The World", ["completion", "wholeness", "integration"]),
]

SUITS = {
    "Wands": ["action", "desire", "creativity", "momentum"],
    "Cups": ["emotion", "intimacy", "intuition", "belonging"],
    "Swords": ["thought", "language", "conflict", "decision"],
    "Pentacles": ["money", "body", "work", "stability"],
}

MINORS = [
    ("Ace", ["seed", "opening", "gift"]),
    ("Two", ["choice", "duality", "exchange"]),
    ("Three", ["growth", "collaboration", "first result"]),
    ("Four", ["stability", "pause", "container"]),
    ("Five", ["friction", "change", "challenge"]),
    ("Six", ["support", "movement", "repair"]),
    ("Seven", ["test", "strategy", "persistence"]),
    ("Eight", ["practice", "speed", "adjustment"]),
    ("Nine", ["ripening", "self-reliance", "threshold"]),
    ("Ten", ["completion", "burden", "overflow"]),
    ("Page", ["message", "beginner mind", "curiosity"]),
    ("Knight", ["pursuit", "movement", "intensity"]),
    ("Queen", ["receptivity", "maturity", "care"]),
    ("King", ["mastery", "responsibility", "direction"]),
]

SPREADS = {
    "single": ["Theme"],
    "three-card": ["Past / root", "Present / challenge", "Near future / advice"],
    "mind-heart-action": ["Mind", "Heart", "Action"],
    "relationship": ["You", "Other person", "Relationship dynamic"],
    "crossroads": ["Current position", "Path A", "Path B", "Hidden influence", "Advice"],
    "celtic-cross": [
        "Present",
        "Crossing challenge",
        "Root",
        "Recent past",
        "Possible direction",
        "Near future",
        "Self",
        "Environment",
        "Hope or fear",
        "Outcome tendency",
    ],
}


def build_deck() -> list[dict[str, object]]:
    deck: list[dict[str, object]] = []
    for name, keywords in MAJOR:
        deck.append({"name": name, "arcana": "Major", "keywords": keywords})
    for suit, suit_keywords in SUITS.items():
        for rank, rank_keywords in MINORS:
            deck.append(
                {
                    "name": f"{rank} of {suit}",
                    "arcana": "Minor",
                    "suit": suit,
                    "keywords": rank_keywords + suit_keywords[:2],
                }
            )
    return deck


def stable_seed(question: str, seed: str | None) -> str:
    if seed:
        return seed
    if question:
        return hashlib.sha256(question.encode("utf-8")).hexdigest()
    return datetime.now(timezone.utc).isoformat()


def draw(spread: str, question: str, seed: str | None, reversed_cards: bool) -> dict[str, object]:
    if spread not in SPREADS:
        raise SystemExit(f"Unknown spread '{spread}'. Choose one of: {', '.join(SPREADS)}")
    rng = random.Random(stable_seed(question, seed))
    deck = build_deck()
    rng.shuffle(deck)
    cards = []
    for position, card in zip(SPREADS[spread], deck):
        orientation = "reversed" if reversed_cards and rng.random() < 0.38 else "upright"
        cards.append({"position": position, "orientation": orientation, **card})
    return {
        "question": question,
        "spread": spread,
        "seed": seed,
        "cards": cards,
        "note": "For entertainment and reflection; not a deterministic prediction.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw tarot cards as JSON.")
    parser.add_argument("--spread", default="three-card", choices=sorted(SPREADS))
    parser.add_argument("--question", default="")
    parser.add_argument("--seed", default=None)
    parser.add_argument("--no-reversed", action="store_true")
    args = parser.parse_args()

    result = draw(args.spread, args.question, args.seed, not args.no_reversed)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
