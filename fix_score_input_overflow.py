import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_score_input_overflow.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old = '''        <input
          type="number" inputMode="numeric" value={myScore} onChange={(e) => setMyScore(e.target.value)}
          placeholder="You" style={{ flex: 1, boxSizing: "border-box", padding: "12px 14px", borderRadius: 14, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 16, fontWeight: 800, textAlign: "center", fontFamily: "'Inter', sans-serif" }}
        />
        <span style={{ color: COLORS.textSecondary, fontSize: 14, fontWeight: 700 }}>-</span>
        <input
          type="number" inputMode="numeric" value={opponentScore} onChange={(e) => setOpponentScore(e.target.value)}
          placeholder="Them" style={{ flex: 1, boxSizing: "border-box", padding: "12px 14px", borderRadius: 14, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 16, fontWeight: 800, textAlign: "center", fontFamily: "'Inter', sans-serif" }}
        />'''
    new = '''        <input
          type="number" inputMode="numeric" value={myScore} onChange={(e) => setMyScore(e.target.value)}
          placeholder="You" style={{ flex: 1, minWidth: 0, width: "100%", boxSizing: "border-box", padding: "12px 14px", borderRadius: 14, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 16, fontWeight: 800, textAlign: "center", fontFamily: "'Inter', sans-serif" }}
        />
        <span style={{ color: COLORS.textSecondary, fontSize: 14, fontWeight: 700, flexShrink: 0 }}>-</span>
        <input
          type="number" inputMode="numeric" value={opponentScore} onChange={(e) => setOpponentScore(e.target.value)}
          placeholder="Them" style={{ flex: 1, minWidth: 0, width: "100%", boxSizing: "border-box", padding: "12px 14px", borderRadius: 14, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 16, fontWeight: 800, textAlign: "center", fontFamily: "'Inter', sans-serif" }}
        />'''

    count = content.count(old)
    if count != 1:
        print(f"ABORTED before writing: expected exactly 1 match, found {count}. No changes were made to the file.")
        sys.exit(1)

    content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Applied score input overflow fix successfully to {path}")

if __name__ == '__main__':
    main()
