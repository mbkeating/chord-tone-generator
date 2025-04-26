from Note import Note

def list_of_notes_to_str(notes: list[Note]):
    strings = ['-' for _ in range(6)]
    for i in range(len(notes)):
        string, fret = notes[i].unwrap()
        for i in range(6):
            if i == string:
                strings[i] += str(fret).rjust(2) + ' '
            else:
                strings[i] += '---'

        for i in range(6):
            strings[i] += '-'

    result = ""
    for s in range(len(strings) - 1, -1, -1):
        result += strings[s] + '\n'

    return result