import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_debug_log.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old = '''      {showLogScore && (
        <div style={{ position: "fixed", inset: 0, background: COLORS.background, zIndex: 900 }}>
          <LogMatchScreen'''
    new = '''      {showLogScore && (
        <div style={{ position: "fixed", inset: 0, background: COLORS.background, zIndex: 900 }}>
          {/* TEMPORARY - remove once buildingId issue is confirmed */}
          {console.log("DEBUG profile object:", profile, "buildingId:", profile?.buildingId, "uid:", profile?.uid)}
          <LogMatchScreen'''

    count = content.count(old)
    if count != 1:
        print(f"ABORTED before writing: expected exactly 1 match, found {count}. No changes were made to the file.")
        sys.exit(1)

    content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Applied temporary debug log successfully to {path}")
    print("Remember: this is temporary and should be removed once we've confirmed the real issue.")

if __name__ == '__main__':
    main()
