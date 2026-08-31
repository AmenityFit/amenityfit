
// ============ WIDENING VERIFICATION ============
console.log("\n\n============ WIDENING VERIFICATION ============");

const testProfiles = [
  { label: "Advanced Male Bands-Only", experience: "advanced", effectiveLevel: "advanced", gender: "male", equipmentPreference: "bands", frequency: 4, primaryGoal: "muscle_gain", age: "28" },
  { label: "Advanced Female Bands-Only", experience: "advanced", effectiveLevel: "advanced", gender: "female", equipmentPreference: "bands", frequency: 3, primaryGoal: "muscle_gain", age: "32" },
  { label: "Intermediate Male Bands-Only", experience: "intermediate", effectiveLevel: "intermediate", gender: "male", equipmentPreference: "bands", frequency: 4, primaryGoal: "fat_loss", age: "29" },
];

for (const baseProfile of testProfiles) {
  console.log(`\n--- ${baseProfile.label} ---`);
  let profile = { ...baseProfile, cycleNumber: 6, previousPrograms: [], exerciseHistory: {}, sessionLength: 60, injuries: "none" };
  const results = [];
  let crashed = false, crashMsg = "";
  const equipmentViolations = [];
  const structuralShapes = new Set();

  for (let cycle = 6; cycle <= 40; cycle++) {
    profile.cycleNumber = cycle;
    try {
      const result = generateMonth6Program(profile);
      const usedIds = [];
      const dayShapes = [];
      (result.generatedDays || []).forEach(day => {
        if (day.isRest) return;
        const exIds = [];
        (day.groups || []).forEach(g => (g.exercises || []).forEach(ex => {
          if (ex.id) { usedIds.push(ex.id); exIds.push(ex.id); }
        }));
        dayShapes.push(exIds.length);
        // Check every exercise used is actually bands-compatible
        exIds.forEach(id => {
          const exData = EXERCISES_DATA[id];
          if (!exData) return;
          const eq = (exData.equipment || "").toLowerCase();
          const bandsIncompatible = ["barbell", "cable machine", "machine", "smith machine", "leg press"].some(bad => eq.includes(bad));
          if (bandsIncompatible && baseProfile.equipmentPreference === "bands") {
            equipmentViolations.push(`cycle ${cycle}: ${id} (${exData.equipment})`);
          }
        });
      });
      structuralShapes.add(dayShapes.join(","));
      results.push({ cycle, programKey: result.programKey, exerciseIds: usedIds });
      const newHistory = { ...profile.exerciseHistory };
      usedIds.forEach(id => { newHistory[id] = cycle; });
      profile = { ...profile, previousPrograms: [...profile.previousPrograms, result.programKey], exerciseHistory: newHistory };
    } catch (e) {
      crashed = true; crashMsg = e.message; break;
    }
  }

  if (crashed) {
    console.log(`  !!! CRASHED at cycle: ${crashMsg}`);
    continue;
  }

  const distinctSkeletons = new Set(results.map(r => r.programKey.replace("month6-", ""))).size;
  console.log("Cycles run:", results.length, "| Distinct skeleton labels:", distinctSkeletons, "| Distinct day-count shapes:", structuralShapes.size);
  console.log("Equipment violations:", equipmentViolations.length, equipmentViolations.length > 0 ? equipmentViolations.slice(0, 10) : "");

  // Exercise overlap in later cycles (post Phase-2 kick-in) - lower = more variety
  if (results.length > 15) {
    const a = new Set(results[results.length - 3].exerciseIds);
    const b = new Set(results[results.length - 2].exerciseIds);
    const overlap = [...a].filter(x => b.has(x)).length;
    console.log(`Late-cycle exercise overlap: ${overlap}/${a.size} identical between consecutive cycles`);
  }
}
