import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_share_confirmation.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # ── 1. One safely-appended helper, no anchor risk at all ────────────────
    helper = '''

// ── showShareConfirmation - a real, visible signal that a share/save
// action actually completed, instead of nothing happening at all. Plain
// DOM manipulation on purpose, not React state - this needs to work
// identically from five separate components without adding five new
// pieces of state, each needing its own safely-unique anchor to declare.
// Honest about what it confirms: that the OS share sheet was completed
// without being cancelled - the web app has no way to know which
// specific destination the person chose there, so this says "Shared",
// not "Saved to Photos", since the app genuinely can't promise that.
function showShareConfirmation() {
  const el = document.createElement("div");
  el.textContent = "Shared";
  el.style.cssText = "position:fixed;bottom:100px;left:50%;transform:translateX(-50%);background:rgba(30,30,30,0.95);color:#FFFFFF;padding:12px 24px;border-radius:20px;font-family:'Inter',sans-serif;font-size:14px;font-weight:700;z-index:99999;box-shadow:0 8px 24px rgba(0,0,0,0.4);pointer-events:none;opacity:0;transition:opacity 0.2s ease;";
  document.body.appendChild(el);
  requestAnimationFrame(() => { el.style.opacity = "1"; });
  setTimeout(() => {
    el.style.opacity = "0";
    setTimeout(() => el.remove(), 250);
  }, 2000);
}
'''

    if "function showShareConfirmation" in content:
        print("ABORTED: showShareConfirmation already exists in this file. No changes were made.")
        sys.exit(1)

    edits = []

    old1 = '''      if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({ files: [file], title: "My AmenityFit Stats" });
      } else {
        // Real fix for a genuine bug found via real-device testing: an
        // auto-triggered download here can fail completely silently in
        // the wrapped app's WKWebView specifically - nothing visible
        // happens at all, no error, no confirmation. Surfacing a real,
        // on-screen button the person can see and tap themselves removes
        // that ambiguity entirely.
        setFallbackDownloadUrl(URL.createObjectURL(blob));
      }
    } catch (e: any) {'''
    new1 = '''      if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({ files: [file], title: "My AmenityFit Stats" });
        showShareConfirmation();
      } else {
        // Real fix for a genuine bug found via real-device testing: an
        // auto-triggered download here can fail completely silently in
        // the wrapped app's WKWebView specifically - nothing visible
        // happens at all, no error, no confirmation. Surfacing a real,
        // on-screen button the person can see and tap themselves removes
        // that ambiguity entirely.
        setFallbackDownloadUrl(URL.createObjectURL(blob));
      }
    } catch (e: any) {'''
    edits.append(('ShareableStatCard handleShare (line ~20742)', old1, new1))

    old2 = '''      const file = new File([blob], "amenityfit-sticker.png", { type: "image/png" });
      if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({ files: [file], title: "My AmenityFit Stats" });
      } else {
        // Same visible-fallback fix as ShareableStatCard - see its own
        // comment for the full explanation.
        setFallbackDownloadUrl(URL.createObjectURL(blob));
      }
    } catch (e: any) {
      if (e?.name !== "AbortError") setShareError("Couldn't share right now. Try again.");
    }
    setSharing(false);
  };'''
    count2 = content.count(old2)
    if count2 != 2:
        print(f"ABORTED before writing: 'StickerShareScreen handleShare (both modes)' matched {count2} times (expected exactly 2). No changes were made to the file.")
        sys.exit(1)
    new2 = '''      const file = new File([blob], "amenityfit-sticker.png", { type: "image/png" });
      if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({ files: [file], title: "My AmenityFit Stats" });
        showShareConfirmation();
      } else {
        // Same visible-fallback fix as ShareableStatCard - see its own
        // comment for the full explanation.
        setFallbackDownloadUrl(URL.createObjectURL(blob));
      }
    } catch (e: any) {
      if (e?.name !== "AbortError") setShareError("Couldn't share right now. Try again.");
    }
    setSharing(false);
  };'''
    # This block appears twice (both sticker modes at lines ~21502 and ~21541) -
    # both get fixed together by replace() below, intentionally.
    edits.append(('StickerShareScreen handleShare - both modes (lines ~21502, ~21541)', old2, new2))

    old3 = '''      const file = new File([blob], "amenityfit-match.png", { type: "image/png" });
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
  };'''
    new3 = '''      const file = new File([blob], "amenityfit-match.png", { type: "image/png" });
      if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({ files: [file], title: "AmenityFit Match Result" });
        showShareConfirmation();
      } else {
        const url = URL.createObjectURL(blob);
        setFallbackDownloadUrl(url);
      }
    } catch (err) {
      setShareError("Could not share right now. Try again.");
    } finally {
      setSharing(false);
    }
  };'''
    edits.append(('MatchGameCard handleShare (line ~30045)', old3, new3))

    old4 = '''      const file = new File([blob], "amenityfit-match-sticker.png", { type: "image/png" });
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
  };'''
    new4 = '''      const file = new File([blob], "amenityfit-match-sticker.png", { type: "image/png" });
      if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({ files: [file], title: "AmenityFit Match Result" });
        showShareConfirmation();
      } else {
        const url = URL.createObjectURL(blob);
        setFallbackDownloadUrl(url);
      }
    } catch (err) {
      setShareError("Could not share right now. Try again.");
    } finally {
      setSharing(false);
    }
  };'''
    edits.append(('MatchGameSticker handleShare (line ~30520)', old4, new4))

    for label, old, new in edits:
        if old in (old2,):
            continue  # already count-checked above with its own rule
        count = content.count(old)
        if count != 1:
            print(f"ABORTED before writing: '{label}' matched {count} times (expected exactly 1). No changes were made to the file.")
            sys.exit(1)

    for label, old, new in edits:
        content = content.replace(old, new)

    content = content.rstrip('\n') + '\n' + helper.lstrip('\n')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Applied {len(edits)} edits (one covering 2 locations) plus the helper function successfully to {path}")
    for label, _, _ in edits:
        print(f"  - {label}")

if __name__ == '__main__':
    main()
