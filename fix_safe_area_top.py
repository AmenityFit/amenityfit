import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_safe_area_top.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old = '''    <div style={{ minHeight: "100vh", background: COLORS.background, fontFamily: "'Inter', sans-serif", padding: "24px 20px 40px" }}>
      <button onClick={onBack} style={{ background: "transparent", border: "none", color: COLORS.textSecondary, fontSize: 14, fontWeight: 700, cursor: "pointer", marginBottom: 20 }}>
        ← Back
      </button>'''
    new = '''    <div style={{ minHeight: "100vh", background: COLORS.background, fontFamily: "'Inter', sans-serif", padding: "calc(24px + env(safe-area-inset-top)) 20px 40px" }}>
      <button onClick={onBack} style={{ background: "transparent", border: "none", color: COLORS.textSecondary, fontSize: 14, fontWeight: 700, cursor: "pointer", marginBottom: 20 }}>
        ← Back
      </button>'''

    count = content.count(old)
    if count != 1:
        print(f"ABORTED before writing: expected exactly 1 match, found {count}. No changes were made to the file.")
        sys.exit(1)

    content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Applied safe-area top padding fix successfully to {path}")

if __name__ == '__main__':
    main()
