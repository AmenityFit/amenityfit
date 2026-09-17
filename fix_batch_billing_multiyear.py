import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_batch_billing_multiyear.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    edits = []

    # Edit 1: new state declarations
    old1 = '  const [batchCompanyName, setBatchCompanyName] = React.useState("");'
    new1 = '''  const [batchCompanyName, setBatchCompanyName] = React.useState("");
  const [batchBillingFrequency, setBatchBillingFrequency] = React.useState("");
  const [batchMultiYearTerm, setBatchMultiYearTerm] = React.useState("");'''
    edits.append(('new state: batchBillingFrequency, batchMultiYearTerm', old1, new1))

    # Edit 2: carry both fields through the Load into form handler
    old2 = '''                              setPortfolioAppLoadedId(app.id);
                              setBatchPropertyType(app.propertyType === "hotel" ? "hotel" : "building");'''
    new2 = '''                              setPortfolioAppLoadedId(app.id);
                              setBatchPropertyType(app.propertyType === "hotel" ? "hotel" : "building");
                              setBatchBillingFrequency(app.billingFrequency || "");
                              setBatchMultiYearTerm(app.multiYearTerm || "");'''
    edits.append(('carry billingFrequency/multiYearTerm through Load into form', old2, new2))

    # Edit 3: show both elections on the portfolio application card, so
    # they are visible even before clicking Load
    old3 = '''                            <p style={{ color: COLORS.textSecondary, fontSize: 11, margin: 0 }}>
                              {app.contactName} &middot; {app.execEmail} &middot; ~{app.propertyCount} properties
                              {app.csvText && app.csvText.trim() ? " · CSV attached" : " · No CSV - will need a follow-up"}
                              {app.referralCode ? ` · Ref: ${app.referralCode}` : ""}
                            </p>'''
    new3 = '''                            <p style={{ color: COLORS.textSecondary, fontSize: 11, margin: 0 }}>
                              {app.contactName} &middot; {app.execEmail} &middot; ~{app.propertyCount} properties
                              {app.csvText && app.csvText.trim() ? " · CSV attached" : " · No CSV - will need a follow-up"}
                              {app.referralCode ? ` · Ref: ${app.referralCode}` : ""}
                              {app.billingFrequency ? ` · Billing: ${app.billingFrequency === "monthly" ? "Monthly" : "Annual"}` : " · Billing: NOT SET"}
                              {app.multiYearTerm ? ` · ${app.multiYearTerm}-year term elected` : ""}
                            </p>'''
    edits.append(('display billingFrequency/multiYearTerm on the application card', old3, new3))

    # Edit 4: required selector UI + warning, inserted right before the
    # existing PM Executive Email warning block
    old4 = '''                {!batchPmEmail.trim() && (
                  <div style={{ background: "#FF4D4D15", border: "1px solid #FF4D4D40", borderRadius: 12, padding: "12px 16px", marginBottom: 16 }}>
                    <p style={{ color: "#FF6B6B", fontSize: 13, margin: 0 }}>⚠️ A PM Executive Email is required before submitting a batch.</p>
                  </div>
                )}'''
    new4 = '''                <div style={{ marginBottom: 16 }}>
                  <label style={{ color: COLORS.textSecondary, fontSize: 12, fontWeight: 600, display: "block", marginBottom: 6 }}>Payment Frequency (required)</label>
                  <select
                    value={batchBillingFrequency}
                    onChange={e => setBatchBillingFrequency(e.target.value)}
                    style={{ width: "100%", padding: 12, borderRadius: 10, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 13 }}
                  >
                    <option value="">Select one</option>
                    <option value="annual">Annual (paid upfront)</option>
                    <option value="monthly">Monthly</option>
                  </select>
                </div>
                {batchPropertyType === "hotel" && (
                  <div style={{ marginBottom: 16 }}>
                    <label style={{ color: COLORS.textSecondary, fontSize: 12, fontWeight: 600, display: "block", marginBottom: 6 }}>Portfolio Commitment Term</label>
                    <select
                      value={batchMultiYearTerm}
                      onChange={e => setBatchMultiYearTerm(e.target.value)}
                      style={{ width: "100%", padding: 12, borderRadius: 10, border: `1px solid ${COLORS.border}`, background: COLORS.card, color: COLORS.white, fontSize: 13 }}
                    >
                      <option value="">Standard 1-year term</option>
                      <option value="2">2-year term</option>
                      <option value="3">3-year term</option>
                    </select>
                  </div>
                )}
                {!batchBillingFrequency && (
                  <div style={{ background: "#FF4D4D15", border: "1px solid #FF4D4D40", borderRadius: 12, padding: "12px 16px", marginBottom: 16 }}>
                    <p style={{ color: "#FF6B6B", fontSize: 13, margin: 0 }}>⚠️ Payment Frequency must be selected before submitting a batch.</p>
                  </div>
                )}
                {!batchPmEmail.trim() && (
                  <div style={{ background: "#FF4D4D15", border: "1px solid #FF4D4D40", borderRadius: 12, padding: "12px 16px", marginBottom: 16 }}>
                    <p style={{ color: "#FF6B6B", fontSize: 13, margin: 0 }}>⚠️ A PM Executive Email is required before submitting a batch.</p>
                  </div>
                )}'''
    edits.append(('required Payment Frequency / Commitment Term selectors + warning', old4, new4))

    # Edit 5: validate + write both fields into the actual batchSubmissions doc
    old5 = '''                    const valid = batchParsed.filter(b => b.valid);
                    if (valid.length === 0 || !batchPmEmail.trim() || !batchCompanyName.trim()) return;
                    setBatchSubmitting(true);
                    try {
                      const batchDocRef = doc(collection(db, "batchSubmissions"));
                      await setDoc(batchDocRef, {
                        companyName: batchCompanyName.trim(),
                        pmEmail: batchPmEmail.trim(),
                        propertyType: batchPropertyType,
                        buildings: valid.map(b => ({
                          buildingName: b.buildingName,
                          location: b.location,
                          units: b.units,
                          managerEmail: b.managerEmail,
                        })),
                        status: "pending",
                        createdAt: serverTimestamp(),
                      });
                      setBatchSubmissionId(batchDocRef.id);
                      setBatchInvoiceMode(true);
                    } catch (e: any) {
                      alert("Failed to submit batch: " + (e.message || "Unknown error"));
                    }
                    setBatchSubmitting(false);
                  }}
                  disabled={batchParsed.every(b => !b.valid) || !batchPmEmail.trim() || !batchCompanyName.trim() || batchSubmitting}'''
    new5 = '''                    const valid = batchParsed.filter(b => b.valid);
                    if (valid.length === 0 || !batchPmEmail.trim() || !batchCompanyName.trim() || !batchBillingFrequency) return;
                    setBatchSubmitting(true);
                    try {
                      const batchDocRef = doc(collection(db, "batchSubmissions"));
                      await setDoc(batchDocRef, {
                        companyName: batchCompanyName.trim(),
                        pmEmail: batchPmEmail.trim(),
                        propertyType: batchPropertyType,
                        billingFrequency: batchBillingFrequency,
                        multiYearTerm: batchPropertyType === "hotel" ? batchMultiYearTerm : "",
                        buildings: valid.map(b => ({
                          buildingName: b.buildingName,
                          location: b.location,
                          units: b.units,
                          managerEmail: b.managerEmail,
                        })),
                        status: "pending",
                        createdAt: serverTimestamp(),
                      });
                      setBatchSubmissionId(batchDocRef.id);
                      setBatchInvoiceMode(true);
                    } catch (e: any) {
                      alert("Failed to submit batch: " + (e.message || "Unknown error"));
                    }
                    setBatchSubmitting(false);
                  }}
                  disabled={batchParsed.every(b => !b.valid) || !batchPmEmail.trim() || !batchCompanyName.trim() || !batchBillingFrequency || batchSubmitting}'''
    edits.append(('require + write billingFrequency/multiYearTerm to batchSubmissions', old5, new5))

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
