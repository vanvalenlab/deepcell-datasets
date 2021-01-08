exports.handler = (event, context, callback) => {
    var eduRegEx = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+edu))$/i;
    var error = null;
    if (!eduRegEx.test(event.userName)) {
        error = new Error('Only .edu emails are supported.');
    }
    callback(error, event);
};
