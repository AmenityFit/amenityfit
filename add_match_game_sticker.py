import sys

NEW_CODE = '''

// ── MatchGameSticker - transparent overlay sticker for match results ──────
// Wrapped in the same createPortal pattern StickerShareScreen uses, for
// the same real reason: on actual mobile WKWebView, position:fixed can
// get trapped inside its nearest scrolling ancestor instead of covering
// the full viewport - a portal to document.body sidesteps that.
// Deliberately simpler than StickerShareScreen's full version: no
// adaptive light/dark text based on sampling the photo behind it, that's
// real, separate engineering worth verifying on its own rather than
// copied in blind. Text here is always white with a strong shadow,
// which reads fine on most photo backgrounds but isn't the same
// auto-adaptive polish the workout stickers have yet.
const MatchGameStickerInner = ({
  sport,
  myName,
  opponentName,
  myScore,
  opponentScore,
  onClose,
}: {
  sport: "basketball" | "padel" | "soccer";
  myName: string;
  opponentName: string;
  myScore: number;
  opponentScore: number;
  onClose: () => void;
}) => {
  const stickerRef = React.useRef<HTMLDivElement>(null);
  const [sharing, setSharing] = useState(false);
  const [shareError, setShareError] = useState<string | null>(null);
  const [fallbackDownloadUrl, setFallbackDownloadUrl] = useState<string | null>(null);

  const isWin = myScore > opponentScore;
  const isDraw = myScore === opponentScore;
  const resultLabel = isDraw ? "DRAW" : isWin ? "W" : "L";
  const resultColor = isWin ? COLORS.accent : "#FFFFFF";

  const captureSticker = async (): Promise<Blob | null> => {
    if (!stickerRef.current) return null;
    const canvas = await html2canvas(stickerRef.current, { scale: 2, backgroundColor: null });
    return new Promise((resolve) => canvas.toBlob((blob: Blob | null) => resolve(blob), "image/png"));
  };

  const handleShare = async () => {
    setSharing(true);
    setShareError(null);
    try {
      const blob = await captureSticker();
      if (!blob) throw new Error("Could not generate sticker");
      const file = new File([blob], "amenityfit-match-sticker.png", { type: "image/png" });
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
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.9)", zIndex: 1100, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 20 }}>
      <div
        ref={stickerRef}
        style={{
          width: 260, padding: "20px 24px", borderRadius: 24,
          background: "rgba(20,20,20,0.55)", backdropFilter: "blur(12px)",
          fontFamily: "'Inter', sans-serif", textAlign: "center",
        }}
      >
        <p style={{ color: "#FFFFFF", fontSize: 11, fontWeight: 700, letterSpacing: 1.2, textTransform: "uppercase", margin: "0 0 8px", textShadow: "0 2px 8px rgba(0,0,0,0.6)" }}>{sport}</p>
        <span style={{
          display: "inline-block", background: isWin ? COLORS.accent : "transparent",
          border: isWin ? "none" : "1px solid rgba(255,255,255,0.5)",
          color: isWin ? "#0A0A0A" : "#FFFFFF",
          fontSize: 10, fontWeight: 900, letterSpacing: 1, padding: "3px 10px", borderRadius: 20, marginBottom: 8,
        }}>{resultLabel}</span>
        <h1 style={{ color: "#FFFFFF", fontSize: 44, fontWeight: 900, margin: 0, lineHeight: 1, textShadow: "0 2px 12px rgba(0,0,0,0.7)" }}>{myScore}-{opponentScore}</h1>
        <p style={{ color: "#FFFFFF", fontSize: 12, fontWeight: 600, margin: "10px 0 0", textShadow: "0 2px 8px rgba(0,0,0,0.6)" }}>{myName} vs {opponentName}</p>
      </div>

      <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
        <button onClick={handleShare} disabled={sharing} style={{ background: COLORS.accent, color: "#0A0A0A", border: "none", borderRadius: 20, padding: "10px 20px", fontSize: 13, fontWeight: 800, cursor: "pointer" }}>
          {sharing ? "Preparing..." : "Share Sticker"}
        </button>
        <button onClick={onClose} style={{ background: "transparent", color: "#FFFFFF", border: "1px solid rgba(255,255,255,0.3)", borderRadius: 20, padding: "10px 20px", fontSize: 13, fontWeight: 700, cursor: "pointer" }}>
          Close
        </button>
      </div>
      {shareError && <p style={{ color: "#FF6B6B", fontSize: 12, marginTop: 8 }}>{shareError}</p>}
      {fallbackDownloadUrl && (
        <a href={fallbackDownloadUrl} download="amenityfit-match-sticker.png" style={{ color: COLORS.accent, fontSize: 13, fontWeight: 700, marginTop: 10, textDecoration: "underline" }}>
          Download sticker
        </a>
      )}
    </div>
  );
};

const MatchGameSticker = (props: React.ComponentProps<typeof MatchGameStickerInner>) =>
  createPortal(<MatchGameStickerInner {...props} />, document.body);
'''

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_match_game_sticker.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "const MatchGameSticker" in content:
        print("ABORTED: MatchGameSticker already exists in this file. No changes were made.")
        sys.exit(1)
    if "const MatchGameCard" not in content:
        print("ABORTED: MatchGameCard doesn't exist in this file yet - run add_match_game_card.py first. No changes were made.")
        sys.exit(1)

    content = content.rstrip('\n') + '\n' + NEW_CODE.lstrip('\n')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Appended MatchGameSticker successfully to {path}")

if __name__ == '__main__':
    main()
