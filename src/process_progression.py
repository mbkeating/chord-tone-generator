from math import inf
import random
from Arpeggio import Arpeggio
from Graph import Graph
from Note import Note
from utils import list_of_notes_to_str

def get_fretboard():
    fretboard = [["E"], ["A"], ["D"], ["G"], ["B"], ["E"]]
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

    for string in range(len(fretboard)):
        note_idx = notes.index(fretboard[string][0])
        for _ in range(21):
            note_idx += 1
            fretboard[string].append(notes[note_idx % 12])

    return fretboard


def arpeggio_to_line(arpeggios: list[Arpeggio]):
    line: list[Note] = []
    previous_passing_note = None

    for i in range(len(arpeggios) - 1):
        cur_arpeggio = arpeggios[i]
        next_arpeggio = arpeggios[i + 1]

        cur_arpeggio_passing_note = None
        next_arpeggio_passing_note = None
        passing_note_distance = inf

        for cur_note in cur_arpeggio.notes:
            if cur_note == previous_passing_note:
                continue

            for next_note in next_arpeggio.notes:
                if next_note - cur_note < passing_note_distance:
                    cur_arpeggio_passing_note = cur_note
                    next_arpeggio_passing_note = next_note
                    passing_note_distance = next_note - cur_note

        # Randomly shuffle the array
        cur_arpeggio_notes = cur_arpeggio.notes
        random.shuffle(cur_arpeggio_notes)

        for note in cur_arpeggio_notes:
            if note == previous_passing_note or note == cur_arpeggio_passing_note:
                continue

            line.append(note)

        line.append(cur_arpeggio_passing_note)
        line.append(next_arpeggio_passing_note)

        previous_passing_note = next_arpeggio_passing_note

    final_arpeggio_notes = arpeggios[-1].notes
    random.shuffle(final_arpeggio_notes)

    for note in final_arpeggio_notes:
        if note == previous_passing_note:
            continue

        line.append(note)

    return line


def process_chord_progression(chord_list: list[str], span: int):
    graph = Graph()
    fretboard = get_fretboard()

    for chord_name in chord_list:
        graph.add_arpeggio(chord_name, fretboard, span)

    graph.add_sink()

    shortest_path_prev = graph.shortest_path()

    arpeggios = graph.reconstruct_path(shortest_path_prev)

    return arpeggio_to_line(arpeggios)


if __name__ == "__main__":
    res = process_chord_progression(["Amin7", "D7", "Gmaj7"], 4)
    print(list_of_notes_to_str(res))