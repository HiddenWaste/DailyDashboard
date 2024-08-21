"""
    This is the file where I will be building a prototype of an interactive music generator

    using the functions and such I have built up in chord_generator.py and any that need to be made later on

    Some initial Ideas:
        - A Gui Screen where you can select the key, scale type, (synthdef if supercolldier), and progression pattern from the lists
        - Choose to generate a supercollider script or a midi file

        - (Later) Create a sort of 'supercollider decoder' that could parse the supercollider code to
                test the sound prior to generating either a midi file or a supercollider script

    Initial Supercollider Decoder Idea Pseudo Code:

    def supercollider_decoder(supercollider_script):
        # Take the script either line by line or in chunks
                # If you can take chunks and send them to supercollider to play, that would be best, run a synthdef and then the pbind
                # Maybe split by semicolon as that is what ends each command?
        # Send the script to supercollider to play
            # If it plays, then the script is good

    Initial Issues/Concerns:
        - The feasibility of coding this to a useable state with python and tkinter
        - How to even code this
        - Would using Javascript to create a web app for this I can display directly on my gatsby site for this be better?
            - With JavaScript and my Gatsby Site, would I be able to make supercollider sounds and sound effects play throughout my site?
        - What is the upper limit to this on python? 
            - GUI design?
            - Processing Speed?
            - Ease of Use?
"""

import tkinter as tk   # Used for a GUI
import chord_generator as cg

def main():

    # Create the main window
    window = tk.Tk()                    # Create the main window
    window.title("Music Generator")    # Set the title of the window
    window.geometry("400x400")          # Set the size of the window

    # Create the key selection dropdown
    key_label = tk.Label(window, text="Select a Key:")
    key_label.pack()

    # Make the window never close
    window.mainloop()

if __name__ == "__main__":
    main()