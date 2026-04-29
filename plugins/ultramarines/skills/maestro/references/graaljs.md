# GraalJS scripting (`evalScript` / `runScript`)

Maestro embeds **GraalJS**, NOT Node.js. Most Node APIs absent.

## Allowed

| API | Use |
|-----|-----|
| `http.get(url)` / `http.post(url, body)` | HTTP requests (sync, returns `{ok, body, status}`) |
| `output.X = value` | Pass data back to flow as `${output.X}` |
| `var`, `let`, `const` | Declarations |
| Standard JS: arrays, regex, JSON, string ops | Yes |
| `console.log` | Logs to Maestro test output |

## Forbidden

| API | Why |
|-----|-----|
| `fetch()` | Not in GraalJS — use `http.get` |
| `async`/`await` | All scripts run sync |
| `require()` / `import` | No module system |
| `process.env` | Use Maestro env vars: `${MAESTRO_BASE_URL}` |
| `Buffer`, `fs`, Node stdlib | Not available |

## OTP fetch pattern (Mailpit local)

`scripts/fetch-otp.js`:
```javascript
var response = http.get('http://localhost:8025/api/v1/messages?limit=1');
var json = JSON.parse(response.body);
var body = json.messages[0].Snippet;
var match = body.match(/\b(\d{6})\b/);
output.otp = match ? match[1] : '';
```

In flow:
```yaml
- runScript: ../scripts/fetch-otp.js
- inputText: ${output.otp}
```

## Conditional branching via output

```javascript
// scripts/feature-flag.js
var resp = http.get('${MAESTRO_BASE_URL}/api/flags?user=' + '${MAESTRO_USER_ID}');
var flags = JSON.parse(resp.body);
output.showsNewCheckout = flags.new_checkout === true;
```

```yaml
- runScript: ../scripts/feature-flag.js
- runFlow:
    when:
      true: ${output.showsNewCheckout}
    file: ../subflows/checkout-v2.yaml
- runFlow:
    when:
      false: ${output.showsNewCheckout}
    file: ../subflows/checkout-v1.yaml
```

## Env vars

Pass at CLI:
```bash
maestro test -e BASE_URL=https://staging.example.com -e USER=test@x.com .maestro/flows
```

Read in flow:
```yaml
- inputText: ${USER}
```

Read in script:
```javascript
var url = '${BASE_URL}' + '/api/things';
```

(Yes, string interpolation in scripts uses Maestro template syntax, NOT JS.)

## Mock API server pattern

Bring up a local mock before suite (Express/Mock Service Worker), point app at `http://localhost:3000`, GraalJS hits it for state assertions or test setup. Tear down in CI `after_script`.
