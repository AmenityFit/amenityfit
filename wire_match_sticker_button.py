import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 wire_match_sticker_button.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    edits = []

    old1 = '''  const [sharing, setSharing] = useState(false);
  const [shareError, setShareError] = useState<string | null>(null);
  const [fallbackDownloadUrl, setFallbackDownloadUrl] = useState<string | null>(null);

  const isWin = myScore > opponentScore;
  const isDraw = myScore === opponentScore;
  const resultLabel = isDraw ? "DRAW" : isWin ? "W" : "L";
  // Win gets the same bold accent glow'''
    new1 = '''  const [sharing, setSharing] = useState(false);
  const [shareError, setShareError] = useState<string | null>(null);
  const [fallbackDownloadUrl, setFallbackDownloadUrl] = useState<string | null>(null);
  const [showSticker, setShowSticker] = useState(false);

  const isWin = myScore > opponentScore;
  const isDraw = myScore === opponentScore;
  const resultLabel = isDraw ? "DRAW" : isWin ? "W" : "L";
  // Win gets the same bold accent glow'''
    edits.append(('MatchGameCard - declare showSticker state', old1, new1))

    old2 = '''      <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
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
};'''
    new2 = '''      <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
        <button onClick={handleShare} disabled={sharing} style={{ background: COLORS.accent, color: "#0A0A0A", border: "none", borderRadius: 20, padding: "10px 20px", fontSize: 13, fontWeight: 800, cursor: "pointer" }}>
          {sharing ? "Preparing..." : "Share"}
        </button>
        <button onClick={() => setShowSticker(true)} style={{ background: "transparent", color: COLORS.white, border: `1px solid ${COLORS.border}`, borderRadius: 20, padding: "10px 20px", fontSize: 13, fontWeight: 700, cursor: "pointer" }}>
          Sticker
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
      {showSticker && (
        <MatchGameSticker
          sport={sport}
          myName={myName}
          opponentName={opponentName}
          myScore={myScore}
          opponentScore={opponentScore}
          onClose={() => setShowSticker(false)}
        />
      )}
    </div>
  );
};'''
    edits.append(('MatchGameCard - add Sticker button and render MatchGameSticker', old2, new2))

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
