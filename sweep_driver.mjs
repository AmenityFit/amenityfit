
// ============ FULL SYSTEMATIC SWEEP ============
const sweepExperiences = ["beginner", "intermediate", "advanced"];
const sweepAges = [{ label: "adult", age: "30" }, { label: "senior", age: "68" }];
const sweepGenders = ["male", "female", "prefer_not"];
const sweepEquipments = ["gym", "bands", "gym-and-bands"];
const sweepGoals = ["fat_loss", "muscle_gain", "general_fitness", "athletic_performance"];

let totalCombos = 0, crashCombos = 0, wrongLevelCombos = 0, wrongGenderCombos = 0, thinContentCombos = 0;
const failures = [];
const thinContentList = [];

for (const experience of sweepExperiences) {
  for (const ageInfo of sweepAges) {
    for (const gender of sweepGenders) {
      for (const equipmentPreference of sweepEquipments) {
        for (const primaryGoal of sweepGoals) {
          totalCombos++;
          const label = `${experience}/${ageInfo.label}/${gender}/${equipmentPreference}/${primaryGoal}`;
          let profile = {
            experience, effectiveLevel: experience, age: ageInfo.age, gender, equipmentPreference,
            primaryGoal, frequency: 4, sessionLength: 60, injuries: "none",
            cycleNumber: 6, previousPrograms: [], exerciseHistory: {},
          };
          const results = [];
          let crashed = false, crashMsg = "";

          for (let cycle = 6; cycle <= 25; cycle++) {
            profile.cycleNumber = cycle;
            try {
              const result = generateMonth6Program(profile);
              const usedIds = [];
              (result.generatedDays || []).forEach(day => {
                if (day.isRest) return;
                (day.groups || []).forEach(g => (g.exercises || []).forEach(ex => { if (ex.id) usedIds.push(ex.id); }));
              });
              results.push({ cycle, programKey: result.programKey, exerciseIds: usedIds });
              const newHistory = { ...profile.exerciseHistory };
              usedIds.forEach(id => { newHistory[id] = cycle; });
              profile = { ...profile, previousPrograms: [...profile.previousPrograms, result.programKey], exerciseHistory: newHistory };
            } catch (e) {
              crashed = true; crashMsg = e.message; break;
            }
          }

          if (crashed) {
            crashCombos++;
            failures.push(`CRASH: ${label} -> ${crashMsg}`);
            continue;
          }

          const isSenior = ageInfo.label === "senior";
          const wrongLevel = results.filter(r => {
            let k = r.programKey.replace("month6-", "");
            if (isSenior && !k.includes("senior")) return true;
            if (!isSenior && k.includes("senior")) return true;
            if (experience === "intermediate" && k.includes("beginner")) return true;
            if (experience === "advanced" && k.includes("beginner")) return true;
            if (experience === "beginner" && (k.includes("intermediate") || k.includes("advanced"))) return true;
            return false;
          });
          if (wrongLevel.length > 0) {
            wrongLevelCombos++;
            failures.push(`WRONG-LEVEL: ${label} -> ${[...new Set(wrongLevel.map(r => r.programKey))]}`);
          }

          const wrongGender = results.filter(r => {
            const k = r.programKey.replace("month6-", "");
            if (gender === "male") return k.startsWith("womens-");
            if (gender === "female") return k.startsWith("mens-");
            return k.startsWith("mens-") || k.startsWith("womens-");
          });
          if (wrongGender.length > 0) {
            wrongGenderCombos++;
            failures.push(`WRONG-GENDER: ${label} -> ${[...new Set(wrongGender.map(r => r.programKey))]}`);
          }

          const distinctSkeletons = new Set(results.map(r => r.programKey.replace("month6-", ""))).size;
          if (distinctSkeletons <= 2) {
            thinContentCombos++;
            thinContentList.push(`${label}: only ${distinctSkeletons} distinct skeleton(s) available`);
          }
        }
      }
    }
  }
}

console.log("\n\n============ SWEEP SUMMARY ============");
console.log("Total combinations tested:", totalCombos);
console.log("Crashes:", crashCombos);
console.log("Wrong-level leaks:", wrongLevelCombos);
console.log("Wrong-gender leaks:", wrongGenderCombos);
console.log("Thin-content combos (<=2 distinct skeletons):", thinContentCombos);
console.log("\n--- FAILURES (crash/wrong-level/wrong-gender) ---");
failures.forEach(f => console.log(f));
console.log("\n--- THIN CONTENT (not a bug, real content gap) ---");
thinContentList.forEach(t => console.log(t));
