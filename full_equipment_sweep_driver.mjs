
// ============ FULL 216-COMBINATION EQUIPMENT SAFETY SWEEP ============
console.log("\n\n============ FULL EQUIPMENT SAFETY SWEEP ============");

const eqExperiences = ["beginner", "intermediate", "advanced"];
const eqAges = [{ label: "adult", age: "30" }, { label: "senior", age: "68" }];
const eqGenders = ["male", "female", "prefer_not"];
const eqEquipments = ["gym", "bands", "gym-and-bands"];
const eqGoals = ["fat_loss", "muscle_gain", "general_fitness", "athletic_performance"];

let eqTotalCombos = 0, eqCrashCombos = 0, eqViolationCombos = 0, eqTotalViolations = 0;
const eqFailures = [];

for (const experience of eqExperiences) {
  for (const ageInfo of eqAges) {
    for (const gender of eqGenders) {
      for (const equipmentPreference of eqEquipments) {
        for (const primaryGoal of eqGoals) {
          eqTotalCombos++;
          const label = `${experience}/${ageInfo.label}/${gender}/${equipmentPreference}/${primaryGoal}`;
          let profile = {
            experience, effectiveLevel: experience, age: ageInfo.age, gender, equipmentPreference,
            primaryGoal, frequency: 4, sessionLength: 60, injuries: "none",
            cycleNumber: 6, previousPrograms: [], exerciseHistory: {},
          };
          let crashed = false, crashMsg = "";
          const violations = [];

          for (let cycle = 6; cycle <= 30; cycle++) {
            profile.cycleNumber = cycle;
            try {
              const result = generateMonth6Program(profile);
              const usedIds = [];
              (result.generatedDays || []).forEach(day => {
                if (day.isRest) return;
                (day.groups || []).forEach(g => (g.exercises || []).forEach(ex => { if (ex.id) usedIds.push(ex.id); }));
              });
              usedIds.forEach(id => {
                const exData = EXERCISES_DATA[id];
                if (!exData) return;
                const eq = (exData.equipment || "").toLowerCase();
                if (equipmentPreference === "bands") {
                  const gymOnly = ["barbell", "cable machine", "machine", "smith machine", "leg press"].some(bad => eq.includes(bad));
                  if (gymOnly) violations.push(`cycle ${cycle}: ${id} (${exData.equipment})`);
                } else if (equipmentPreference === "gym") {
                  const bandOnly = eq.includes("band") || id.startsWith("band-");
                  if (bandOnly) violations.push(`cycle ${cycle}: ${id} (${exData.equipment})`);
                }
              });
              const newHistory = { ...profile.exerciseHistory };
              usedIds.forEach(id => { newHistory[id] = cycle; });
              profile = { ...profile, previousPrograms: [...profile.previousPrograms, result.programKey], exerciseHistory: newHistory };
            } catch (e) {
              crashed = true; crashMsg = e.message; break;
            }
          }

          if (crashed) {
            eqCrashCombos++;
            eqFailures.push(`CRASH: ${label} -> ${crashMsg}`);
            continue;
          }

          if (violations.length > 0) {
            eqViolationCombos++;
            eqTotalViolations += violations.length;
            eqFailures.push(`EQUIPMENT: ${label} -> ${violations.length} violations, e.g. ${violations[0]}`);
          }
        }
      }
    }
  }
}

console.log("Total combinations tested:", eqTotalCombos);
console.log("Crashes:", eqCrashCombos);
console.log("Combos with equipment violations:", eqViolationCombos, "| Total violations:", eqTotalViolations);
console.log("\n--- FAILURES ---");
eqFailures.forEach(f => console.log(f));
