const ws = new WebSocket("ws://localhost:8000/ws/chat");
            const messagesDiv = document.getElementById("messages");
            const messageInput = document.getElementById("messageInput");

            ws.onmessage = (event) => {
                const message = document.createElement("div");
                message.textContent = event.data;
                message.style.padding = "5px";
                message.style.borderBottom = "1px solid #eee";
                messagesDiv.appendChild(message);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            };

            function sendMessage() {
                const message = messageInput.value;
                if (message.trim() !== "") {
                    ws.send(message);
                    messageInput.value = "";
                }
            }