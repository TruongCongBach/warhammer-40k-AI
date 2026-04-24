# React Native Review Checklist

## Purpose

Use this checklist when reviewing a React Native implementation.

## Checklist

- Screen entry and navigation path are consistent with the ticket.
- Back navigation and route transitions appear safe.
- Loading, refreshing, and retry states are handled.
- Error and empty states are visible and actionable when relevant.
- Keyboard, focus, and form interactions are handled.
- Disabled CTA behavior is explicit when required.
- iOS and Android differences are considered.
- Safe area, notch, and smaller-device layout risks are considered.
- Gesture, scroll, and list interactions appear stable.
- Async state updates are not likely to create flicker, stale UI, or race conditions.
- Hardcoded spacing, colors, or typography values are not replacing shared tokens without reason.
- Tests cover critical interactive paths if the change is behavior-heavy.

## Common Review Targets

- `screens/`
- `navigation/`
- `components/`
- `hooks/`
- store or context providers
- API/services and request handlers
- shared theme or token files
