import sys

NEW_CODE = '''

// ── PendingMatchConfirm - the actual trust mechanic ────────────────────────
// Checks for any match logged against the current user that's still
// pending their confirmation. Shows a real prompt with the claimed
// result; only once they tap Confirm does confirmMatchGame get called
// and the match becomes real (counts toward the head-to-head record,
// becomes shareable). If they never confirm, it just stays pending
// forever - no dispute system needed, exactly as designed.
const PendingMatchConfirm = ({
  currentUid,
  onDismiss,
}: {
  currentUid: string;
  onDismiss: () => void;
}) => {
  const [pendingMatch, setPendingMatch] = useState<any | null>(null);
  const [loggerName, setLoggerName] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [confirming, setConfirming] = useState(false);
  const [confirmError, setConfirmError] = useState<string | null>(null);
  const [confirmedResult, setConfirmedResult] = useState<any | null>(null);

  React.useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const snap = await getDocs(query(
          collection(db, "matchGames"),
          where("player2Id", "==", currentUid),
          where("status", "==", "pending"),
        ));
        if (cancelled) return;
        if (snap.docs.length === 0) { setLoading(false); return; }
        const matchDoc = snap.docs[0];
        const match = { id: matchDoc.id, ...matchDoc.data() } as any;
        setPendingMatch(match);
        const loggerDoc = await getDocFromServer(doc(db, "users", match.loggedBy));
        if (!cancelled && loggerDoc.exists()) {
          const data = loggerDoc.data() as any;
          setLoggerName(data.name || data.displayName || "A player");
        }
      } catch (err) {
        // Silent - a pending-match prompt failing to load isn't worth
        // surfacing an error screen over, it'll just show again next visit.
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [currentUid]);

  const handleConfirm = async () => {
    if (!pendingMatch) return;
    setConfirming(true);
    setConfirmError(null);
    try {
      const idToken = await getAuth().currentUser?.getIdToken();
      if (!idToken) throw new Error("Not signed in.");
      const res = await fetch("https://us-central1-amenityfit-31276.cloudfunctions.net/confirmMatchGame", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idToken, matchId: pendingMatch.id }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Could not confirm this match.");
      setConfirmedResult(pendingMatch);
    } catch (err: any) {
      setConfirmError(err.message || "Could not confirm this match. Try again.");
    } finally {
      setConfirming(false);
    }
  };

  if (loading || !pendingMatch) return null;

  if (confirmedResult) {
    return (
      <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.85)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000, padding: 20 }}>
        <MatchGameCard
          sport={confirmedResult.sport}
          myName="You"
          opponentName={loggerName}
          myScore={confirmedResult.score2}
          opponentScore={confirmedResult.score1}
          heartRateAvg={confirmedResult.heartRateAvg}
          caloriesBurned={confirmedResult.caloriesBurned}
          confirmed={true}
          onClose={onDismiss}
        />
      </div>
    );
  }

  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.85)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000, padding: 20 }}>
      <div style={{ width: 320, background: COLORS.card, borderRadius: 24, border: `1px solid ${COLORS.border}`, padding: "28px 24px", fontFamily: "'Inter', sans-serif", textAlign: "center" }}>
        <p style={{ color: COLORS.textSecondary, fontSize: 12, fontWeight: 700, letterSpacing: 0.8, textTransform: "uppercase", margin: "0 0 12px" }}>{pendingMatch.sport}</p>
        <h2 style={{ color: COLORS.white, fontSize: 18, fontWeight: 800, margin: "0 0 8px" }}>{loggerName} logged a game against you</h2>
        <p style={{ color: COLORS.white, fontSize: 32, fontWeight: 900, margin: "12px 0" }}>{pendingMatch.score1}-{pendingMatch.score2}</p>
        <p style={{ color: COLORS.textSecondary, fontSize: 13, margin: "0 0 24px" }}>Confirm this result to make it count.</p>
        {confirmError && <p style={{ color: "#FF6B6B", fontSize: 12, marginBottom: 14 }}>{confirmError}</p>}
        <div style={{ display: "flex", gap: 10, justifyContent: "center" }}>
          <button onClick={handleConfirm} disabled={confirming} style={{ flex: 1, padding: "12px", borderRadius: 20, border: "none", background: COLORS.accent, color: "#0A0A0A", fontSize: 14, fontWeight: 800, cursor: "pointer" }}>
            {confirming ? "Confirming..." : "Confirm"}
          </button>
          <button onClick={onDismiss} style={{ flex: 1, padding: "12px", borderRadius: 20, border: `1px solid ${COLORS.border}`, background: "transparent", color: COLORS.textSecondary, fontSize: 14, fontWeight: 700, cursor: "pointer" }}>
            Later
          </button>
        </div>
      </div>
    </div>
  );
};
'''

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_pending_match_confirm.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "const PendingMatchConfirm" in content:
        print("ABORTED: PendingMatchConfirm already exists in this file. No changes were made.")
        sys.exit(1)
    if "const MatchGameCard" not in content:
        print("ABORTED: MatchGameCard doesn't exist in this file yet - run add_match_game_card.py first. No changes were made.")
        sys.exit(1)

    content = content.rstrip('\n') + '\n' + NEW_CODE.lstrip('\n')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Appended PendingMatchConfirm successfully to {path}")

if __name__ == '__main__':
    main()
