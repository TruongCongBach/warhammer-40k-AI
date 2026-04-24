# React Native Planning Checklist

## Purpose

Use this checklist when the ticket affects a React Native app.

## Checklist

- Screen entry point is identified.
- Navigation path and back-stack behavior are considered.
- Local state, global state, or server state ownership is clear.
- Loading, refreshing, and retry behavior are planned.
- Error state and empty state behavior are planned.
- Keyboard, focus, and form interaction behavior are considered.
- Platform differences between iOS and Android are considered.
- Safe area, notch, and device-size variations are considered.
- Gesture or scroll interaction behavior is considered.
- Offline or flaky-network behavior is considered if relevant.
- Native module or permissions impact is considered if relevant.
- Analytics, logging, or crash reporting impact is considered if relevant.

## Likely Affected Areas

- `screens/`
- `navigation/`
- `components/`
- `hooks/`
- `store/`, `redux/`, `zustand/`, or context providers
- `services/` or `api/`
- form validators and transformers
- native bridge or permission handlers
