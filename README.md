# chord-tone-generator
A Graph Engine for Guitar Chord-Tone Soloing Education

## Running code
Update the main function in `src/process_progression.py` with your chord progression then run

`python src/process_progression.py`

## Paper

This engine will be presented at ICMC2025 in June. Paper postprint https://arxiv.org/pdf/2510.19666

### Paper Abstract

We present a graph-based engine for computing chord tone soloing suggestions for guitar students. Chord tone soloing is a fundamental practice for improvising over a chord progression, where the instrumentalist uses only the notes contained in the current chord. This practice is a building block for all advanced jazz guitar theory but is difficult to learn and practice. First, we discuss methods for generating chord-tone arpeggios. Next, we construct a weighted graph where each node represents a chord-tone arpeggio for a chord in the progression. Then, we calculate the edge weight between each consecutive chord's nodes in terms of optimal transition tones. We then find the shortest path through this graph and reconstruct a chord-tone soloing line. Finally, we discuss a user-friendly system to handle input and output to this engine for guitar students to practice chord tone soloing.
