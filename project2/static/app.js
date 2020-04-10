document.addEventListener("DOMContentLoaded", ()=>{
   console.log("DOM Loaded");

    // Connect Socket
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When socket is connected
    socket.on('connect', ()=>{
        console.log("Socket connesscted");
        const btn = document.querySelector("#sendMsgBtn");
        btn.addEventListener("click", ()=>{
            let timestamp1 = new Date();
            timestamp1 = timestamp1.toLocaleTimeString().toUpperCase();
            let msg = "[" + timestamp1 + "]: ";
            msg += document.querySelector("#msgText").value;
            socket.emit("send msg", msg)
        });
    });

    socket.on("user connected", (msg)=>{
        console.log(msg);
    });

    let timestamp = new Date();
    timestamp = timestamp.toLocaleTimeString().toUpperCase();
    document.querySelector("#msgText").addEventListener("focus", ()=>{
        socket.emit("join room", timestamp);
    });

    socket.on("joined room", (msg)=>{
       let messages = document.querySelector("#messages");
       let message = document.createElement("li");
       message.innerHTML = msg;
       messages.appendChild(message);
    });


    socket.on("msg sent", (msg)=>{
        let messages = document.querySelector("#messages");
        let message = document.createElement("li");
        message.innerHTML= msg;
        messages.appendChild(message);
        document.getElementById("msgText").value = "";
    });


});