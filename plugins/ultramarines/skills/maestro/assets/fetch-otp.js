// Fetch latest OTP from local Mailpit instance.
// Mailpit must run at localhost:8025 with app SMTP pointed there.
// Pairs with subflow-auth.yaml. Sets output.otp for ${output.otp} in flow.

var resp = http.get('http://localhost:8025/api/v1/messages?limit=1');

if (resp.status !== 200) {
  output.otp = '';
  console.log('Mailpit fetch failed: status=' + resp.status);
} else {
  var json = JSON.parse(resp.body);
  if (!json.messages || json.messages.length === 0) {
    output.otp = '';
    console.log('No messages in Mailpit inbox');
  } else {
    var snippet = json.messages[0].Snippet || '';
    var match = snippet.match(/\b(\d{6})\b/);
    output.otp = match ? match[1] : '';
    console.log('OTP extracted: ' + output.otp);
  }
}
