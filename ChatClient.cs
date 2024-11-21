using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        using (ClientWebSocket socket = new ClientWebSocket())
        {
            Uri serverUri = new Uri("ws://localhost:8765");
            await socket.ConnectAsync(serverUri, CancellationToken.None);
            Console.WriteLine("Connected to the server!");
            
            Task receiveTask = ReceiveMessages(socket);

            while (true)
            {
                string message = Console.ReadLine();
                if (message.ToLower() == "exit")
                {
                    break;
                }

                ArraySegment<byte> bytesToSend = new ArraySegment<byte>(Encoding.UTF8.GetBytes(message));
                await socket.SendAsync(bytesToSend, WebSocketMessageType.Text, true, CancellationToken.None);
            }

            await socket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Client closing", CancellationToken.None);
        }
    }

    static async Task ReceiveMessages(ClientWebSocket socket)
    {
        byte[] buffer = new byte[1024];
        while (true)
        {
            WebSocketReceiveResult result = await socket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
            if (result.MessageType == WebSocketMessageType.Close)
            {
                Console.WriteLine("Server closed connection.");
                break;
            }

            string message = Encoding.UTF8.GetString(buffer, 0, result.Count);
            Console.WriteLine($"Received: {message}");
        }
    }
}
