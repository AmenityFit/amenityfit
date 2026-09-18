import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 make_debug_visible.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old = '''      {showLogScore && (
        <div style={{ position: "fixed", inset: 0, background: COLORS.background, zIndex: 900 }}>
          {/* TEMPORARY - remove once buildingId issue is confirmed */}
          {console.log("DEBUG profile object:", profile, "buildingId:", profile?.buildingId, "uid:", profile?.uid)}
          <LogMatchScreen'''
    new = '''      {showLogScore && (
        <div style={{ position: "fixed", inset: 0, background: COLORS.background, zIndex: 900 }}>
          {/* TEMPORARY - remove once buildingId issue is confirmed */}
          <div style={{ position: "fixed", top: 0, left: 0, right: 0, background: "#FF3B30", color: "#FFFFFF", padding: 12, fontSize: 12, fontFamily: "monospace", zIndex: 9999, wordBreak: "break-all" }}>
            DEBUG - buildingId: {JSON.stringify(profile?.buildingId)} | uid: {JSON.stringify(profile?.uid)}
          </div>
          <LogMatchScreen'''

    count = content.count(old)
    if count != 1:
        print(f"ABORTED before writing: expected exactly 1 match, found {count}. No changes were made to the file.")
        sys.exit(1)

    content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Applied visible debug banner successfully to {path}")

if __name__ == '__main__':
    main()
