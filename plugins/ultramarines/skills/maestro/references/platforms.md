# Platform specifics

## iOS

- `appId:` = bundle ID (`com.example.app`), NOT scheme
- `clearState: true` clears app data but **NOT Keychain** — explicit logout subflow needed for auth
- `clearKeychain: true` (Maestro 1.34+) wipes Keychain on launch
- Cold-boot race: first frame may report `kAXErrorInvalidUIElement`. Add a tiny swipe right after `launchApp` to force layout settle:
  ```yaml
  - launchApp
  - swipe:
      from: { x: 50%, y: 50% }
      to: { x: 50%, y: 45% }
  ```
- Permission dialog labels: `Allow`, `Allow While Using App`, `Don't Allow`
- Notification dialog: `Allow`, `Don't Allow`
- Locale: English in CI (`maestro test -e LANG=en`); non-English permission text breaks

### Sim selection

```bash
# List
xcrun simctl list devices available
# Boot specific
maestro --device "iPhone 15 Pro" test ...
```

## Android

- `appId:` = package name (`com.example.app`)
- ADB visible: `adb devices` must list device before `maestro test`
- Permission dialog labels (vary by API): `Allow`, `While using the app`, `Only this time`, `Deny`
- Some OEMs (MIUI, EMUI) inject extra dialogs — `optional: true` essential

### Emulator helpers

```bash
# Start specific AVD
emulator -avd Pixel_7_API_34 -no-snapshot -no-boot-anim &
adb wait-for-device

# Run Maestro
maestro test .maestro/flows
```

## React Native (RN/Expo)

- Use `testID="..."` on every interactive element
- `testID` does NOT propagate from RN component to native view by default — wrap in `<View testID>` if `<Pressable>` doesn't expose it
- Expo dev client: deep links via `exp+yourapp://path` in dev, `yourapp://path` in prod
- Hot reload during `maestro studio`: kill metro and re-launch, state diverges otherwise

## Flutter

- `Semantics(identifier: "...")` — NOT widget `key:`
- Enable semantics tree: `WidgetsApp(showSemanticsDebugger: false)` is fine; Maestro reads accessibility tree directly
- Flutter web: not supported by Maestro (use Playwright instead)

## Web (Chromium)

- `appId:` = URL: `appId: "https://example.com"`
- Selectors: CSS-like via `id:` or `text:`
- Maestro web is beta — Playwright remains the better choice for web E2E
