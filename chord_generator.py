import random

# Global Variables for constructing key and chord progressions
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
major_intervals = [2, 2, 1, 2, 2, 2]  # Whole, Whole, Half, Whole, Whole, Whole
minor_intervals = [2, 1, 2, 2, 1, 2]  # Whole, Half, Whole, Whole, Half, Whole

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
        raise ValueError("Invalid scale type. Choose 'major' or 'minor'.")

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
    
    return key, scale_type, progression