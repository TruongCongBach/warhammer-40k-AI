# Gotchas — full symptom→cause→fix table

## Auth & state

| Symptom | Cause | Fix |
|---------|-------|-----|
| `clearState: true` but iOS still authed | Keychain survives data wipe | `clearKeychain: true` OR explicit logout subflow |
| Android session persists after `clearState` | SharedPreferences in protected dir | `adb shell pm clear $appId` before `maestro test` |
| Biometric prompt blocks flow | TouchID/FaceID modal not in app hierarchy | iOS sim: `xcrun simctl ui $UDID biometric_match`. Or stub auth in dev build. |
| OTP-gated login flakes | Email delivery delay | Mailpit + GraalJS fetch (see `graaljs.md`) — local instant delivery |

## Selectors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Element not found: text="OK"` | Multiple "OK" buttons in hierarchy | Add relative selector (`below:`, `childOf:`) |
| Tap fires on wrong row | List recycled views with same testID | Compose unique testID with item key: `testID={`row-${item.id}`}` |
| testID present in JSX but Maestro can't see it | `<Pressable>` doesn't propagate testID to native | Wrap in `<View testID>` outer |
| Flow works in Studio, fails in CI | Different sim locale/size | Pin sim model + `LANG=en` env |

## Timing

| Symptom | Cause | Fix |
|---------|-------|-----|
| Random `assertVisible` fails | Optimistic UI server roundtrip | `timeout: 5000` for network, `3000` for animation |
| Cold-boot first launch fails on iOS | XCTest race `kAXErrorInvalidUIElement` | Tiny swipe after `launchApp` (see `platforms.md`) |
| Flow hangs forever | No timeout on a `wait*` step | Always set `timeout:` explicitly |
| Animation in progress, tap misses | Element exists but not yet interactive | `extendedWaitUntil: { visible: ..., timeout: 8000 }` before tap |

## GraalJS

| Symptom | Cause | Fix |
|---------|-------|-----|
| `fetch is not defined` | GraalJS, not Node | `http.get(url)` |
| `await` syntax error | GraalJS sync only | Remove `async/await`; HTTP is sync |
| `process.env.X is undefined` | No Node `process` | Use Maestro template `${X}` |
| Output not visible in next step | Wrong variable scope | Always `output.X = ...`, read as `${output.X}` |

## Deep links

| Symptom | Cause | Fix |
|---------|-------|-----|
| `openLink` opens browser instead of app | Used HTTPS without app association | Use URL scheme: `myapp://path` |
| Universal link opens but state wrong | Cold start vs warm path differ | Test both: `launchApp` first, then `openLink`, vs `stopApp` then `openLink` |

## Debugging workflow

1. `maestro hierarchy` while screen open → copy actual selectors
2. `maestro test --debug flow.yaml` → step-by-step with snapshots
3. `maestro studio` → live record + autocomplete
4. Failing in CI only → reproduce with same `LANG`, sim model, app build (CI app != local app often)
5. Flake suspected → `maestro test --retries=3` and check if all 3 attempts hit same step
