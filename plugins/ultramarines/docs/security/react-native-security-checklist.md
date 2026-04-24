# React Native Security Checklist

Use this checklist when a React Native ticket may affect security-sensitive behavior.

## Focus Areas

- Token and session storage: Keychain, Keystore, SecureStore, AsyncStorage, persisted stores
- Deep links and universal links: untrusted parameters, route hijacking, open-redirect style behavior
- WebViews: injected JavaScript, unrestricted origins, cookie/session leakage, unsafe messaging bridges
- Device files and uploads: temporary files, media permissions, file path exposure, stale cached files
- Clipboard and share flows: copying tokens, personal data, or internal URLs unintentionally
- Offline and retry behavior: replaying protected actions, stale auth state, duplicate submissions
- Push notifications and background flows: sensitive content in notifications, auth-dependent background actions
- Crash logging and analytics: request payloads, headers, tokens, or identifiers sent to third parties
- Platform differences: iOS vs Android permission handling, secure storage fallback behavior, app state transitions

## Questions To Ask

- Is sensitive data stored in the safest available mechanism?
- Can a deep link or push payload drive the user into a flow they should not access?
- Does a WebView or bridge trust content that should stay untrusted?
- Could logs, analytics, or crash reports leak something sensitive?
- Do offline or retry flows repeat a protected action without enough guarding?
