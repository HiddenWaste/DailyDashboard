import random
from midiutil import MIDIFile # Midi Library for creating midi files

# Global Variables for constructing key and chord progressions
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
major_intervals = [2, 2, 1, 2, 2, 2]  # Whole, Whole, Half, Whole, Whole, Whole
minor_intervals = [2, 1, 2, 2, 1, 2]  # Whole, Half, Whole, Whole, Half, Whole

# Define the Root Notes
root_notes = {
    'C': 60,
    'C#': 61,
    'D': 62,
    'D#': 63,
    'E': 64,
    'F': 65,
    'F#': 66,
    'G': 67,
    'G#': 68,
    'A': 69,
    'A#': 70,
    'B': 71
}

# presets for weird modes
# dorian_intervals = [2, 1, 2, 2, 2, 1]  # Whole, Half, Whole, Whole, Whole, Half
# mixolydian_intervals = [2, 2, 1, 2, 2, 1]  # Whole, Whole, Half, Whole, Whole, Half
# phrygian_intervals = [1, 2, 2, 2, 1, 2]  # Half, Whole, Whole, Whole, Half, Whole
# lydian_intervals = [2, 2, 2, 1, 2, 1]  # Whole, Whole, Whole, Half, Whole, Half

# Presets for possible progressions
progression_patterns = [['1', '4', '5', '1'],   # Very Basic Pop Progression
                        ['1', '6', '4', '5'],   # The "six four five" progression
                        ['1', '5', '6', '4'], 
                        ['5', '1'],             # the "five one" jazz progression
                        ['2', '5'], 
                        ['2', '5', '1']]

# generate a scale based on the key and type (major or minor)
def generate_scale(key, scale_type):
    if scale_type == 'major':
        intervals = major_intervals
    elif scale_type == 'minor':
        intervals = minor_intervals
    else:
        raise ValueError("Invalid scale type.") # Error message for invalid scale type

    scale = [key]                       # Set the tonic note chosen as the Scale name
    start_index = notes.index(key)      # Start an index pointer at the key's point in the notes array
    for interval in intervals:                                  # For Each interval in scale tyle
        start_index = (start_index + interval) % len(notes)     # Iterate by interval step
        scale.append(notes[start_index])                        # Build the Actual Scale
    return scale

# Create the chords for the scale and to pick the progression out
def generate_chords(scale, scale_type):

    # Define the chords for each scale degree in major and minor scales
    if scale_type == 'major':
        chord_pattern = ['maj', 'min', 'min', 'maj', 'maj', 'min', 'dim']
    elif scale_type == 'minor':
        chord_pattern = ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj']

    # # The 'Weird' Modes
    # elif scale_type == 'dorian':
    #     chord_pattern = ['min', 'min', 'maj', 'maj', 'min', 'dim', 'maj']
    # elif scale_type == 'mixolydian':
    #     chord_pattern = ['maj', 'min', 'dim', 'maj', 'min', 'min', 'maj']
    # elif scale_type == 'phrygian':
    #     chord_pattern = ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj']
    # elif scale_type == 'lydian':
    #     chord_pattern = ['maj', 'maj', 'min', 'dim', 'maj', 'min', 'min']
    
    chords = {f'{i+1}': f'{note}{chord_pattern[i]}' for i, note in enumerate(scale[:7])}  # Limit to 7 notes
    return chords

# Generate the chord progression
def generate_chord_progression(key=None, scale_type=None, progression_pattern=None):

    if not key:
        key = random.choice(notes)  # Pick a random tonic note

    if not scale_type:
        scale_type = random.choice(['major', 'minor'])  # Pick a random scale type

    scale = generate_scale(key, scale_type)         # Generate the Scale
    chords = generate_chords(scale, scale_type)     # Generate the Chords

    if not progression_pattern:                     # Grab a Progression
        progression_pattern =  random.choice(progression_patterns)

    progression = [chords[degree] for degree in progression_pattern]
    
    return key, scale_type, progression, progression_pattern


# ------------------------------------------------------------------------------------------------

"""
    File Generation area of the script

    taking the previously made structural generating functions, to implement into
    file generation to actually create audio!

    First working on a supercollider script, then a midi file generator!

    Supercollider Script Ideas:
        - (Later) Pull a random synthdef from a list
        - Generate a SynthDef (currently chord)
        - Generate a Pbind with the progression pattern
        - Play the Pbind
               - Maybe create different Pbind Presets?
        - Save the script to a .scd file


    Midi File Generator Ideas:
        - Generate a midi file with the chord progression
        - Use a simple midi library to create the file
        - Save the midi file to a .mid file
        - Load the file in your favorite DAW!!

    (Later) Make a gui or paramters to call from other py files to create these, or at least the content for them as generation?
        - Unsure 
"""

# Supercollider Script Generator
def generate_supercollider_script(key, scale_type, progression_pattern):
    # Initialize SuperCollider Script
    supercollider_content = "\ns.boot;\n"

    # Define the SynthDef for the Chord Synth
    synthdef = """
    SynthDef.new(\\chord, {
        arg freq = 440, amp = 0.5, dur = 0.5;
        var env, sig;
        env = EnvGen.kr(Env.perc(0.01, 0.1), doneAction: 2);
        sig = SinOsc.ar(freq, 0, amp) * env;
        Out.ar(0, sig);
    }).add;
    """

    # Convert progression pattern to degrees for SuperCollider
    degree_array = ', '.join(progression_pattern)  # Keep degrees as string
    
    # Define the Pbind for the Chord Progression
    pbind = f"""
    Pbind(
        \\instrument, \\chord,
        \\dur, 0.5,
        \\amp, 0.5,
        \\degree, Pseq([ {degree_array} ], inf),
        \\scale, Scale.{scale_type.capitalize}(), 
        \\root, {notes.index(key)},
        \\octave, 4
    ).play;
    """

    # Append to supercollider content
    supercollider_content += synthdef
    supercollider_content += pbind

    return supercollider_content



def generate_midi_file(key, scale_type, progression_pattern):
    # Create a MIDIFile Object
    midi = MIDIFile(1)  # Just one track for now

    # Add a track name and tempo. The first argument to addTrackName and addTempo is the time to write the event.
    track = 0
    time = 0
    midi.addTrackName(track, time, "Sample Track")
    midi.addTempo(track, time, 120)

    

    # Add the Chord Progression to the MIDI File
    for i, notes in enumerate(progression_notes):
        for note in notes:
            midi.addNote(track, 0, note, time + i * chord_length, chord_length, 100)

    # Save the MIDI File
    with open("chord_progression.mid", "wb") as f:
        midi.writeFile(f)

    return "chord_progression.mid"

# ------------------------------------------------------------------------------------------------


# # Main function to generate a chord progression and supercollider script
# def main():
#     key, scale_type, progression, progression_pattern = generate_chord_progression()

#     print(f"Key: {key}")
#     print(f"Scale Type: {scale_type}")
#     print(f"Progression: {progression}")
#     print(f"Progression Pattern: {progression_pattern}")
#     print("\n")

#     # supercollider_script = generate_supercollider_script(key, scale_type, degrees)

#     # # Save the content of the supercollider script to an scd file
#     # with open("chord_progression.scd", "w") as f:
#     #     f.write(supercollider_script)

#     # # Generate a MIDI file
#     midi_file = generate_midi_file(key, scale_type, progression_pattern)
#     with open("chord_progression.mid", "wb") as f:
#         f.write(midi_file)

#     # print("Supercollider Script:")
#     # print(supercollider_script)

#     # print("MIDI File Generated: chord_progression.mid")

# if __name__ == "__main__":
#     main()