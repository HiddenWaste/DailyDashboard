# Interacting with supercollider via subprocess ( DOES NOT WORK CURRENTLY )

# import subprocess       # Import the subprocess module

# # Simple create and run functions written by Chat
# def create_supercollider_script(script_content, filename="chord_progression.scd"):
#     with open(filename, 'w') as file:
#         file.write(script_content)
#     return filename

# def run_supercollider_script(filename):
#     # Assuming scsynth (SuperCollider server) is in your PATH
#     process = subprocess.Popen(['sclang', filename])
#     process.wait()  # Wait for the process to complete

# # Example usage
# script_content = """
# s.boot;
# { SinOsc.ar(440, 0, 0.5).play }.fork;
# s.quit;
# """

# filename = create_supercollider_script(script_content)
# run_supercollider_script("chord_progression.scd")


# ----------------------------------------------------

from pythonosc import udp_client
import time

def send_message(client, address, *args):
    client.send_message(address, args)

def start_supercollider_server():
    client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
    # Load SynthDef from SuperCollider (you must have it preloaded in SC)
    send_message(client, "/d_load", "/synthdefs.scd")
    return client

def play_synth(client, synth_name, *args):
    send_message(client, "/s_new", synth_name, -1, 0, 0, *args)

def stop_synth(client, node_id):
    send_message(client, "/n_free", node_id)

def quit_supercollider(client):
    send_message(client, "/quit")

# Example usage
client = start_supercollider_server()
time.sleep(1)  # Wait for server to boot
play_synth(client, "chord", "freq", 440)
time.sleep(2)
stop_synth(client, 1000)
quit_supercollider(client)
