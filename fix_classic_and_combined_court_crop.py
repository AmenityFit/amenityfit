import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_classic_and_combined_court_crop.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    edits = []

    # ── Full Combined layout's map image ────────────────────────────────────
    old1 = '''          {routeMapUrl && (
            <img
              src={routeMapUrl}
              alt=""
              decoding="sync"
              loading="eager"
              crossOrigin="anonymous"
              style={{ maxWidth: 200, maxHeight: 130, width: "auto", height: "auto", borderRadius: 12, filter: `drop-shadow(0 4px 16px rgba(0,0,0,0.5))` }}
            />
          )}
          {logoRow}
        </div>
      );
    }

    // "Classic" - the original, unchanged design. Also the fallback if
    // "Full Combined" was somehow selected without real combined data.
    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start", gap: 14 }}>
        {routeMapUrl && (
          <img
            src={routeMapUrl}
            alt=""
            decoding="sync"
            loading="eager"
            crossOrigin="anonymous"
            style={{ maxWidth: 240, maxHeight: 160, width: "auto", height: "auto", borderRadius: 12, filter: `drop-shadow(0 4px 16px rgba(0,0,0,0.5))` }}
          />
        )}'''
    new1 = '''          {routeMapUrl && (
            <div style={{ width: 200, height: 130, display: "flex", alignItems: "flex-start", justifyContent: "flex-start" }}>
              <img
                src={routeMapUrl}
                alt=""
                decoding="sync"
                loading="eager"
                crossOrigin="anonymous"
                style={{ width: "100%", height: "100%", objectFit: "contain", objectPosition: "left top", borderRadius: 12, filter: `drop-shadow(0 4px 16px rgba(0,0,0,0.5))` }}
              />
            </div>
          )}
          {logoRow}
        </div>
      );
    }

    // "Classic" - the original, unchanged design. Also the fallback if
    // "Full Combined" was somehow selected without real combined data.
    // Real fix: this was the one location neither earlier pass ever
    // reached - it still had the exact width:auto/height:auto+max
    // pattern already confirmed broken elsewhere, and Classic is the
    // default/most commonly selected tab, so this was very likely the
    // actual real cause of the export cropping the whole time.
    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start", gap: 14 }}>
        {routeMapUrl && (
          <div style={{ width: 240, height: 160, display: "flex", alignItems: "flex-start", justifyContent: "flex-start" }}>
            <img
              src={routeMapUrl}
              alt=""
              decoding="sync"
              loading="eager"
              crossOrigin="anonymous"
              style={{ width: "100%", height: "100%", objectFit: "contain", objectPosition: "left top", borderRadius: 12, filter: `drop-shadow(0 4px 16px rgba(0,0,0,0.5))` }}
            />
          </div>
        )}'''
    edits.append(('Full Combined and Classic layout map images', old1, new1))

    for label, old, new in edits:
        count = content.count(old)
        if count != 1:
            print(f"ABORTED before writing: '{label}' matched {count} times (expected exactly 1). No changes were made to the file.")
            sys.exit(1)

    for label, old, new in edits:
        content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Applied {len(edits)} edit(s) successfully to {path}")
    for label, _, _ in edits:
        print(f"  - {label}")

if __name__ == '__main__':
    main()
