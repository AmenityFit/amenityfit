import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_match_game_integration.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    edits = []

    # Note: heartRateAvg removal from the backend logMatchGame function
    # lives in ~/alerts/index.js, a separate file - run
    # fix_backend_heart_rate.py against that file instead. Everything
    # below is frontend-only, real edits against App.tsx.

    # ── 1. Remove heart rate from MatchGameCard's props/signature ──────────
    old1 = '''  myScore,
  opponentScore,
  heartRateAvg,
  caloriesBurned,
  confirmed,
  onClose,
}: {
  sport: "basketball" | "padel" | "soccer";
  myName: string;
  opponentName: string;
  myAvatar?: string | null;
  opponentAvatar?: string | null;
  myScore: number;
  opponentScore: number;
  heartRateAvg?: number | null;
  caloriesBurned?: number | null;'''
    new1 = '''  myScore,
  opponentScore,
  caloriesBurned,
  confirmed,
  onClose,
}: {
  sport: "basketball" | "padel" | "soccer";
  myName: string;
  opponentName: string;
  myAvatar?: string | null;
  opponentAvatar?: string | null;
  myScore: number;
  opponentScore: number;
  caloriesBurned?: number | null;'''
    edits.append(('MatchGameCard - remove heartRateAvg from props', old1, new1))

    old2 = '''        {(heartRateAvg || caloriesBurned) && (
          <div style={{ padding: "16px 24px 8px", display: "grid", gridTemplateColumns: heartRateAvg && caloriesBurned ? "1fr 1fr" : "1fr", gap: 14 }}>
            {heartRateAvg && (
              <div style={{ background: `${COLORS.white}08`, borderRadius: 14, padding: "12px 8px", textAlign: "center" }}>
                <p style={{ color: COLORS.textSecondary, fontSize: 9, fontWeight: 700, letterSpacing: 0.8, textTransform: "uppercase", margin: "0 0 4px" }}>Avg Heart Rate</p>
                <p style={{ color: COLORS.white, fontSize: 17, fontWeight: 800, margin: 0 }}>{heartRateAvg} bpm</p>
              </div>
            )}
            {caloriesBurned && (''' 
    new2 = '''        {caloriesBurned && (
          <div style={{ padding: "16px 24px 8px", display: "grid", gridTemplateColumns: "1fr", gap: 14 }}>
            {caloriesBurned && ('''
    edits.append(('MatchGameCard - remove heart rate stat box', old2, new2))

    # ── 2. Remove heart rate from PendingMatchConfirm's card render ────────
    old5 = '''          caloriesBurned={confirmedResult.caloriesBurned}
          heartRateAvg={confirmedResult.heartRateAvg}'''
    new5 = '''          caloriesBurned={confirmedResult.caloriesBurned}'''
    count5 = content.count(old5)
    if count5 == 0:
        # Order may differ - try the swapped variant.
        old5b = '''          heartRateAvg={confirmedResult.heartRateAvg}
          caloriesBurned={confirmedResult.caloriesBurned}'''
        new5b = '''          caloriesBurned={confirmedResult.caloriesBurned}'''
        edits.append(('PendingMatchConfirm - remove heartRateAvg prop', old5b, new5b))
    else:
        edits.append(('PendingMatchConfirm - remove heartRateAvg prop', old5, new5))

    # ── 3. Remove the standalone floating "+" button and its wiring ────────
    old6 = '''            {/* Checks for any match logged against the current user that
                still needs their confirmation - this is what makes the
                head-to-head record trustworthy, so it runs automatically
                every time the dashboard is visited rather than needing to
                be found manually. */}
            {screen === "dashboard" && userProfile?.uid && (
              <PendingMatchConfirm currentUid={userProfile.uid} onDismiss={() => {}} />
            )}
            {screen === "dashboard" && (
              <button
                onClick={() => setScreen("log-match")}
                style={{
                  position: "fixed", bottom: 90, right: 20, zIndex: 500,
                  width: 56, height: 56, borderRadius: 28, border: "none",
                  background: COLORS.accent, color: "#0A0A0A", fontSize: 24, fontWeight: 900,
                  cursor: "pointer", boxShadow: "0 8px 24px rgba(0,0,0,0.4)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                }}
                aria-label="Log a match"
              >
                +
              </button>
            )}'''
    new6 = '''            {/* Checks for any match logged against the current user that
                still needs their confirmation - this is what makes the
                head-to-head record trustworthy, so it runs automatically
                every time the dashboard is visited rather than needing to
                be found manually. The real entry point for LOGGING a
                match lives in ActivityDetailView instead (a "Log Score"
                button alongside Share/Sticker, shown only for
                basketball/soccer/padel sessions) - not a separate
                floating button, since basketball/soccer/padel already
                flow through the real Track an Activity system. */}
            {screen === "dashboard" && userProfile?.uid && (
              <PendingMatchConfirm currentUid={userProfile.uid} onDismiss={() => {}} />
            )}'''
    edits.append(('Remove standalone floating Log Match button', old6, new6))

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
