from Arpeggio import Arpeggio
from Note import Note

def get_arpeggio_from_name(fretboard: list[list[str]], chord_name: str, span: int) -> list[Arpeggio]:
    """
    Given a chord with name such as Amaj7 and span number
    - parse the name into root note and chord type
    - get the intervals for chord type (maj7 = [maj3, min3, maj3] = [4, 3, 4])
    - use recursive generate function to get all arpeggio possibilities
    within a span fret box for each starting note

    Return a list of arpeggios
    """
    root_note, chord_type = parse_chord_name(chord_name)
    arpeggios = []
    desired_notes = get_desired_notes(root_note=root_note, chord_type=chord_type)

    for string in range(len(fretboard)):
        for fret in range(len(fretboard[string])):
            if fretboard[string][fret] == root_note:
                arpeggios.extend(generate_arpeggio(fretboard, fret, fret, span, desired_notes, [Note(string, fret)]))

    return arpeggios


def parse_chord_name(chord_name: str) -> tuple[str, str]:
    """
    Return the chord name and chord type
    """
    if chord_name[1] == '#':
        # Sharp note
        return chord_name[0:2], chord_name[2:]
    
    return chord_name[0], chord_name[1:]


def get_desired_notes(root_note, chord_type) -> set[str]:
    """
    Get the note names for an arpeggio
    For example Amaj7 -> [A, C#, E, G#]
    """
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    chord_type_intervals = {
        'maj7': [4, 3, 4],
        'min7': [3, 4, 3],
        '7': [4, 3, 3],
    }
    desired_notes = set()
    desired_notes.add(root_note)
    current_index = notes.index(root_note)
    for interval in chord_type_intervals[chord_type]:
        current_index = (current_index + interval) % 12
        desired_notes.add(notes[current_index])
    return desired_notes


def generate_arpeggio(fretboard: list[list[str]], min_note_fret: int, max_note_fret: int, span: int, desired_notes: set[str], notes: list[Note]) -> list[Arpeggio]:
    """
    Recursively generate arpeggios
    """
    if len(notes) == len(desired_notes):
        return [Arpeggio(notes)]
    
    span_remaining = span - (abs(min_note_fret - max_note_fret))
    fret_box_max = min(max_note_fret + span_remaining, len(fretboard[0]))
    fret_box_min = max(0, min_note_fret - span_remaining)
    most_recent_note = notes[-1]
    # TODO: store the note names better to not recompute every turn
    remaining_desired_notes = desired_notes.difference([fretboard[note.string][note.fret] for note in notes])
    arpeggios = []

    def recursive_step(string, fret):
        if fretboard[string][fret] in remaining_desired_notes:
            next_note = Note(string=string, fret=fret)
            arpeggios.extend(generate_arpeggio(fretboard, min(min_note_fret, fret), max(max_note_fret, fret), span, desired_notes, notes + [next_note]))
    
    # Go right of the most recent note on the same string first
    for fret in range(most_recent_note.fret + 1, fret_box_max):
        recursive_step(most_recent_note.string, fret)

    if most_recent_note.string + 1 > len(fretboard) - 1:
        # Early exit if we're done with the fretboard, could be empty
        return arpeggios
    
    # Go over the next string within the fret box
    for fret in range(fret_box_min, fret_box_max):
        recursive_step(most_recent_note.string + 1, fret)

    return arpeggios