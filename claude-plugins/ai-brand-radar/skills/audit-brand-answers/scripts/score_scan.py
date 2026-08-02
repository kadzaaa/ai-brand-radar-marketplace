#!/usr/bin/env python3
"""Validate and score an AI Brand Radar scan JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable


VALID_STATUS = {"eligible", "failed", "blocked"}
VALID_CONFIDENCE = {"low", "medium", "high"}
REQUIRED_FIELDS = {
    "id",
    "cluster",
    "prompt",
    "demand_label",
    "demand_evidence",
    "intent_weight",
    "commercial_priority",
    "status",
    "target_brand_mentioned",
    "target_brand_recommended",
    "first_position",
    "brands_mentioned",
    "citations",
    "answer_correct",
    "answer_complete",
    "competitor_substitution",
    "site_content_ready",
    "site_content_readiness_evidence",
    "competitor_content_advantage",
    "competitor_advantage_evidence",
    "stronger_competitor_urls",
    "evidence",
    "gap_types",
    "target_url",
    "recommended_change",
    "recheck_prompt",
    "success_condition",
    "confidence",
}


def load_scan(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Scan file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Scan root must be a JSON object")
    return payload


def validate(scan: dict[str, Any], strict_50: bool) -> list[str]:
    errors: list[str] = []
    scenarios = scan.get("scenarios")
    if not isinstance(scenarios, list):
        return ["scenarios must be an array"]
    if strict_50 and len(scenarios) != 50:
        errors.append(f"strict mode requires exactly 50 scenarios; found {len(scenarios)}")

    ids: set[Any] = set()
    for index, scenario in enumerate(scenarios, start=1):
        label = f"scenario[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = sorted(REQUIRED_FIELDS - scenario.keys())
        if missing:
            errors.append(f"{label} missing fields: {', '.join(missing)}")
        scenario_id = scenario.get("id")
        if scenario_id in ids:
            errors.append(f"{label} has duplicate id {scenario_id!r}")
        ids.add(scenario_id)

        status = scenario.get("status")
        if status not in VALID_STATUS:
            errors.append(f"{label}.status must be one of {sorted(VALID_STATUS)}")
        confidence = scenario.get("confidence")
        if confidence not in VALID_CONFIDENCE:
            errors.append(f"{label}.confidence must be one of {sorted(VALID_CONFIDENCE)}")
        for field in ("intent_weight", "commercial_priority"):
            value = scenario.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                errors.append(f"{label}.{field} must be an integer from 1 to 5")
        for field in (
            "target_brand_mentioned",
            "target_brand_recommended",
            "competitor_substitution",
        ):
            if not isinstance(scenario.get(field), bool):
                errors.append(f"{label}.{field} must be boolean")
        for field in ("answer_correct", "answer_complete"):
            if scenario.get(field) is not None and not isinstance(scenario.get(field), bool):
                errors.append(f"{label}.{field} must be boolean or null")
        for field in ("site_content_ready", "competitor_content_advantage"):
            if scenario.get(field) is not None and not isinstance(scenario.get(field), bool):
                errors.append(f"{label}.{field} must be boolean or null")
        position = scenario.get("first_position")
        if position is not None and (
            not isinstance(position, int) or isinstance(position, bool) or position < 1
        ):
            errors.append(f"{label}.first_position must be a positive integer or null")
        if not isinstance(scenario.get("citations"), list):
            errors.append(f"{label}.citations must be an array")
        if not isinstance(scenario.get("gap_types"), list):
            errors.append(f"{label}.gap_types must be an array")
        if not isinstance(scenario.get("stronger_competitor_urls"), list):
            errors.append(f"{label}.stronger_competitor_urls must be an array")
    return errors


def pct(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return round(100 * numerator / denominator, 1)


def owned_citation(scenario: dict[str, Any]) -> bool:
    return any(citation.get("owned") is True for citation in scenario.get("citations", []))


def canonical_citation(scenario: dict[str, Any]) -> bool:
    return any(
        citation.get("canonical_for_intent") is True
        for citation in scenario.get("citations", [])
    )


def aggregate(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [item for item in scenarios if item["status"] == "eligible"]
    citation_eligible = [item for item in eligible if item.get("citations")]
    correctness = [item for item in eligible if item.get("answer_correct") is not None]
    completeness = [item for item in eligible if item.get("answer_complete") is not None]
    site_readiness = [item for item in eligible if item.get("site_content_ready") is not None]
    competitor_advantage = [
        item for item in eligible if item.get("competitor_content_advantage") is not None
    ]
    positions = [item["first_position"] for item in eligible if item.get("first_position")]
    gaps = [
        item
        for item in eligible
        if item.get("answer_correct") is False or item.get("answer_complete") is False
    ]

    def weighted_rate(
        predicate: Callable[[dict[str, Any]], bool], items: list[dict[str, Any]]
    ) -> float | None:
        total = sum(item["intent_weight"] * item["commercial_priority"] for item in items)
        won = sum(
            item["intent_weight"] * item["commercial_priority"]
            for item in items
            if predicate(item)
        )
        return pct(won, total)

    metrics: dict[str, Any] = {
        "scenario_count": len(scenarios),
        "eligible_count": len(eligible),
        "failed_or_blocked_count": len(scenarios) - len(eligible),
        "answer_presence": {
            "count": sum(item["target_brand_mentioned"] for item in eligible),
            "denominator": len(eligible),
        },
        "recommended_brand_share": {
            "count": sum(item["target_brand_recommended"] for item in eligible),
            "denominator": len(eligible),
        },
        "first_party_citation_coverage": {
            "count": sum(owned_citation(item) for item in citation_eligible),
            "denominator": len(citation_eligible),
        },
        "correct_answer_rate": {
            "count": sum(item["answer_correct"] is True for item in correctness),
            "denominator": len(correctness),
        },
        "complete_answer_rate": {
            "count": sum(item["answer_complete"] is True for item in completeness),
            "denominator": len(completeness),
        },
        "competitor_substitution_rate": {
            "count": sum(item["competitor_substitution"] for item in eligible),
            "denominator": len(eligible),
        },
        "canonical_source_rate": {
            "count": sum(canonical_citation(item) for item in citation_eligible),
            "denominator": len(citation_eligible),
        },
        "website_answer_readiness": {
            "count": sum(item["site_content_ready"] is True for item in site_readiness),
            "denominator": len(site_readiness),
        },
        "competitor_content_advantage_rate": {
            "count": sum(
                item["competitor_content_advantage"] is True
                for item in competitor_advantage
            ),
            "denominator": len(competitor_advantage),
        },
        "answer_gap_count": len(gaps),
        "average_first_position": round(sum(positions) / len(positions), 2) if positions else None,
        "weighted_percentages": {
            "answer_presence": weighted_rate(lambda item: item["target_brand_mentioned"], eligible),
            "recommended_brand_share": weighted_rate(
                lambda item: item["target_brand_recommended"], eligible
            ),
            "first_party_citation_coverage": weighted_rate(owned_citation, citation_eligible),
            "correct_answer_rate": weighted_rate(
                lambda item: item["answer_correct"] is True, correctness
            ),
            "complete_answer_rate": weighted_rate(
                lambda item: item["answer_complete"] is True, completeness
            ),
            "competitor_substitution_rate": weighted_rate(
                lambda item: item["competitor_substitution"], eligible
            ),
            "canonical_source_rate": weighted_rate(canonical_citation, citation_eligible),
            "website_answer_readiness": weighted_rate(
                lambda item: item["site_content_ready"] is True, site_readiness
            ),
            "competitor_content_advantage_rate": weighted_rate(
                lambda item: item["competitor_content_advantage"] is True,
                competitor_advantage,
            ),
        },
    }
    for value in metrics.values():
        if isinstance(value, dict) and "count" in value:
            value["percentage"] = pct(value["count"], value["denominator"])
    return metrics


def cluster_metrics(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for scenario in scenarios:
        groups[scenario["cluster"]].append(scenario)
    return {name: aggregate(items) for name, items in sorted(groups.items())}


def compare(current: dict[str, Any], previous: dict[str, Any]) -> dict[str, Any]:
    current_metrics = aggregate(current["scenarios"])
    previous_metrics = aggregate(previous["scenarios"])
    keys = [
        "answer_presence",
        "recommended_brand_share",
        "first_party_citation_coverage",
        "correct_answer_rate",
        "complete_answer_rate",
        "competitor_substitution_rate",
        "canonical_source_rate",
        "website_answer_readiness",
        "competitor_content_advantage_rate",
    ]
    deltas: dict[str, Any] = {}
    for key in keys:
        now = current_metrics[key]["percentage"]
        before = previous_metrics[key]["percentage"]
        deltas[key] = None if now is None or before is None else round(now - before, 1)
    deltas["answer_gap_count"] = (
        current_metrics["answer_gap_count"] - previous_metrics["answer_gap_count"]
    )
    return deltas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scan", type=Path, help="Completed scan JSON")
    parser.add_argument("--strict-50", action="store_true", help="Require exactly 50 scenarios")
    parser.add_argument("--compare", type=Path, help="Previous scan JSON")
    args = parser.parse_args()

    try:
        scan = load_scan(args.scan)
        errors = validate(scan, args.strict_50)
        previous = None
        if args.compare:
            previous = load_scan(args.compare)
            errors.extend(f"previous: {error}" for error in validate(previous, args.strict_50))
        if errors:
            raise ValueError("\n".join(errors))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    result = {
        "scan_id": scan.get("scan_id"),
        "metrics": aggregate(scan["scenarios"]),
        "clusters": cluster_metrics(scan["scenarios"]),
    }
    if previous is not None:
        result["comparison_deltas_percentage_points"] = compare(scan, previous)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
