// Generic 6-digit OTP extractor from arbitrary email body string.
// Use when fetch-otp.js inbox shape differs (e.g. SendGrid, Postmark webhook capture).
//
// Inputs (set via ${output.X} from prior runScript):
//   output.emailBody — raw email body string
// Outputs:
//   output.otp — 6-digit code, or '' if none found

var body = output.emailBody || '';

// Try common patterns in order of specificity
var patterns = [
  /verification code is[:\s]+(\d{6})/i,
  /your code[:\s]+(\d{6})/i,
  /\b(\d{6})\b/  // last-resort: any standalone 6-digit run
];

output.otp = '';
for (var i = 0; i < patterns.length; i++) {
  var m = body.match(patterns[i]);
  if (m) {
    output.otp = m[1];
    break;
  }
}

console.log('OTP extracted: ' + (output.otp || '(none)'));
