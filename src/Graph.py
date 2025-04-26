from heapq import heappop, heappush
from math import inf
from random import randint
from Arpeggio import Arpeggio
from Note import Note
import generate_arpeggio

class Graph:
    def __init__(self):
        self.source = Arpeggio([Note(string=randint(0, 5), fret=randint(0,20))])
        self.sink = Arpeggio([Note(string=-2, fret=-2)])

        self.adj_list = dict()
        self.adj_list[self.source] = []

        self.current_layer = [self.source]

    
    def add_arpeggio(self, chord_name: str, fretboard: list[list[str]], span: int):
        next_layer = []

        arpeggios = generate_arpeggio.get_arpeggio_from_name(fretboard=fretboard, chord_name=chord_name, span=span)

        for arpeggio in arpeggios:
            for current_layer_arpeggio in self.current_layer:
                # Minus operator is always non-negative
                current_edge_weight = current_layer_arpeggio - arpeggio
                self.adj_list[current_layer_arpeggio].append((current_edge_weight, arpeggio))

            self.adj_list[arpeggio] = []
            next_layer.append(arpeggio)

        self.current_layer = next_layer


    def add_sink(self) -> None:
        """
        Add the sink node to the end of the graph which is connected to all the fingerings for the last chord
        """
        for current_layer_voicing in self.current_layer:
            self.adj_list[current_layer_voicing].append((0, self.sink))

        self.adj_list[self.sink] = []


    def shortest_path(self) -> dict:
        """
        Use dijstras algorithm to find the shortest path in the graph

        Return the path as a list of arpeggios
        """
        
        priority_queue = []
        prev = dict()
        # Keep distances in a dict too for faster lookup
        dist = dict()

        # Initialize previous to have source with a previous of None
        prev[self.source] = None
        
        for vertex in self.adj_list.keys():
            if vertex == self.source:
                heappush(priority_queue, (0, vertex))
                dist[vertex] = 0
            else:
                heappush(priority_queue, (inf, vertex))
                dist[vertex] = inf
        
        while len(priority_queue) > 0:
            # Get vertex with the minimum distance
            u_dist, u_value = heappop(priority_queue)

            if u_dist > dist[u_value]:
                # We've already been here
                continue

            for neighbor in self.adj_list[u_value]:
                # Unwrap neighbor tuple
                edge_weight, arpeggio = neighbor
                cur_distance = dist[u_value] + edge_weight

                if cur_distance < dist[arpeggio]:
                    dist[arpeggio] = cur_distance
                    heappush(priority_queue, (cur_distance, arpeggio))
                    prev[arpeggio] = u_value

        return prev
    

    def reconstruct_path(self, shortest_path_prev) -> list[Arpeggio]:
        """
        Take in the shortest path previous values found from the shortest_path function 
        and reconstruct the shortest path from source to sink
        """
        try:
            cur = self.sink
            path = []
            while shortest_path_prev[cur] != self.source:
                previous = shortest_path_prev[cur]
                path.insert(0, previous)
                cur = previous
            return path
        except:
            # This should only be an error if the search constraints were too narrow
            return 'Bad Search Constraints'