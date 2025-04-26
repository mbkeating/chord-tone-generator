from math import inf
from Note import Note
from utils import list_of_notes_to_str

class Arpeggio:
    def __init__(self, notes: list[Note]):
        self.notes = notes


    def __sub__(self, other: "Arpeggio") -> int:
        cur_sub = inf
        for note in self.notes:
            for other_note in other.notes:
                cur_sub = min(note - other_note, cur_sub)

        return cur_sub


    def __lt__(self, other: "Arpeggio") -> bool:
        return self.notes[0] < other.notes[0]


    def __eq__(self, other):
        if len(self.notes) != len(other.notes):
            return False
        
        for i in range(len(self.notes)):
            if self.notes[i] != other.notes[i]:
                return False
        return True


    def __hash__(self) -> int:
        total = 0
        for i in range(len(self.notes)):
            # offset each by the max hash value to keep everything separate
            total += (200 * i) + hash(self.notes[i])

        return total


    def __repr__(self) -> str:
        return list_of_notes_to_str(self.notes)