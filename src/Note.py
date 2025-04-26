class Note:
    def __init__(self, string: int, fret: int):
        self.string = string
        self.fret = fret


    def get_fretwise_distance(self, other_note: "Note"):
        return abs(self.fret - other_note.fret)
    

    def unwrap(self) -> tuple[int, int]:
        return self.string, self.fret
    

    def __sub__(self, other: "Note"):
        return abs(self.fret - other.fret) + 2 * abs(self.string - other.string)
    

    def __eq__(self, other: "Note"):
        if other is None:
            return False
        
        return self.string == other.string and self.fret == other.fret
    

    def __lt__(self, other: "Note"):
        if self.string < other.string:
            return True
        
        if self.string > other.string:
            return False
        
        if self.string == other.string:
            return self.fret < other.fret
        

    def __hash__(self):
        """
        Hash the notes assuming 22 is the max fret
        """
        return self.fret + (self.string * 23)