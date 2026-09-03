"""Project saved selections and errors into the public demo without rerunning policies."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from socratic_tutor.acquisition_study.canonical_execution import CanonicalRunManifest
from socratic_tutor.acquisition_study.canonical_primary_analysis import (
    CanonicalPrimaryAnalysisReport,
)
from socratic_tutor.acquisition_study.canonical_stream import (
    CanonicalPublicPolicyMetric,
    CanonicalRestrictedEpisode,
)
from socratic_tutor.benchmark.hashing import model_content_hash
from socratic_tutor.contracts.replay import (
    ExperimentSummaryArtifact,
    SelectorExample,
    SelectorMethodExample,
)

POLICIES = {
    "reliability_aware_quantile_bounded": "Proposed reliability rule",
    "uncertainty_only_bounded": "Uncertainty selection",
}


def checked_path(root: Path, name: str, expected_hash: str) -> Path:
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Source path escapes the canonical run")
    with path.open("rb") as source:
        actual = hashlib.file_digest(source, "sha256").hexdigest()
    if actual != expected_hash:
        raise ValueError(f"Source digest mismatch: {name}")
    return path


def export_example(run_root: Path) -> SelectorExample:
    manifest = CanonicalRunManifest.model_validate_json(
        (run_root / "canonical_run_manifest.json").read_bytes()
    )
    if model_content_hash(manifest, exclude={"manifest_hash"}) != manifest.manifest_hash:
        raise ValueError("Canonical manifest hash mismatch")
    restricted = checked_path(run_root, manifest.restricted_file, manifest.restricted_file_sha256)
    public = checked_path(run_root, manifest.public_file, manifest.public_file_sha256)
    # Choose by file position before reading policy performance.
    with restricted.open(encoding="utf-8") as source:
        episode = CanonicalRestrictedEpisode.model_validate_json(next(source))
    if episode.privileged_episode.environment_id != "matched":
        raise ValueError("The declared example is the first saved matched-environment episode")
    report = CanonicalPrimaryAnalysisReport.model_validate_json(
        (run_root / "primary-analysis-v1/canonical_primary_analysis_report.json").read_bytes()
    )
    if model_content_hash(report, exclude={"report_hash"}) != report.report_hash:
        raise ValueError("Primary report hash mismatch")
    if (
        report.canonical_run_manifest_hash != manifest.manifest_hash
        or report.public_stream_sha256 != manifest.public_file_sha256
    ):
        raise ValueError("Primary report belongs to another canonical run")
    metrics: dict[str, CanonicalPublicPolicyMetric] = {}
    with public.open(encoding="utf-8") as source:
        for line in source:
            row = CanonicalPublicPolicyMetric.model_validate_json(line)
            if (
                row.metric.episode_id == episode.policy_episode.episode_id
                and row.metric.environment_id == episode.privileged_episode.environment_id
                and row.metric.policy_id in POLICIES
            ):
                if row.metric.policy_id in metrics:
                    raise ValueError("Duplicate example metric")
                metrics[row.metric.policy_id] = row
                if len(metrics) == len(POLICIES):
                    break
    methods: list[SelectorMethodExample] = []
    for policy_id, label in POLICIES.items():
        row = metrics[policy_id]
        index, decision = next(
            (index, decision)
            for index, decision in enumerate(episode.decisions)
            if decision.policy_id == policy_id
        )
        if (
            row.shared_candidate_hash != episode.shared_candidate_hash
            or row.policy_result_hash != episode.policy_result_hashes[index]
            or row.metric.selected_probe_count != len(decision.selected_case_ids)
            or row.metric.candidate_count != 40
        ):
            raise ValueError("The saved decisions and public metrics do not agree")
        methods.append(
            SelectorMethodExample(
                policy_id=policy_id,
                label=label,
                selected_case_ids=decision.selected_case_ids,
                error_count=row.metric.classification_error_count,
                source_result_hash=row.policy_result_hash,
            )
        )
    comparison = next(
        row
        for row in report.held_out_primary_intervals
        if row.comparator_policy_id == "uncertainty_only_bounded"
    )
    return SelectorExample(
        episode_id=episode.policy_episode.episode_id,
        environment_id=episode.privileged_episode.environment_id,
        selection_rule=(
            "First saved episode in the matched environment. "
            "Chosen by file order, before comparing errors."
        ),
        case_ids=tuple(case.case_id for case in episode.policy_episode.request.candidates),
        methods=tuple(methods),
        aggregate_error_difference=comparison.macro_mean_paired_effect,
        aggregate_interval_lower=comparison.interval_lower,
        aggregate_interval_upper=comparison.interval_upper,
        interval_confidence=comparison.confidence_level,
        source_manifest_hash=manifest.manifest_hash,
        source_report_hash=report.report_hash,
        source_episode_hash=model_content_hash(episode),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-root", type=Path, default=Path("artifacts/acquisition-study/canonical-v1")
    )
    parser.add_argument(
        "--summary", type=Path, default=Path("data/demo/experiment-summary-v1.json")
    )
    args = parser.parse_args()
    summary = ExperimentSummaryArtifact.model_validate_json(args.summary.read_bytes())
    example = export_example(args.run_root)
    updated = ExperimentSummaryArtifact.model_validate(
        {**summary.model_dump(), "selector_example": example}
    )
    args.summary.write_text(updated.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print(f"Exported {example.episode_id} to {args.summary.resolve()}")


if __name__ == "__main__":
    main()
