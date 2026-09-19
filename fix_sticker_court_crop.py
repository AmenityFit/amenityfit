import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_sticker_court_crop.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old = '''          {routeMapUrl && (
            <img
              src={routeMapUrl}
              alt=""
              decoding="sync"
              loading="eager"
              crossOrigin="anonymous"
              style={{ maxWidth: 300, maxHeight: 220, width: "auto", height: "auto", borderRadius: 12, filter: `drop-shadow(0 4px 16px rgba(0,0,0,0.5))` }}
            />
          )}'''
    new = '''          {routeMapUrl && (
            // Real fix for a confirmed export bug found via real-device
            // testing: width:auto/height:auto with maxWidth/maxHeight
            // asks the browser to scale the whole image down to fit -
            // html2canvas is known to mishandle exactly this combination,
            // capturing the image at its native size and clipping to the
            // smaller box instead of actually scaling it, which showed up
            // as the court cropped to its top-left corner on the actual
            // exported sticker despite looking correct live. A fixed-size
            // container with object-fit:contain removes that ambiguity -
            // it's a well-established reliable pattern with this tool.
            <div style={{ width: 300, height: 220, display: "flex", alignItems: "flex-start", justifyContent: "flex-start" }}>
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

    count = content.count(old)
    if count != 1:
        print(f"ABORTED before writing: expected exactly 1 match, found {count}. No changes were made to the file.")
        sys.exit(1)

    content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Applied sticker court crop fix successfully to {path}")

if __name__ == '__main__':
    main()
