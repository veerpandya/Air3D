// Socket Logic for Chat
var socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("connect", function () {
    socket.emit("message", {
        data: current_user + " Connected",
    });
    var form = $("form").on("submit", function (e) {
        e.preventDefault();
        let user_input = $("input.message").val();
        socket.emit("message", {
            user_name: current_user,
            message: user_input,
        });
        $("input.message").val("").focus();
    });
});
socket.on("response", function (msg) {
    console.log(msg);
    if (typeof msg.user_name !== "undefined") {
        $("h3").remove();
        $("div.message_holder").append(
            '<div><b style="color: #FFFFFF">' +
                msg.user_name +
                "</b> " +
                msg.message +
                "</div>"
        );
    }
});
