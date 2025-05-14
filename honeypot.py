import socket
import json
import datetime
import threading
import logging
import platform
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(filename='honeypot.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def handle_client(client_socket, addr, port):
    """Handle incoming client connections."""
    try:
        data = client_socket.recv(1024).decode('utf-8', errors='ignore')
        log_entry = {
            'timestamp': str(datetime.datetime.now()),
            'ip': addr[0],
            'port': addr[1],
            'captured_port': port,
            'data': data
        }
        logging.info(json.dumps(log_entry))
        print(f"Connection from {addr[0]}:{addr[1]} on port {port} - Data: {data}")
        client_socket.send(b"SSH-2.0-TonyHoneypot\r\n")
    except Exception as e:
        logging.error(f"Error handling client {addr[0]} on port {port}: {str(e)}")
    finally:
        client_socket.close()

def start_honeypot(port):
    """Start the honeypot server on a specific port."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if platform.system() != 'Windows':
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('0.0.0.0', port))
        server.listen(5)
        print(f"Honeypot listening on 0.0.0.0:{port}...")
        while True:
            client_socket, addr = server.accept()
            client_handler = threading.Thread(
                target=handle_client, args=(client_socket, addr, port))
            client_handler.start()
    except Exception as e:
        logging.error(f"Failed to bind on port {port}: {str(e)}")
        print(f"Skipping port {port}: {str(e)}")
    finally:
        server.close()

def main():
    ports = [21, 22, 23, 80, 443, 999, 8080]  # Added 22, 21, 23, 999
    with ThreadPoolExecutor(max_workers=7) as executor:  # Adjusted for 7 ports
        for port in ports:
            executor.submit(start_honeypot, port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Honeypot stopped by user.") 
