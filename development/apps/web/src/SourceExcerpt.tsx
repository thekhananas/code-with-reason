type SourceExcerptProps = {
  label: string;
  text?: string | null;
};

export function SourceExcerpt({ label, text }: SourceExcerptProps) {
  if (!text) return null;
  return (
    <details className="source-excerpt">
      <summary>{label}</summary>
      <pre className="live-response">{text}</pre>
    </details>
  );
}
