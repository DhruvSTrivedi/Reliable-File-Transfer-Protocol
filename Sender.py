import socket
import struct
import sys


def create_packets(filename):
    """Reads a file and creates a list of packets from it.
    
    Each packet contains:
        int type ->    0: Ack  1: Data   2: EOF
        int seq_num ->  sequence number of the packet
        int length ->  length of the string data
        string data -> String with max length 500

    Args:
        filename: The name of the file to read from.

    Returns:
        List of packets.
    """
    packets = []
    seq_num = 0
    with open(filename, 'rb') as file:
        while True:
            data = file.read(500)
            if not data:
                break
            length = len(data)
            packet = struct.pack('!iii500s', 1, seq_num, length, data)
            packets.append(packet)
            seq_num += 1
    return packets


def send_file(receiver_host, receiver_port, sender_port, timeout, filename):
    """Sends a file in form of packets to the receiver via UDP socket.

    Args:
        receiver_host: The hostname of the receiver.
        receiver_port: UDP port number for the receiver.
        sender_port: UDP port number for the sender.
        timeout: Waiting time for receiving acknowledgements (in seconds).
        filename: The name of the file to send.
    """
    print(f"Sending File: {filename}")
    packets = create_packets(filename)
    acks_received = set()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("", sender_port))
        while len(acks_received) < len(packets):
            for i, packet_to_send in enumerate(packets):
                if i not in acks_received:
                    sock.sendto(packet_to_send, (receiver_host, receiver_port))
                    with open("seqnum.log", "a") as log_file:
                        log_file.write(f"{i}\n")

            sock.settimeout(timeout)
            try:
                ack_data, _ = sock.recvfrom(512)
                _, seq_num, _, _ = struct.unpack('!iii0s', ack_data)
                acks_received.add(seq_num)
                with open('ack.log', 'a') as log_file:
                    log_file.write(f"{seq_num}\n")
            except socket.timeout:
                continue

        eot_packet = struct.pack('!iii500s', 2, len(packets), 0, b'')
        sock.sendto(eot_packet, (receiver_host, receiver_port))
        with open('seqnum.log', 'a') as log_file:
            log_file.write(f"{len(packets)}\n")

        while True:
            try:
                eot_data, _ = sock.recvfrom(512)
                _, eot_seq_num, _, _ = struct.unpack("!iii0s", eot_data)
                if eot_seq_num == len(packets):
                    with open('ack.log', 'a') as log_file:
                        log_file.write(f"{eot_seq_num}\n")
                    break
            except socket.timeout:
                sock.sendto(eot_packet, (receiver_host, receiver_port))

        print("File sent successfully.")


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Enter valid number of arguments')
        sys.exit(1)

    receiver_host = sys.argv[1]
    try:
        receiver_port = int(sys.argv[2])
        sender_port = int(sys.argv[3])
        timeout = int(sys.argv[4]) / 1000  # Convert milliseconds to seconds
    except ValueError:
        print("Invalid parameter type. Please enter correct values.")
        sys.exit(1)

    filename = sys.argv[5]
    send_file(receiver_host, receiver_port, sender_port, timeout, filename)
