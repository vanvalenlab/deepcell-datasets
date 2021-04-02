function testEmail(email) {
  // https://stackoverflow.com/a/54088130
  // check that the input string is an well formed email
  email = email.toString().toLowerCase();
  var emailFilter = /^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+.)+([a-zA-Z0-9]{2,4})+$/;
  if (!emailFilter.test(email)) {
    return false;
  }

  // A whitelist of domains to enable registration
  var domainWhitelist = (process.env.DOMAIN_WHITELIST || '.edu').split(',');

  for (let s of domainWhitelist) {
    if (email.endsWith(s)) {
      return true;
    }
  }
  // email is well formed but not in the whitelist
  return false;
};

exports.handler = (event, context, callback) => {
    var error = null;
    if (!testEmail(event.userName)) {
      error = new Error('Only university/academic email domains are supported.');
    }
    callback(error, event);
};
