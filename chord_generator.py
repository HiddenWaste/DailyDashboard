import random
from midiutil import MIDIFile # Midi Library for creating midi files

# Global Variables for constructing key and chord progressions
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

INTERVALS = {
    'major': [2, 2, 1, 2, 2, 2],        # Whole, Whole, Half, Whole, Whole, Whole, Half
    'minor': [2, 1, 2, 2, 1, 2],        # Whole, Half, Whole, Whole, Half, Whole, Whole
    'dorian': [2, 1, 2, 2, 2, 1],       # Whole, Half, Whole, Whole, Whole, Half, Whole
    'mixolydian': [2, 2, 1, 2, 2, 1],   # Whole, Whole, Half, Whole, Whole, Half, Whole
    'phrygian': [1, 2, 2, 2, 1, 2],     # Half, Whole, Whole, Whole, Half, Whole, Whole
    'lydian': [2, 2, 2, 1, 2, 1]        # Whole, Whole, Whole, Half, Whole, Half, Whole
}

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
        intervals = INTERVALS["major"]
    elif scale_type == 'minor':
        intervals = INTERVALS["minor"]
    else:
        raise ValueError("Invalid scale type.") # Error message for invalid scale type
    
    # Create the scale based on the key and intervals
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
    # The 'Weird' Modes
    elif scale_type == 'dorian':
        chord_pattern = ['min', 'min', 'maj', 'maj', 'min', 'dim', 'maj']
    elif scale_type == 'mixolydian':
        chord_pattern = ['maj', 'min', 'dim', 'maj', 'min', 'min', 'maj']
    elif scale_type == 'phrygian':
        chord_pattern = ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj']
    elif scale_type == 'lydian':
        chord_pattern = ['maj', 'maj', 'min', 'dim', 'maj', 'min', 'min']
    
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

    Supercollider Script Ideas:
        - Play the Pbind
               - Maybe create different Pbind Presets?

    Midi File Generator Ideas:
        - Generate a midi file with the chord progression
        - Use a simple midi library to create the file
        - Save the midi file to a .mid file
        - Load the file in your favorite DAW!!

    (Later) Make a gui or paramters to call from other py files to create these, or at least the content for them as generation?
        - Unsure 
"""
# ------------------------------------------------------------------------------------------------


# Supercollider Script Generator
def generate_supercollider_script(key, scale_type, progression_pattern):
    supercollider_content = "\ns.boot;\n\n"  # Initialize the SuperCollider content

    # Collect SynthDef presets from a supercollider file
    with open("synthdefs.scd", "r") as f:
        synthdefs = f.read()
    synthdefs = synthdefs.split('\n\n')     # Split synthdefs by 2 newlines
    synthdef = random.choice(synthdefs)     # Randomly choose one of the synthdefs

    # Extract the synthdef name to call in the Pbind   
    chosen_synthdef = synthdef[14:synthdef.index(',')]  #   First line Example:  'SynthDef.new(\bass, {', Need to skip first 14 characters, and then until the first comma

    # Lines To Debug Synthdef
    # print(f'Chosen Synthdef:\n {chosen_synthdef}') # Debugging
    # print(f'Full Synthdef:\n {synthdef}\n') # Debugging

    # Convert progression pattern to degrees for SuperCollider
    degree_array = ', '.join(progression_pattern)  # Keep degrees as string
    
    # Now Create a Pbind to play the chord progression on the chosen synth
    pbind = f"""
    Pbind(
        \\instrument, \{chosen_synthdef},           // Use the chosen synth
        \\dur, 0.5,                                  // Duration of each note
        \\amp, 0.2,                                  // Amplitude of each note
        \\degree, Pseq([ {degree_array} ], inf),     // A Pseq that cycles through the progression's notes (degrees) the inf means it will loop forever
        \\scale, Scale.{scale_type},               // The scale to use
        \\root, {notes.index(key)},                             
        \\octave, 4
    ).play;
    """

    # Append to supercollider content
    supercollider_content += synthdef + '\n'    # Add the chosen synthdef
    supercollider_content += pbind + '\n'       # Add the Pbind

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
def main():
    key, scale_type, progression, progression_pattern = generate_chord_progression()

    degrees = progression_pattern  # Initialize degrees variable

    supercollider_script = generate_supercollider_script(key, scale_type, degrees)

    # Save the content of the supercollider script to an scd file
    with open("chord_progression.scd", "w") as f:
        f.write(supercollider_script)

    # # Generate a MIDI file
    # midi_file = generate_midi_file(key, scale_type, progression_pattern)
    # with open("chord_progression.mid", "wb") as f:
    #     f.write(midi_file)

    # ------------------------------------------------------------------------------------------------

    # Debugging Prints    
    
    # Chord Generation part
    # print(f"Key: {key}")
    # print(f"Scale Type: {scale_type}")
    # print(f"Progression: {progression}")
    # print(f"Progression Pattern: {progression_pattern}")
    # print("\n")

    # Midi and Supercollider Generation Parts
    # print("MIDI File Generated: chord_progression.mid")
    # print("Supercollider Script:")
    # print(supercollider_script)

if __name__ == "__main__":
    main()