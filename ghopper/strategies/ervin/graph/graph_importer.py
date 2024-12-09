from ervin.graph.graph import Graph
from ervin.phase_sequence import PhaseSequence
from ervin.sequence_importer import SequenceImporter
import json


class GraphImporter:
    def from_string(self, sequences: str) -> Graph:
        g = Graph()
        try:
            sequences = self._get_sequences_from_json(sequences)
        except json.JSONDecodeError:
            importer = SequenceImporter()
            sequences = importer.from_string(sequences)

        for sequence in sequences:
            for a,b in sequence.pair_iter():
                if g.has_edge(a,b):
                    weight = g.edges[a,b]['weight']
                    g.update(edges=[(a,b,{'weight': weight + 1})])
                else:
                    g.add_edge(a,b,weight=1)
        
        g_copy = g.copy()
        for a,b in g.edges:
          g.edges[a,b]['weight'] = g.edges[a, b]['weight'] / g_copy.out_degree(a, 'weight')

        return g

    def _get_sequences_from_json(self, string):
        data = json.loads(string)
        sequences  =[]
        for elem in data['output']:
            for sequence in elem['sequences']:
                sequences.append(PhaseSequence(sequence))
        return sequences

