import socket
import json
import datetime
import threading
import logging

# Configure logging
logging.basicConfig(filename='honeypot.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def handle_client(client_socket, addr):
    """Handle incoming client connections."""
    try:
        # Log connection details
        data = client_socket.recv(1024).decode('utf-8', errors='ignore')
        log_entry = {
            'timestamp': str(datetime.datetime.now()),
            'ip': addr[0],
            'port': addr[1],
            'data': data
        }
        logging.info(json.dumps(log_entry))
        print(f"Connection from {addr[0]}:{addr[1]} - Data: {data}")

        # Send a fake SSH banner to mimic a real server
        client_socket.send(b"SSH-2.0-TonyHoneypot\r\n")
    except Exception as e:
        logging.error(f"Error handling client {addr[0]}: {str(e)}")
    finally:
        client_socket.close()

def start_honeypot(host='0.0.0.0', port=22):
    """Start the honeypot server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"Honeypot listening on {host}:{port}...")
        while True:
            client_socket, addr = server.accept()
            # Handle each client in a separate thread
            client_handler = threading.Thread(
                target=handle_client, args=(client_socket, addr))
            client_handler.start()
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
    finally:
        server.close()

if __name__ == "__main__":
    start_honeypot()

