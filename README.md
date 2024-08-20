# DailyDashboard
This is a collection of python code I've developed (alongside a lot of online help, including ChatGPT) that gathers various data and creates a markdown file of said information for me to use in my gatsby site development

# Different Scripts

## chord_generator
Despite the name, this script generates more than chords. It can generate keys, scales, and then midi or supercollider files based off of those generations! Not entirely sure what an end goal with this script will be other than to keep pushing its capabilities and see what I can do! 

Ideas:
- (WIP) Supercollider (.scd) file generation
    - (Not Implemented) A Library of Supercollider synthdefs to pull from
- (WIP) Midi File Generation
- Make each facet callable in other .py scripts

## history_scrape
This is the script I use to get the 'Today In History' information for the daily note. It scrapes the events, births, and deaths, from the wikipedia page for the day; then filters each section based on a score filtering system I've implemented inspired by my interests to limit the number of each shown and make them more likely to be relevant to my interests.

Ideas:
-(WIP) Fine-tune filters
-(NI) Cross-check or include other today in history sources?

## data-functions-testing + genius-data-testing

## sudoku