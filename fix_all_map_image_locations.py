import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_all_map_image_locations.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    edits = []

    # ── Line ~16706: ActivityDetailView's court/map display ────────────────
    old1 = '''      {courtType && mapUrl && (
        <div style={{ margin: "16px 24px 0", borderRadius: 20, overflow: "hidden", border: `1px solid ${COLORS.border}` }}>
          <img src={mapUrl} alt="" style={{ width: "100%", display: "block" }} />
        </div>
      )}'''
    new1 = '''      {courtType && mapUrl && (
        <div style={{ margin: "16px 24px 0", borderRadius: 20, overflow: "hidden", border: `1px solid ${COLORS.border}`, aspectRatio: "16/9" }}>
          <img src={mapUrl} alt="" style={{ width: "100%", height: "100%", objectFit: "contain", display: "block" }} crossOrigin="anonymous" />
        </div>
      )}'''
    edits.append(('ActivityDetailView court/map (line ~16706)', old1, new1))

    # ── Line ~19962: CardioTrackingScreen completion screen ────────────────
    old2 = '''        {mapUrl && (
          <div style={{ margin: "16px 24px 0", borderRadius: 20, overflow: "hidden", border: `1px solid ${COLORS.border}`, boxShadow: "0 8px 30px rgba(0,0,0,0.3)" }}>
            <img src={mapUrl} alt="Route map" decoding="sync" loading="eager" style={{ width: "100%", display: "block" }} />
          </div>
        )}'''
    new2 = '''        {mapUrl && (
          <div style={{ margin: "16px 24px 0", borderRadius: 20, overflow: "hidden", border: `1px solid ${COLORS.border}`, boxShadow: "0 8px 30px rgba(0,0,0,0.3)", aspectRatio: "16/9" }}>
            <img src={mapUrl} alt="Route map" decoding="sync" loading="eager" style={{ width: "100%", height: "100%", objectFit: "contain", display: "block" }} crossOrigin="anonymous" />
          </div>
        )}'''
    edits.append(('CardioTrackingScreen completion screen (line ~19962)', old2, new2))

    # ── Line ~20870: ShareableStatCard classic layout ───────────────────────
    old3 = '''        {displayMapUrl && (
          <div style={{ margin: "0 20px 8px", borderRadius: 16, overflow: "hidden", border: `1px solid ${COLORS.border}` }}>
            <img src={displayMapUrl} alt="" style={{ width: "100%", display: "block" }} crossOrigin="anonymous" />
          </div>
        )}'''
    new3 = '''        {displayMapUrl && (
          <div style={{ margin: "0 20px 8px", borderRadius: 16, overflow: "hidden", border: `1px solid ${COLORS.border}`, aspectRatio: "16/9" }}>
            <img src={displayMapUrl} alt="" style={{ width: "100%", height: "100%", objectFit: "contain", display: "block" }} crossOrigin="anonymous" />
          </div>
        )}'''
    edits.append(('ShareableStatCard classic layout (line ~20870)', old3, new3))

    # ── Line ~20934: the actual likely culprit - sticker's own map overlay
    # mode, already has a fixed height:220 clipping container AND the
    # already-proven-risky width:auto/height:auto+max CSS combination. ─────
    old4 = '''            <div style={{ position: "relative", height: 220, background: COLORS.card, display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden" }}>
              <img src={displayMapUrl} alt="" style={{ maxWidth: "100%", maxHeight: "100%", width: "auto", height: "auto", display: "block" }} crossOrigin="anonymous" />'''
    new4 = '''            <div style={{ position: "relative", height: 220, background: COLORS.card, display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden" }}>
              <img src={displayMapUrl} alt="" style={{ width: "100%", height: "100%", objectFit: "contain", display: "block" }} crossOrigin="anonymous" />'''
    edits.append(('Sticker map overlay mode - the likely real culprit (line ~20934)', old4, new4))

    # ── Line ~20987: another displayMapUrl location ─────────────────────────
    old5 = '''          {displayMapUrl && (
            <div style={{ margin: "16px 0 0", borderRadius: 14, overflow: "hidden", border: `1px solid ${COLORS.border}` }}>
              <img src={displayMapUrl} alt="" style={{ width: "100%", display: "block" }} crossOrigin="anonymous" />
            </div>
          )}'''
    new5 = '''          {displayMapUrl && (
            <div style={{ margin: "16px 0 0", borderRadius: 14, overflow: "hidden", border: `1px solid ${COLORS.border}`, aspectRatio: "16/9" }}>
              <img src={displayMapUrl} alt="" style={{ width: "100%", height: "100%", objectFit: "contain", display: "block" }} crossOrigin="anonymous" />
            </div>
          )}'''
    edits.append(('Remaining displayMapUrl location (line ~20987)', old5, new5))

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
