import random
from midiutil import MIDIFile

# Global Variables for constructing key and chord progressions
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

INTERVALS = {
    'major': [2, 2, 1, 2, 2, 2],        # Whole, Whole, Half, Whole, Whole, Whole, Half
    'minor': [2, 1, 2, 2, 1, 2],        # Whole, Half, Whole, Whole, Half, Whole, Whole
    'dorian': [2, 1, 2, 2, 2, 1],       # Whole, Half, Whole, Whole, Whole, Half, Whole
    'mixolydian': [2, 2, 1, 2, 2, 1],   # Whole, Whole, Half, Whole, Whole, Half, Whole
    'phrygian': [1, 2, 2, 2, 1, 2],     # Half, Whole, Whole, Whole, Half, Whole, Whole
    'lydian': [2, 2, 2, 1, 2, 1]        # Whole, Whole, Whole, Half, Whole, Half, Whole
}

SCALE_TYPES = [
    'major', 'minor'
]

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

# Initialize the class

class MusicGenerator:
    def __init__(self, key=None, scale_type=None, progression_pattern=None):    # Default has none, can pass in later?
        self.key = key or random.choice(NOTES)
        self.scale_type = scale_type or random.choice(SCALE_TYPES)
        self.progression_pattern = progression_pattern or random.choice(progression_patterns)
        self.scale = self.generate_scale()
        self.chords = self.generate_chords()
        self.progression = self.generate_chord_progression()

    def generate_scale(self):
        intervals = INTERVALS.get(self.scale_type)
        if not intervals:
            raise ValueError("Invalid scale type.")

        scale = [self.key]
        start_index = NOTES.index(self.key)
        for interval in intervals:
            start_index = (start_index + interval) % len(NOTES)
            scale.append(NOTES[start_index])
        return scale

    def generate_chords(self):
        if self.scale_type == 'major':
            chord_pattern = ['maj', 'min', 'min', 'maj', 'maj', 'min', 'dim']
        elif self.scale_type == 'minor':
            chord_pattern = ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj']
        elif self.scale_type in INTERVALS.keys():
            chord_pattern = ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj']  # Example for other modes
        else:
            raise ValueError("Invalid scale type.")
        
        chords = {f'{i+1}': f'{note}{chord_pattern[i]}' for i, note in enumerate(self.scale[:7])}
        return chords

    def generate_chord_progression(self):
        progression = [self.chords[degree] for degree in self.progression_pattern]
        return progression

    def generate_supercollider_script(self):
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
        degree_array = ', '.join(self.progression_pattern)  # Keep degrees as string
        
        # Now Create a Pbind to play the chord progression on the chosen synth
        pbind = f"""
        Pbind(
            \\instrument, \{chosen_synthdef},           // Use the chosen synth
            \\dur, 0.5,                                  // Duration of each note
            \\amp, 0.2,                                  // Amplitude of each note
            \\degree, Pseq([ {degree_array} ], inf),     // A Pseq that cycles through the progression's notes (degrees) the inf means it will loop forever
            \\scale, Scale.{self.scale_type},               // The scale to use
            \\root, {NOTES.index(self.key)},                             
            \\octave, 4
        ).play;
        """

        # Append to supercollider content
        supercollider_content += synthdef + '\n'                    # Add the chosen synthdef
        supercollider_content += pbind + '\n' + 'Server.killAll'       # Add the Pbind and killswitch

        return supercollider_content
        pass

    def generate_midi_file(self):
        # Implement the MIDI file generation as before
        pass

# Example usage:
generator = MusicGenerator()
print(f"Generated Progression: {generator.progression}\n Key: {generator.key}\n Scale Type: {generator.scale_type}\n Progression Pattern: {generator.progression_pattern}\n\n")

generatorB = MusicGenerator()
print(f"Generated Progression: {generatorB.progression}\n Key: {generatorB.key}\n Scale Type: {generatorB.scale_type}\n Progression Pattern: {generatorB.progression_pattern}\n\n")