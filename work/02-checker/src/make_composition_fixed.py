"""Build the schema-v1 composition (cover) block for the recorded run from m2's measured map.

  python3 src/make_composition.py <m2-dir> <out-prefix>

Source: `.ultramath/smwgx104w/m2/composition-cover-map.json` (recovered by instrumenting a copy
of the archived refiner; output byte-identical to data/fb1.bin).  This script only re-encodes it
canonically and checks the block's internal invariants and addressed record identities; it does not re-derive the cover.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stagec_schema as S
import stagec_composition as C

m2dir, pref = sys.argv[1:3]
m = json.load(open(os.path.join(m2dir, 'composition-cover-map.json')))
manifest_path = (sys.argv[3] if len(sys.argv) > 3 else
                 'certdata/runs/h1-coverage/coverage-manifest.json')
manifest = json.load(open(manifest_path))['unresolved']['records']
by_batch = {}
for record in manifest:
    # m2's batch_index is an ordinal within each bad*.bin file, whereas the
    # manifest's batch_index is the original position within that whole batch.
    by_batch.setdefault(record['batch'], []).append(record['fine_index'])
assert len(manifest) == 163
metric = dict(w=str(m['metric']['w']), target_child_radius=str(m['metric']['target_child_radius']),
              E_formula=m['metric']['E_formula'], naxis=str(m['metric']['naxis']),
              cells_total_per_parent=str(m['metric']['cells_total_per_parent']),
              inside_cells_per_parent=str(m['metric']['inside_cells_per_parent']),
              cover_criterion=m['metric']['cover_criterion'])

parents = []
for p in m['parents']:
    if p['ok'] != 1:
        raise SystemExit('parent not fully refined: %r' % (p,))
    g = by_batch[p['batch']][p['batch_index']]  # Actual original batch/fine index of the capped record.
    # inside = relation_marks + snap_closed_cells (m2: 515,243 inside = 515,236 marks + 7 snap-closed)
    parents.append(dict(g=g, base=int(metric['cells_total_per_parent']), inside=p['inside_cells'],
                        relation_marks=p['marks'],
                        snap_closed_cells=p['inside_cells'] - p['marks'], fail=0,
                        created=p['created'], inherited=p['inherited'], degree=p['used']))
parents.sort(key=lambda p: p['g'])
children = sorted(c['fb1_index'] for c in m['children'])
links = sorted((c, t) for t, p in enumerate(parents) for c in m['parents'][
    [i for i, q in enumerate(m['parents']) if by_batch[q['batch']][q['batch_index']] == p['g']][0]]['children'])
# the comprehension above is O(n^2); rebuild directly
links = []
for t, p in enumerate(parents):
    src = [q for q in m['parents'] if by_batch[q['batch']][q['batch_index']] == p['g']][0]
    for c in src['children']:
        links.append((c, t))
links.sort()
comp = C.Composition(0, parents, children, links)
blob = comp.to_bytes()
open(pref + '.bin', 'wb').write(blob)
open(pref + '.txt', 'w').write(comp.text())
back = C.Composition.from_bytes(blob)
assert back.to_bytes() == blob and back.text() == comp.text()
errs = C.check_composition([comp], metric=metric, pos=None)
print('composition: parents %d children %d links %d inherited %d'
      % (len(parents), len(children), len(links), sum(p['inherited'] for p in parents)))
print('bytes %d (header 28 + %d B parents + %d B children + %d B links)'
      % (len(blob), 32 * len(parents), 4 * len(children), 4 * len(links)))
print('snap_closed_cells total %d, relation_marks total %d, inside total %d (identity holds: %s)'
      % (sum(p['snap_closed_cells'] for p in parents), sum(p['relation_marks'] for p in parents),
         sum(p['inside'] for p in parents),
         all(p['inside'] == p['relation_marks'] + p['snap_closed_cells'] for p in parents)))
print('internal validation errors:', errs[:3] if errs else 'none')
json.dump(dict(metric=metric, bytes=len(blob), parents=len(parents), children=len(children),
               links=len(links), inherited=sum(p['inherited'] for p in parents),
               source='m2 composition-cover-map.json'),
          open(pref + '.json', 'w'), indent=1, sort_keys=True)
