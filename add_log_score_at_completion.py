import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_log_score_at_completion.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    edits = []

    # ── 1. Add showLogScore state, anchored uniquely to CardioTrackingScreen ──
    old1 = '''  const [showShareCard, setShowShareCard] = useState(false);
  const [showStickerMode, setShowStickerMode] = useState(false);
  // Progressive stats reveal on the live tracking screen: starts minimal'''
    new1 = '''  const [showShareCard, setShowShareCard] = useState(false);
  const [showStickerMode, setShowStickerMode] = useState(false);
  const [showLogScore, setShowLogScore] = useState(false);
  // Progressive stats reveal on the live tracking screen: starts minimal'''
    edits.append(('CardioTrackingScreen - add showLogScore state', old1, new1))

    # ── 2. Add the real Log Score button + LogMatchScreen render, right at
    # completion, alongside Share/Sticker - the actual natural moment. ──────
    old2 = '''        <div style={{ padding: "0 24px 40px", marginTop: "auto", display: "flex", flexDirection: "column", gap: 12 }}>
          <div style={{ display: "flex", gap: 12 }}>
            <button onClick={() => setShowShareCard(true)} style={{ flex: 1, padding: "16px", borderRadius: 16, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 15, fontWeight: 700, cursor: "pointer" }}>
              Share
            </button>
            <button onClick={() => setShowStickerMode(true)} style={{ flex: 1, padding: "16px", borderRadius: 16, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 15, fontWeight: 700, cursor: "pointer" }}>
              Sticker'''
    new2 = '''        <div style={{ padding: "0 24px 40px", marginTop: "auto", display: "flex", flexDirection: "column", gap: 12 }}>
          {/* Log Score - the real entry point, right at the actual moment
              an activity finishes, not buried later in history. Only for
              basketball/soccer/padel (not pickleball - not in scope). */}
          {(activityMeta?.courtType === "basketball" || activityMeta?.courtType === "soccer" || activityMeta?.courtType === "padel") && (
            <button onClick={() => setShowLogScore(true)} style={{ width: "100%", padding: "16px", borderRadius: 16, border: "none", background: COLORS.accent, color: "#0A0A0A", fontSize: 15, fontWeight: 800, cursor: "pointer" }}>
              Log Score
            </button>
          )}
          <div style={{ display: "flex", gap: 12 }}>
            <button onClick={() => setShowShareCard(true)} style={{ flex: 1, padding: "16px", borderRadius: 16, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 15, fontWeight: 700, cursor: "pointer" }}>
              Share
            </button>
            <button onClick={() => setShowStickerMode(true)} style={{ flex: 1, padding: "16px", borderRadius: 16, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 15, fontWeight: 700, cursor: "pointer" }}>
              Sticker'''
    edits.append(('CardioTrackingScreen - add Log Score button', old2, new2))

    old3 = '''        {showStickerMode && (
          <StickerShareScreen'''
    new3 = '''        {showLogScore && (
          <div style={{ position: "fixed", inset: 0, background: COLORS.background, zIndex: 900 }}>
            <LogMatchScreen
              buildingId={profile?.buildingId}
              currentUid={profile?.uid}
              presetSport={activityMeta?.courtType as "basketball" | "soccer" | "padel"}
              presetCalories={finalCalories || null}
              onBack={() => setShowLogScore(false)}
              onLogged={() => setShowLogScore(false)}
            />
          </div>
        )}

        {showStickerMode && (
          <StickerShareScreen'''
    edits.append(('CardioTrackingScreen - render LogMatchScreen on Log Score', old3, new3))

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
