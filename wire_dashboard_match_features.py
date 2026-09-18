import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 wire_dashboard_match_features.py App.tsx")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old = '''        {visitedTabs.has("dashboard") && (
          <div style={{ display: screen === "dashboard" ? "block" : "none" }}>
            <Dashboard key={"dashboard" + workoutDoneToday + (userProfile?.programDay || 1)} profile={liveProfile} onStartWorkout={() => setScreen("workout")} onCompleteRestDay={handleCompleteRestDay} workoutDoneToday={workoutDoneToday} isInProgress={!!(userProfile?.workoutProgress?.date === new Date().toDateString())} onNavigate={navigate} onViewWeekly={() => setScreen("weekly")} reEntryMode={userProfile?.reEntryMode} reEntrySessions={userProfile?.reEntrySessions || 0} reEntryTarget={Math.round((userProfile?.frequency || 3) * 2)} wearableModifier={getWorkoutModifier(userProfile)} onWearableOverride={() => setUserProfile((prev: any) => ({ ...prev, wearableOverride: true }))} />
          </div>
        )}'''

    new = '''        {visitedTabs.has("dashboard") && (
          <div style={{ display: screen === "dashboard" ? "block" : "none" }}>
            <Dashboard key={"dashboard" + workoutDoneToday + (userProfile?.programDay || 1)} profile={liveProfile} onStartWorkout={() => setScreen("workout")} onCompleteRestDay={handleCompleteRestDay} workoutDoneToday={workoutDoneToday} isInProgress={!!(userProfile?.workoutProgress?.date === new Date().toDateString())} onNavigate={navigate} onViewWeekly={() => setScreen("weekly")} reEntryMode={userProfile?.reEntryMode} reEntrySessions={userProfile?.reEntrySessions || 0} reEntryTarget={Math.round((userProfile?.frequency || 3) * 2)} wearableModifier={getWorkoutModifier(userProfile)} onWearableOverride={() => setUserProfile((prev: any) => ({ ...prev, wearableOverride: true }))} />
            {/* Checks for any match logged against the current user that
                still needs their confirmation - this is what makes the
                head-to-head record trustworthy, so it runs automatically
                every time the dashboard is visited rather than needing to
                be found manually. */}
            {screen === "dashboard" && userProfile?.uid && (
              <PendingMatchConfirm currentUid={userProfile.uid} onDismiss={() => {}} />
            )}
            {screen === "dashboard" && (
              <button
                onClick={() => setScreen("log-match")}
                style={{
                  position: "fixed", bottom: 90, right: 20, zIndex: 500,
                  width: 56, height: 56, borderRadius: 28, border: "none",
                  background: COLORS.accent, color: "#0A0A0A", fontSize: 24, fontWeight: 900,
                  cursor: "pointer", boxShadow: "0 8px 24px rgba(0,0,0,0.4)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                }}
                aria-label="Log a match"
              >
                +
              </button>
            )}
          </div>
        )}'''

    count = content.count(old)
    if count != 1:
        print(f"ABORTED before writing: expected exactly 1 match, found {count}. No changes were made to the file.")
        sys.exit(1)

    content = content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Wired PendingMatchConfirm and the Log Match button successfully into {path}")

if __name__ == '__main__':
    main()
