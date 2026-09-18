import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 show_real_residents_error.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old = '''      } catch (err) {
        setSubmitError("Could not load residents. Try again.");
      } finally {
        if (!cancelled) setLoadingResidents(false);
      }'''
    new = '''      } catch (err: any) {
        // TEMPORARY - showing the real error to diagnose, revert to a
        // plain message once the actual cause is confirmed.
        setSubmitError(`Could not load residents. Real error: ${err?.code || "no code"} - ${err?.message || String(err)}`);
      } finally {
        if (!cancelled) setLoadingResidents(false);
      }'''

    count = content.count(old)
    if count != 1:
        print(f"ABORTED before writing: expected exactly 1 match, found {count}. No changes were made to the file.")
        sys.exit(1)

    content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Applied real-error diagnostic successfully to {path}")

if __name__ == '__main__':
    main()
