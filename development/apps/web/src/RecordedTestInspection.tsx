import type { RecordedOutcome } from "./types";
import { SourceExcerpt } from "./SourceExcerpt";

type Inspection = NonNullable<RecordedOutcome["inspection"]>;

export function RecordedTestInspection({ inspection }: { inspection: Inspection }) {
  return (
    <section className="test-inspection" aria-labelledby="test-inspection-title">
      <h4 id="test-inspection-title">Why did an incomplete solution pass?</h4>
      <p>The task required two things: change the supplied list and return the remaining tags.</p>
      <SourceExcerpt label="Original task" text={inspection.task_prompt} />
      <div className="inspection-section">
        <h5>The submitted function</h5>
        <p>This excerpt omits the docstring and comments. It retains every executable line.</p>
        <pre className="live-response">{inspection.submitted_code_excerpt}</pre>
        <p>The list comprehension creates a new list. The supplied list keeps its original contents.</p>
      </div>
      <SourceExcerpt label="Original test definitions: both passed" text={inspection.authored_tests} />
      <div className="inspection-section">
        <h5>The missing check</h5>
        <pre className="live-response">{inspection.proposed_assertion}</pre>
        <p>
          This proposed assertion checks the supplied list after the call. The submitted function
          leaves "new" in that list, so this assertion would fail. It was absent from the original
          tests and does not change the recorded result.
        </p>
      </div>
      <details className="inspection-sources">
        <summary>Source record</summary>
        <p>Prompt: <code>{inspection.prompt_ref}</code></p>
        <p>Tests: <code>{inspection.tests_ref}</code></p>
        <p>Recorded response hash: <code>{inspection.response_hash}</code></p>
      </details>
    </section>
  );
}
