import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_log_score_button.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    edits = []

    # ── 1. LogMatchScreen: accept presetSport/presetCalories so it can be
    # opened from a real activity session with the sport and calories
    # already known, instead of asking for them again. ────────────────────
    old1 = '''const LogMatchScreen = ({
  buildingId,
  currentUid,
  onBack,
  onLogged,
}: {
  buildingId: string;
  currentUid: string;
  onBack: () => void;
  onLogged: (matchId: string) => void;
}) => {
  const [sport, setSport] = useState<"basketball" | "padel" | "soccer" | null>(null);'''
    new1 = '''const LogMatchScreen = ({
  buildingId,
  currentUid,
  onBack,
  onLogged,
  presetSport,
  presetCalories,
}: {
  buildingId: string;
  currentUid: string;
  onBack: () => void;
  onLogged: (matchId: string) => void;
  // Set when opened from a real tracked activity session - the sport is
  // already known (from the session's own courtType), so the picker step
  // is skipped entirely rather than asking again for something already
  // captured.
  presetSport?: "basketball" | "padel" | "soccer";
  // Real tracked calories from the session, submitted as-is - never
  // re-asked for here.
  presetCalories?: number | null;
}) => {
  const [sport, setSport] = useState<"basketball" | "padel" | "soccer" | null>(presetSport || null);'''
    edits.append(('LogMatchScreen - accept presetSport/presetCalories props', old1, new1))

    old2 = '''        body: JSON.stringify({
          idToken, sport, opponentUid: opponentId,
          myScore: Number(myScore), opponentScore: Number(opponentScore),
        }),'''
    new2 = '''        body: JSON.stringify({
          idToken, sport, opponentUid: opponentId,
          myScore: Number(myScore), opponentScore: Number(opponentScore),
          caloriesBurned: typeof presetCalories === "number" ? presetCalories : undefined,
        }),'''
    edits.append(('LogMatchScreen - submit real presetCalories with the match', old2, new2))

    old3 = '''      <p style={{ color: COLORS.textSecondary, fontSize: 12, fontWeight: 700, letterSpacing: 0.8, textTransform: "uppercase", margin: "0 0 10px" }}>Sport</p>
      <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
        {MATCH_SPORTS_LIST.map((s) => (
          <button key={s.id} onClick={() => setSport(s.id)} style={{
            flex: 1, padding: "12px 8px", borderRadius: 14, border: `1px solid ${sport === s.id ? COLORS.accent : COLORS.border}`,
            background: sport === s.id ? `${COLORS.accent}18` : COLORS.card,
            color: sport === s.id ? COLORS.accent : COLORS.white, fontSize: 13, fontWeight: 700, cursor: "pointer",
          }}>
            {s.label}
          </button>
        ))}
      </div>'''
    new3 = '''      {!presetSport && (
        <>
          <p style={{ color: COLORS.textSecondary, fontSize: 12, fontWeight: 700, letterSpacing: 0.8, textTransform: "uppercase", margin: "0 0 10px" }}>Sport</p>
          <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
            {MATCH_SPORTS_LIST.map((s) => (
              <button key={s.id} onClick={() => setSport(s.id)} style={{
                flex: 1, padding: "12px 8px", borderRadius: 14, border: `1px solid ${sport === s.id ? COLORS.accent : COLORS.border}`,
                background: sport === s.id ? `${COLORS.accent}18` : COLORS.card,
                color: sport === s.id ? COLORS.accent : COLORS.white, fontSize: 13, fontWeight: 700, cursor: "pointer",
              }}>
                {s.label}
              </button>
            ))}
          </div>
        </>
      )}'''
    edits.append(('LogMatchScreen - hide sport picker when preset', old3, new3))

    # ── 2. ActivityDetailView: the real Log Score entry point ──────────────
    old4 = '''      <div style={{ padding: "24px", marginTop: "auto", display: "flex", gap: 12 }}>
        <button onClick={() => setShowShareCard(true)} style={{ flex: 1, padding: "16px", borderRadius: 16, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 15, fontWeight: 700, cursor: "pointer" }}>
          Share
        </button>
        <button onClick={() => setShowStickerMode(true)} style={{ flex: 1, padding: "16px", borderRadius: 16, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 15, fontWeight: 700, cursor: "pointer" }}>
          Sticker
        </button>
      </div>'''
    new4 = '''      {/* Log Score - the real entry point for match sports. Only shown for
          basketball/soccer/padel (not pickleball - not in scope), and
          only when this session hasn't already had a match logged
          against it, so the same session can't be submitted twice. */}
      {(courtType === "basketball" || courtType === "soccer" || courtType === "padel") && !session.matchGameId && (
        <div style={{ padding: "0 24px", marginTop: "auto" }}>
          <button onClick={() => setShowLogScore(true)} style={{ width: "100%", padding: "16px", borderRadius: 16, border: "none", background: COLORS.accent, color: "#0A0A0A", fontSize: 15, fontWeight: 800, cursor: "pointer" }}>
            Log Score
          </button>
        </div>
      )}
      <div style={{ padding: "24px", marginTop: (courtType === "basketball" || courtType === "soccer" || courtType === "padel") && !session.matchGameId ? "12px" : "auto", display: "flex", gap: 12 }}>
        <button onClick={() => setShowShareCard(true)} style={{ flex: 1, padding: "16px", borderRadius: 16, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 15, fontWeight: 700, cursor: "pointer" }}>
          Share
        </button>
        <button onClick={() => setShowStickerMode(true)} style={{ flex: 1, padding: "16px", borderRadius: 16, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 15, fontWeight: 700, cursor: "pointer" }}>
          Sticker
        </button>
      </div>
      {showLogScore && (
        <div style={{ position: "fixed", inset: 0, background: COLORS.background, zIndex: 900 }}>
          <LogMatchScreen
            buildingId={profile?.buildingId}
            currentUid={profile?.uid}
            presetSport={courtType as "basketball" | "soccer" | "padel"}
            presetCalories={session.calories || null}
            onBack={() => setShowLogScore(false)}
            onLogged={() => setShowLogScore(false)}
          />
        </div>
      )}'''
    edits.append(('ActivityDetailView - add real Log Score entry point', old4, new4))

    # ── 3. ActivityDetailView needs the showLogScore state declared ────────
    old5 = '''const ActivityDetailView = ({ session, sessionHistory, profile, onClose }: { session: any; sessionHistory: any[]; profile: any; onClose: () => void }) => {
  const [showShareCard, setShowShareCard] = useState(false);
  const [showStickerMode, setShowStickerMode] = useState(false);'''
    new5 = '''const ActivityDetailView = ({ session, sessionHistory, profile, onClose }: { session: any; sessionHistory: any[]; profile: any; onClose: () => void }) => {
  const [showShareCard, setShowShareCard] = useState(false);
  const [showStickerMode, setShowStickerMode] = useState(false);
  const [showLogScore, setShowLogScore] = useState(false);'''
    edits.append(('ActivityDetailView - declare showLogScore state', old5, new5))

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
