import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_back_button_alignment.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old = '''      <button onClick={onBack} style={{ background: "transparent", border: "none", color: COLORS.textSecondary, fontSize: 14, fontWeight: 700, cursor: "pointer", marginBottom: 20 }}>
        ← Back
      </button>'''
    new = '''      <button onClick={onBack} style={{ display: "flex", alignSelf: "flex-start", alignItems: "center", gap: 6, background: "transparent", border: "none", color: COLORS.textSecondary, fontSize: 16, fontWeight: 700, cursor: "pointer", marginBottom: 20, padding: "8px 0", textAlign: "left" }}>
        ← Back
      </button>'''

    count = content.count(old)
    if count != 1:
        print(f"ABORTED before writing: expected exactly 1 match, found {count}. No changes were made to the file.")
        sys.exit(1)

    content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Applied Back button alignment/size fix successfully to {path}")

if __name__ == '__main__':
    main()
