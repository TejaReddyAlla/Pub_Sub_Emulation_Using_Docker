setInterval(function() { setAlertsTopics(); }, 1000);

var topics = [
    "**** Available Carriers ****",
    "1 : mint",
    "2 : T-mobile",
    "3 : AT&T",
    "4 : Lyka",
    "5 : JIO",
    "6 : Airtel",
    "7 : Verizon",
    "8 : BSNL",
    "9 : Variance",
    "10 : Vodafone",
    "11 : Idea",
    "12 : Boost",
    "13 : Metro",
    "14 : Sprint",
    "15 : Visible"
]

printTopics();

function printTopics() {
    for (i in topics) {
        $("#printTopicsDiv").append("<li class='pl-5 ml-5 mb-1'>" + topics[i] + "</li>");
    }
}

/* setAlertsTopics();
 */
function setAlertsTopics() {
    $.ajax({
        type: "GET",
        url: window.location.pathname + "/notifications",
        dataType: "json"
    }).done(function(data) {
        notifications = data["notifications"];
        topics = data["topics"];
        printNotifications(notifications);
    });
}


function getSubTopics() {
    $.ajax({
        type: "GET",
        url: window.location.pathname + "/getSubTopics",
        dataType: "json"
    }).done(function(data) {
        console.log(data);
        printSubbedTopics(data);
    });
}


function printSubbedTopics(subbedtopics) {
    $("#subbedTopics >").remove();
    $.each(subbedtopics, function(i, item) {
        $('#subbedTopics').append("<li class='pl-5 ml-5 mb-1'>" + item + "</li>");
    });
}

function printNotifications(notifications) {
    var index = 1;
    $("#notifications >").remove();
    $.each(notifications, function(key, item) {
        item.forEach((notification, i) => {
            $('#notifications').append("<ul class='ml-2 mb-1'>" + String(index++) + ") \"" + notification + "\"<i> from topic </i>\"" + key + "\"</ul>");
        });
    });
}

function subscribe() {
    var form = $("#subForm");
    var url = window.location.pathname;
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function(data) {
            window.alert("Subscribed")
        },
        error: function(data) {
            window.alert("Failed to Subscribe")
        }
    });
}

function unSubscribe() {
    var form = $("#subForm");
    var url = "http://localhost:8001/unsubscribe/" + window.location.pathname.split('/')[2];
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function(data) {
            window.alert("Un Subscribed")
        },
        error: function(data) {
            window.alert("Failed to UnSubscribe")
        }
    });
}