import socket
import json
import datetime
import threading
import logging
import platform

# Configure logging
logging.basicConfig(filename='honeypot.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def handle_client(client_socket, addr, port):
    """Handle incoming client connections."""
    try:
        # Log connection details including the captured port
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

        # Send a fake banner
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
        logging.error(f"Server error on port {port}: {str(e)}")
    finally:
        server.close()

def main():
    # Define a range of ports to listen on (e.g., 1-1024 for common ports, expandable to 65535)
    ports = range(1, 1025)  # Start with common ports; adjust to range(1, 65536) for all ports
    threads = []
    
    for port in ports:
        try:
            thread = threading.Thread(target=start_honeypot, args=(port,))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        except Exception as e:
            logging.error(f"Failed to start honeypot on port {port}: {str(e)}")

    # Keep the main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Honeypot stopped by user.")

if __name__ == "__main__":
    main()
