# Selector grammar — full reference

## Match dimensions

```yaml
- tapOn:
    id: "checkout-cta"          # testID (RN), accessibilityIdentifier (iOS), resource-id/contentDescription (Android)
    text: "Checkout"            # visible label or substring (regex with /.../)
    enabled: true               # state
    checked: true               # toggles
    focused: true               # input field
    selected: true              # tab bar / segmented control
    width: 300                  # px constraints (rare)
    height: 60
    point: "50%,80%"            # absolute fallback (last resort)
```

Combine multiple keys = AND.

## Regex match

```yaml
- assertVisible:
    text: "Order #[0-9]+"
```

Wrap pattern in `/.../` if you need escapes/anchors.

## Relative selectors

Disambiguate repeated labels without resorting to `index:`.

```yaml
- tapOn:
    text: "Delete"
    childOf:
      id: "cart-row-sku-A1"
```

```yaml
- tapOn:
    text: "Edit"
    below:
      text: "Shipping address"
```

```yaml
- assertVisible:
    text: "$ 99.00"
    rightOf:
      text: "Total"
```

```yaml
- tapOn:
    id: "qty-plus"
    containsDescendants:
      - text: "Item A"
```

## Selector anti-patterns

| ❌ Bad | ✅ Good | Why |
|-------|--------|-----|
| `index: 2` | `childOf: { id: "row-${SKU}" }` | Index changes when row reorders |
| `text: "OK"` (alone) | `text: "OK"` + `below: { text: "Save changes?" }` | "OK" exists in many dialogs |
| `point: "200,400"` | `id: "submit"` | Layout shifts break absolute coords |
| Long substrings of i18n strings | `id:` set in code | Translations break flow |

## testID conventions

Recommend in app code:
- React Native: `testID="feature-element-purpose"` e.g. `testID="cart-row-delete"`
- iOS native: `accessibilityIdentifier`
- Android: `android:tag` or `contentDescription`
- Flutter: `Semantics(identifier: "...")` (NOT `key:`)

Pattern: kebab-case, scope-prefix (`cart-row-…`, `checkout-…`).

## Wait + assert combos

```yaml
- extendedWaitUntil:
    visible:
      id: "list-item-1"
    timeout: 8000
- assertVisible:
    id: "list-item-1"
```

Use `extendedWaitUntil` for legitimately slow loads (network, animation chains). Default `assertVisible` polls 1.5s — bump `timeout:` for optimistic UI.
