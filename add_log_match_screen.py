import sys

NEW_SCREEN_CODE = '''

// ── LogMatchScreen - pick sport, pick opponent, enter score ───────────────
// Opponent selection is a real-user picker, not free text - confirmMatchGame
// needs a real opponentUid to send the confirmation to, so this queries
// other users in the same building (matching the buildingId field already
// used everywhere else in the backend, e.g. residentsSnap queries).
const MATCH_SPORTS_LIST: { id: "basketball" | "padel" | "soccer"; label: string }[] = [
  { id: "basketball", label: "Basketball" },
  { id: "padel", label: "Padel" },
  { id: "soccer", label: "Soccer" },
];

const LogMatchScreen = ({
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
  const [sport, setSport] = useState<"basketball" | "padel" | "soccer" | null>(null);
  const [residents, setResidents] = useState<{ id: string; name: string; avatar?: string | null }[]>([]);
  const [loadingResidents, setLoadingResidents] = useState(true);
  const [search, setSearch] = useState("");
  const [opponentId, setOpponentId] = useState<string | null>(null);
  const [myScore, setMyScore] = useState("");
  const [opponentScore, setOpponentScore] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  React.useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const snap = await getDocs(query(collection(db, "users"), where("buildingId", "==", buildingId)));
        if (cancelled) return;
        const list = snap.docs
          .filter((d) => d.id !== currentUid)
          .map((d) => {
            const data = d.data() as any;
            return { id: d.id, name: data.name || data.displayName || "Resident", avatar: data.photoURL || null };
          });
        setResidents(list);
      } catch (err) {
        setSubmitError("Could not load residents. Try again.");
      } finally {
        if (!cancelled) setLoadingResidents(false);
      }
    })();
    return () => { cancelled = true; };
  }, [buildingId, currentUid]);

  const filteredResidents = search.trim()
    ? residents.filter((r) => r.name.toLowerCase().includes(search.trim().toLowerCase()))
    : residents;

  const canSubmit = sport && opponentId && myScore !== "" && opponentScore !== "" && !submitting;

  const handleSubmit = async () => {
    if (!canSubmit || !sport || !opponentId) return;
    setSubmitting(true);
    setSubmitError(null);
    try {
      const idToken = await getAuth().currentUser?.getIdToken();
      if (!idToken) throw new Error("Not signed in.");
      const res = await fetch("https://us-central1-amenityfit-31276.cloudfunctions.net/logMatchGame", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          idToken, sport, opponentUid: opponentId,
          myScore: Number(myScore), opponentScore: Number(opponentScore),
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Could not log this match.");
      onLogged(data.matchId);
    } catch (err: any) {
      setSubmitError(err.message || "Could not log this match. Try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: COLORS.background, fontFamily: "'Inter', sans-serif", padding: "24px 20px 40px" }}>
      <button onClick={onBack} style={{ background: "transparent", border: "none", color: COLORS.textSecondary, fontSize: 14, fontWeight: 700, cursor: "pointer", marginBottom: 20 }}>
        ← Back
      </button>
      <h1 style={{ color: COLORS.white, fontSize: 24, fontWeight: 900, margin: "0 0 24px" }}>Log a Match</h1>

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

      <p style={{ color: COLORS.textSecondary, fontSize: 12, fontWeight: 700, letterSpacing: 0.8, textTransform: "uppercase", margin: "0 0 10px" }}>Opponent</p>
      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search residents..."
        style={{ width: "100%", boxSizing: "border-box", padding: "12px 14px", borderRadius: 14, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 14, marginBottom: 10, fontFamily: "'Inter', sans-serif" }}
      />
      <div style={{ maxHeight: 220, overflowY: "auto", marginBottom: 24 }}>
        {loadingResidents ? (
          <p style={{ color: COLORS.textSecondary, fontSize: 13 }}>Loading residents...</p>
        ) : filteredResidents.length === 0 ? (
          <p style={{ color: COLORS.textSecondary, fontSize: 13 }}>No residents found.</p>
        ) : (
          filteredResidents.map((r) => (
            <button key={r.id} onClick={() => setOpponentId(r.id)} style={{
              width: "100%", display: "flex", alignItems: "center", gap: 10, padding: "10px 12px", marginBottom: 6,
              borderRadius: 12, border: `1px solid ${opponentId === r.id ? COLORS.accent : COLORS.border}`,
              background: opponentId === r.id ? `${COLORS.accent}18` : COLORS.card, cursor: "pointer", textAlign: "left",
            }}>
              {r.avatar
                ? <img src={r.avatar} alt="" style={{ width: 32, height: 32, borderRadius: 16, objectFit: "cover" }} />
                : <div style={{ width: 32, height: 32, borderRadius: 16, background: `${COLORS.white}10`, display: "flex", alignItems: "center", justifyContent: "center", color: COLORS.white, fontSize: 13, fontWeight: 800 }}>{r.name.charAt(0).toUpperCase()}</div>}
              <span style={{ color: COLORS.white, fontSize: 14, fontWeight: 600 }}>{r.name}</span>
            </button>
          ))
        )}
      </div>

      <p style={{ color: COLORS.textSecondary, fontSize: 12, fontWeight: 700, letterSpacing: 0.8, textTransform: "uppercase", margin: "0 0 10px" }}>Score</p>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 28 }}>
        <input
          type="number" inputMode="numeric" value={myScore} onChange={(e) => setMyScore(e.target.value)}
          placeholder="You" style={{ flex: 1, boxSizing: "border-box", padding: "12px 14px", borderRadius: 14, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 16, fontWeight: 800, textAlign: "center", fontFamily: "'Inter', sans-serif" }}
        />
        <span style={{ color: COLORS.textSecondary, fontSize: 14, fontWeight: 700 }}>-</span>
        <input
          type="number" inputMode="numeric" value={opponentScore} onChange={(e) => setOpponentScore(e.target.value)}
          placeholder="Them" style={{ flex: 1, boxSizing: "border-box", padding: "12px 14px", borderRadius: 14, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 16, fontWeight: 800, textAlign: "center", fontFamily: "'Inter', sans-serif" }}
        />
      </div>

      {submitError && <p style={{ color: "#FF6B6B", fontSize: 13, marginBottom: 14 }}>{submitError}</p>}

      <button onClick={handleSubmit} disabled={!canSubmit} style={{
        width: "100%", padding: "16px", borderRadius: 20, border: "none",
        background: canSubmit ? COLORS.accent : COLORS.card, color: canSubmit ? "#0A0A0A" : COLORS.textSecondary,
        fontSize: 15, fontWeight: 800, cursor: canSubmit ? "pointer" : "not-allowed",
      }}>
        {submitting ? "Logging..." : "Log Match"}
      </button>
    </div>
  );
};
'''

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_log_match_screen.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "const LogMatchScreen" in content:
        print("ABORTED: LogMatchScreen already exists in this file. No changes were made.")
        sys.exit(1)

    # Wire it into the real routing pattern - inserted right before the
    # existing "preview" early-return, matching how other standalone
    # flows (onboarding, login) are wired: an early return keyed off
    # `screen`, not the persistent-tab display-toggle pattern.
    anchor = '  if (screen === "preview" && previewDay?.isRest) {'
    route_line = '''  if (screen === "log-match") return <LogMatchScreen buildingId={userProfile?.buildingId} currentUid={userProfile?.uid} onBack={() => setScreen("dashboard")} onLogged={(matchId) => { setScreen("dashboard"); }} />;

'''
    if anchor not in content:
        print("ABORTED: could not find the routing anchor to wire in the new screen. The LogMatchScreen component was NOT added either, so nothing was changed. Send the exact current text around the 'preview' screen check and I will adjust the anchor.")
        sys.exit(1)
    if content.count(anchor) != 1:
        print(f"ABORTED: anchor matched {content.count(anchor)} times, expected exactly 1. No changes were made.")
        sys.exit(1)

    content = content.replace(anchor, route_line + anchor)
    content = content.rstrip('\n') + '\n' + NEW_SCREEN_CODE.lstrip('\n')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Added LogMatchScreen and wired it into routing successfully in {path}")

if __name__ == '__main__':
    main()
