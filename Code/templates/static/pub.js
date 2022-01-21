function publish() {
    $.ajax({
        type: "POST",
        url: window.location.pathname + "/publish",
        data: $("#publisherForm").serialize(),
        success: function(data) {
            window.alert("Published Successfully")
        },
        error: function(data) {
            window.alert("Failed to Publish")
        }
    });
}

function advertise() {
    $.ajax({
        type: "POST",
        url: window.location.pathname + "/advertise",
        data: $("#publisherForm").serialize(),
        success: function(data) {
            window.alert("Advertised Successfully")
        },
        error: function(data) {
            window.alert("Failed to Advertise")
        }
    });
}

function notify() {
    $.ajax({
        type: "POST",
        url: window.location.pathname + "/advertise",
        data: $("#publisherForm").serialize(),
        success: function(data) {
            window.alert("Notified Successfully")
        },
        error: function(data) {
            window.alert("Failed to Notify")
        }
    });
}