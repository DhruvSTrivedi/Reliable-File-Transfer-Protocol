import sys
import socket
import struct
import random

def send_ack(sock, seqnum, address):
    """Sends an acknowledgement packet for a given sequence number to a specified address.

    Args:
        sock (socket.socket): The UDP socket through which the acknowledgement is sent.
        seqnum (int): The sequence number of the packet being acknowledged.
        address (tuple): The address to which the acknowledgement is sent.
    """
    ack_packet = struct.pack('!iii0s', 0, seqnum, 0, b'')
    sock.sendto(ack_packet, address)

def main(receiver_port, drop_probability, output_filename):
    """Receives file packets from the sender using a UDP socket.

    Args:
        receiver_port (int): The UDP port number used by the receiver.
        drop_probability (float): The probability with which packets are artificially dropped.
        output_filename (str): The name of the file where the received data is saved.
    """
    
    # Initialize socket and bind to the specified port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", receiver_port))

    # Initialize buffer and helper variables
    buffer = {}
    next_expected_seqnum = 0
    packets_received = set()

    while True:
        # Receive packets from the sender
        packet, sender_addr = sock.recvfrom(512)
        packet_type, seqnum, length, data = struct.unpack('!iii500s', packet)
        data = data[:length].decode('utf-8')

        # Simulate packet drop
        drop = random.random() < drop_probability

        # Log the sequence number of the received packet
        with open('arrival.log', 'a') as f:
            f.write(f"{seqnum}\n")

        # Handle EOF packet
        if packet_type == 2:
            send_ack(sock, seqnum, sender_addr)
            packets_received.add(seqnum)
            break

        # Handle data packet
        if packet_type == 1:
            if drop:
                # Log dropped packet and continue
                with open('drop.log', 'a') as log:
                    log.write(f"{seqnum}\n")
                continue
            else:
                send_ack(sock, seqnum, sender_addr)

                if seqnum not in packets_received:
                    packets_received.add(seqnum)

                    if seqnum >= next_expected_seqnum:
                        buffer[seqnum] = data

                    # Write packets in sequence to output file
                    while next_expected_seqnum in buffer:
                        with open(output_filename, 'a') as output_file:
                            output_file.write(buffer[next_expected_seqnum])
                        del buffer[next_expected_seqnum]
                        next_expected_seqnum += 1
                else:
                    continue

    sock.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: <script_name> <receiver_port> <drop_probability> <output_filename>')
        sys.exit(1)

    try:
        receiver_port = int(sys.argv[1])
        drop_probability = float(sys.argv[2])
    except ValueError:
        print("Error: Invalid parameter type. Please check your inputs and try again.")
        sys.exit(1)

    output_filename = sys.argv[3]
    main(receiver_port, drop_probability, output_filename)
