import { useState } from "react";

import { SourceExcerpt } from "./SourceExcerpt";
import type { SelectorExample } from "./types";

export function SelectorComparison({ example }: { example: SelectorExample }) {
  const [revealed, setRevealed] = useState(false);
  return (
    <section className="replay-panel selector-panel" aria-labelledby="selector-title">
      <div className="experiment-section-heading">
        <div>
          <span>Saved simulation episode</span>
          <h3 id="selector-title">Which 20 of these 40 cases received a check?</h3>
        </div>
        <span className="record-status">Recorded selections</span>
      </div>
      <p>{example.selection_rule}</p>
      <p>Both methods faced the same cases and selected their checks before seeing the results.</p>
      <div className="selection-legend">
        <span><span className="selected-swatch" /> Selected</span>
        <span><span className="unselected-swatch" /> Not selected</span>
      </div>
      <div className="selector-methods">
        {example.methods.map((method) => (
          <section key={method.policy_id} aria-label={method.label}>
            <h4>{method.label}</h4>
            <p>{method.selected_case_ids.length} checks selected</p>
            <ol className="selection-grid" aria-label={`${method.label} selections`}>
              {example.case_ids.map((caseId, index) => {
                const selected = method.selected_case_ids.includes(caseId);
                return (
                  <li
                    key={caseId}
                    className={selected ? "case-selected" : "case-unselected"}
                    title={`${caseId}: ${selected ? "selected" : "not selected"}`}
                    aria-label={`Case ${index + 1}: ${selected ? "selected" : "not selected"}`}
                  >
                    {index + 1}{selected && <span aria-hidden="true"> ✓</span>}
                  </li>
                );
              })}
            </ol>
            {revealed && <p className="finding-result">{method.error_count} prediction errors out of 40</p>}
          </section>
        ))}
      </div>
      {!revealed && (
        <button type="button" className="primary-button" onClick={() => setRevealed(true)}>
          Reveal saved error counts
        </button>
      )}
      <section className="selector-aggregate" aria-labelledby="aggregate-selector-title">
        <h4 id="aggregate-selector-title">The full study matters more than this one round</h4>
        <p>
          Across six held-out environments, the proposed rule produced an average of{" "}
          {(example.aggregate_error_difference * 100).toFixed(3)} percentage points more errors
          than uncertainty selection at the same 50% budget.
        </p>
        <p>
          The {(example.interval_confidence * 100).toFixed(2)}% interval was{" "}
          {(example.aggregate_interval_lower * 100).toFixed(3)} to{" "}
          {(example.aggregate_interval_upper * 100).toFixed(3)} percentage points.
          The comparisons used 2,000 episodes per environment.
        </p>
        <p>
          The proposed score is a heuristic. It can assign value to a check even when either
          result leaves the classification unchanged. It does not generally equal expected error reduction.
        </p>
      </section>
      <p className="claim-boundary">
        This display replays saved selections and total errors. It does not run a policy or measure student learning.
      </p>
      <SourceExcerpt label="Episode and source records" text={
        `${example.environment_id} / ${example.episode_id}\nEpisode: ${example.source_episode_hash}\nRun: ${example.source_manifest_hash}\nAnalysis: ${example.source_report_hash}`
      } />
    </section>
  );
}
