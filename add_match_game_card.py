import sys

NEW_CODE = '''

// ── MatchGameCard - pickup-game result card (basketball / padel / soccer) ─
// Built as its own component rather than reusing ShareableStatCard,
// because that component's generic label/value stat grid treats every
// stat equally - it can't give the score the real visual dominance a
// match result needs. Reuses ShareableStatCard's real, proven
// conventions (COLORS tokens, Inter font, card container styling, the
// hero-stat glow treatment, the secondary-stat grid, the footer
// branding, and the exact same html2canvas capture + Web Share API
// fallback pattern - a visible download button, never a silent
// auto-triggered download) rather than inventing new ones.
const MatchGameCard = ({
  sport,
  myName,
  opponentName,
  myAvatar,
  opponentAvatar,
  myScore,
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
  caloriesBurned?: number | null;
  confirmed: boolean;
  onClose: () => void;
}) => {
  const cardRef = React.useRef<HTMLDivElement>(null);
  const [sharing, setSharing] = useState(false);
  const [shareError, setShareError] = useState<string | null>(null);
  const [fallbackDownloadUrl, setFallbackDownloadUrl] = useState<string | null>(null);

  const isWin = myScore > opponentScore;
  const isDraw = myScore === opponentScore;
  const resultLabel = isDraw ? "DRAW" : isWin ? "W" : "L";
  // Win gets the same bold accent glow the app already uses for a new
  // PR - confident, bright, unmistakable. Loss (and a draw) stay quiet
  // and muted on purpose, so the win state is the one that visually pops.
  const resultColor = isWin ? COLORS.accent : COLORS.textSecondary;
  const resultGlow = isWin ? `0 0 50px ${COLORS.accent}90` : "none";

  const captureCard = async (): Promise<Blob | null> => {
    if (!cardRef.current) return null;
    const canvas = await html2canvas(cardRef.current, { scale: 2, backgroundColor: null });
    return new Promise((resolve) => canvas.toBlob((blob: Blob | null) => resolve(blob), "image/png"));
  };

  const handleShare = async () => {
    setSharing(true);
    setShareError(null);
    try {
      const blob = await captureCard();
      if (!blob) throw new Error("Could not generate image");
      const file = new File([blob], "amenityfit-match.png", { type: "image/png" });
      if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({ files: [file], title: "AmenityFit Match Result" });
      } else {
        const url = URL.createObjectURL(blob);
        setFallbackDownloadUrl(url);
      }
    } catch (err) {
      setShareError("Could not share right now. Try again.");
    } finally {
      setSharing(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <div
        ref={cardRef}
        style={{
          width: 340, borderRadius: 28, overflow: "hidden", position: "relative",
          background: `linear-gradient(160deg, ${COLORS.background} 0%, ${COLORS.card} 100%)`,
          border: `1px solid ${COLORS.border}`,
          boxShadow: `0 20px 60px rgba(0,0,0,0.5)`,
          fontFamily: "'Inter', sans-serif",
        }}
      >
        <div style={{
          position: "absolute", top: -80, left: "50%", transform: "translateX(-50%)",
          width: 280, height: 280, borderRadius: "50%",
          background: `radial-gradient(circle, ${isWin ? COLORS.accent : COLORS.primary}35 0%, transparent 70%)`,
          pointerEvents: "none",
        }} />

        <div style={{ position: "relative", padding: "28px 24px 4px", textAlign: "center" }}>
          <p style={{ color: COLORS.textSecondary, fontSize: 12, fontWeight: 700, letterSpacing: 1.5, textTransform: "uppercase", margin: "0 0 4px" }}>{sport}</p>
        </div>

        {/* Hero: the score itself, the biggest thing on the card - this
            is the whole reason the card exists. */}
        <div style={{ position: "relative", textAlign: "center", padding: "4px 24px 4px" }}>
          <span style={{
            display: "inline-block", background: isWin ? COLORS.accent : "transparent",
            border: isWin ? "none" : `1px solid ${COLORS.border}`,
            color: isWin ? "#0A0A0A" : COLORS.textSecondary,
            fontSize: 11, fontWeight: 900, letterSpacing: 1, padding: "4px 12px", borderRadius: 20, marginBottom: 10,
          }}>{resultLabel}</span>
          <h1 style={{
            color: COLORS.white, fontSize: 56, fontWeight: 900, margin: 0, lineHeight: 1,
            letterSpacing: -1.5, textShadow: resultGlow,
          }}>{myScore}-{opponentScore}</h1>
        </div>

        {/* Both players, side by side - a duel layout, not a stacked list. */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 16, padding: "18px 24px 8px" }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6, flex: 1 }}>
            {myAvatar
              ? <img src={myAvatar} alt="" style={{ width: 44, height: 44, borderRadius: 22, objectFit: "cover", border: `2px solid ${resultColor}` }} />
              : <div style={{ width: 44, height: 44, borderRadius: 22, background: `${COLORS.white}10`, border: `2px solid ${resultColor}`, display: "flex", alignItems: "center", justifyContent: "center", color: COLORS.white, fontSize: 15, fontWeight: 800 }}>{myName.charAt(0).toUpperCase()}</div>}
            <p style={{ color: COLORS.white, fontSize: 13, fontWeight: 700, margin: 0, maxWidth: 90, textAlign: "center", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{myName}</p>
          </div>
          <p style={{ color: COLORS.textSecondary, fontSize: 12, fontWeight: 700, margin: 0 }}>VS</p>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6, flex: 1 }}>
            {opponentAvatar
              ? <img src={opponentAvatar} alt="" style={{ width: 44, height: 44, borderRadius: 22, objectFit: "cover", border: `1px solid ${COLORS.border}` }} />
              : <div style={{ width: 44, height: 44, borderRadius: 22, background: `${COLORS.white}10`, border: `1px solid ${COLORS.border}`, display: "flex", alignItems: "center", justifyContent: "center", color: COLORS.white, fontSize: 15, fontWeight: 800 }}>{opponentName.charAt(0).toUpperCase()}</div>}
            <p style={{ color: COLORS.white, fontSize: 13, fontWeight: 700, margin: 0, maxWidth: 90, textAlign: "center", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{opponentName}</p>
          </div>
        </div>

        {/* Secondary stats - deliberately smaller and quieter than the
            score, same rounded-box grid convention as every other card. */}
        {(heartRateAvg || caloriesBurned) && (
          <div style={{ padding: "16px 24px 8px", display: "grid", gridTemplateColumns: heartRateAvg && caloriesBurned ? "1fr 1fr" : "1fr", gap: 14 }}>
            {heartRateAvg && (
              <div style={{ background: `${COLORS.white}08`, borderRadius: 14, padding: "12px 8px", textAlign: "center" }}>
                <p style={{ color: COLORS.textSecondary, fontSize: 9, fontWeight: 700, letterSpacing: 0.8, textTransform: "uppercase", margin: "0 0 4px" }}>Avg Heart Rate</p>
                <p style={{ color: COLORS.white, fontSize: 17, fontWeight: 800, margin: 0 }}>{heartRateAvg} bpm</p>
              </div>
            )}
            {caloriesBurned && (
              <div style={{ background: `${COLORS.white}08`, borderRadius: 14, padding: "12px 8px", textAlign: "center" }}>
                <p style={{ color: COLORS.textSecondary, fontSize: 9, fontWeight: 700, letterSpacing: 0.8, textTransform: "uppercase", margin: "0 0 4px" }}>Calories</p>
                <p style={{ color: COLORS.white, fontSize: 17, fontWeight: 800, margin: 0 }}>{caloriesBurned}</p>
              </div>
            )}
          </div>
        )}

        {/* Understated on purpose - it builds trust without competing
            visually with the result itself. */}
        {confirmed && (
          <p style={{ color: COLORS.textSecondary, fontSize: 10, fontWeight: 600, textAlign: "center", margin: "8px 24px 0" }}>Confirmed by both players</p>
        )}

        <div style={{ position: "relative", padding: "16px 24px", marginTop: 12, borderTop: `1px solid ${COLORS.border}`, display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
          <img src={amenityfitLogo} alt="" style={{ width: 20, height: 20, borderRadius: 6, objectFit: "contain" }} />
          <span style={{ color: COLORS.white, fontSize: 13, fontWeight: 900, letterSpacing: 0.8 }}>AMENITYFIT</span>
        </div>
      </div>

      <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
        <button onClick={handleShare} disabled={sharing} style={{ background: COLORS.accent, color: "#0A0A0A", border: "none", borderRadius: 20, padding: "10px 20px", fontSize: 13, fontWeight: 800, cursor: "pointer" }}>
          {sharing ? "Preparing..." : "Share"}
        </button>
        <button onClick={onClose} style={{ background: "transparent", color: COLORS.textSecondary, border: `1px solid ${COLORS.border}`, borderRadius: 20, padding: "10px 20px", fontSize: 13, fontWeight: 700, cursor: "pointer" }}>
          Close
        </button>
      </div>
      {shareError && <p style={{ color: "#FF6B6B", fontSize: 12, marginTop: 8 }}>{shareError}</p>}
      {fallbackDownloadUrl && (
        <a href={fallbackDownloadUrl} download="amenityfit-match.png" style={{ color: COLORS.accent, fontSize: 13, fontWeight: 700, marginTop: 10, textDecoration: "underline" }}>
          Download image
        </a>
      )}
    </div>
  );
};
'''

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_match_game_card.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "const MatchGameCard" in content:
        print("ABORTED: MatchGameCard already exists in this file. No changes were made.")
        sys.exit(1)

    content = content.rstrip('\n') + '\n' + NEW_CODE.lstrip('\n')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Appended MatchGameCard successfully to {path}")

if __name__ == '__main__':
    main()
