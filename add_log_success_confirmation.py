import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_log_success_confirmation.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    edits = []

    # ── 1. Add loggedSuccess state ──────────────────────────────────────────
    old1 = '''  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);'''
    new1 = '''  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [loggedMatchId, setLoggedMatchId] = useState<string | null>(null);'''
    edits.append(('LogMatchScreen - add loggedMatchId state', old1, new1))

    # ── 2. Show a real confirmation instead of closing instantly ───────────
    old2 = '''      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Could not log this match.");
      onLogged(data.matchId);
    } catch (err: any) {
      setSubmitError(err.message || "Could not log this match. Try again.");
    } finally {
      setSubmitting(false);
    }'''
    new2 = '''      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Could not log this match.");
      // Real fix: this used to close silently on success, which reads
      // exactly like nothing happened. Show a real confirmation with the
      // opponent's name instead, and let the person close it themselves
      // once they've actually seen it.
      setLoggedMatchId(data.matchId);
    } catch (err: any) {
      setSubmitError(err.message || "Could not log this match. Try again.");
    } finally {
      setSubmitting(false);
    }'''
    edits.append(('LogMatchScreen - real confirmation instead of silent close', old2, new2))

    # ── 3. Render the confirmation screen when loggedMatchId is set ────────
    old3 = '''      <button onClick={handleSubmit} disabled={!canSubmit} style={{
        width: "100%", padding: "16px", borderRadius: 20, border: "none",
        background: canSubmit ? COLORS.accent : COLORS.card, color: canSubmit ? "#0A0A0A" : COLORS.textSecondary,
        fontSize: 15, fontWeight: 800, cursor: canSubmit ? "pointer" : "not-allowed",
      }}>
        {submitting ? "Logging..." : "Log Match"}
      </button>
    </div>
  );
};'''
    new3 = '''      <button onClick={handleSubmit} disabled={!canSubmit} style={{
        width: "100%", padding: "16px", borderRadius: 20, border: "none",
        background: canSubmit ? COLORS.accent : COLORS.card, color: canSubmit ? "#0A0A0A" : COLORS.textSecondary,
        fontSize: 15, fontWeight: 800, cursor: canSubmit ? "pointer" : "not-allowed",
      }}>
        {submitting ? "Logging..." : "Log Match"}
      </button>
      {loggedMatchId && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.9)", zIndex: 1000, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 24, textAlign: "center" }}>
          <p style={{ color: COLORS.accent, fontSize: 40, margin: "0 0 16px" }}>✓</p>
          <h2 style={{ color: COLORS.white, fontSize: 20, fontWeight: 800, margin: "0 0 10px" }}>Match Logged</h2>
          <p style={{ color: COLORS.textSecondary, fontSize: 14, margin: "0 0 28px", maxWidth: 280 }}>
            Waiting for {residents.find((r) => r.id === opponentId)?.name || "your opponent"} to confirm. It'll count once they do.
          </p>
          <button onClick={() => onLogged(loggedMatchId)} style={{ background: COLORS.accent, color: "#0A0A0A", border: "none", borderRadius: 20, padding: "14px 32px", fontSize: 14, fontWeight: 800, cursor: "pointer" }}>
            Done
          </button>
        </div>
      )}
    </div>
  );
};'''
    edits.append(('LogMatchScreen - render visible confirmation screen', old3, new3))

    # ── 4. Remove the temporary debug banner ────────────────────────────────
    old4 = '''      {showLogScore && (
        <div style={{ position: "fixed", inset: 0, background: COLORS.background, zIndex: 900 }}>
          {/* TEMPORARY - remove once buildingId issue is confirmed */}
          <div style={{ position: "fixed", top: 0, left: 0, right: 0, background: "#FF3B30", color: "#FFFFFF", padding: 12, fontSize: 12, fontFamily: "monospace", zIndex: 9999, wordBreak: "break-all" }}>
            DEBUG - buildingId: {JSON.stringify(profile?.buildingId)} | uid: {JSON.stringify(profile?.uid)}
          </div>
          <LogMatchScreen'''
    new4 = '''      {showLogScore && (
        <div style={{ position: "fixed", inset: 0, background: COLORS.background, zIndex: 900 }}>
          <LogMatchScreen'''
    edits.append(('ActivityDetailView - remove temporary debug banner', old4, new4))

    for label, old, new in edits:
        count = content.count(old)
        if count != 1:
            print(f"ABORTED before writing: '{label}' matched {count} times (expected exactly 1). No changes were made to the file.")
            sys.exit(1)

    for label, old, new in edits:
        content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Applied {len(edits)} edits successfully to {path}")
    for label, _, _ in edits:
        print(f"  - {label}")

if __name__ == '__main__':
    main()
