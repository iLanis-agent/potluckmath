# Potluck math

Three potluck-planning calculators as a small static site - exact arithmetic,
every borrowed number labeled:

- **Coverage check** - guests and appetite (labeled 400/550/700 g) against
  dishes coming (labeled grams per serving: main 350, side 150, salad 100,
  dessert 120) - coverage percent and a short/just-right/feast verdict.
- **Batch planner** - portions needed become batches to cook (labeled servings
  per batch: main 8, side 10, salad 12, dessert 12), with leftovers counted.
- **Drinks and ice** - guests and hours become drinks (labeled 1.5 per guest
  per hour) and ice (labeled 150 g per guest per hour).

## Files

- `index.html` - landing page
- `app.html` - the three calculators
- `engine.js` - all arithmetic, shared by the page and the tests
- `oracle.py` - independent Python mirror of the engine; regenerates `expected.json`
- `expected.json` - 51 cases (per-card values plus error cases)
- `test.js` - runs the engine against `expected.json` (node test.js)

## Tests

```
python3 oracle.py   # regenerate expected cases
node test.js        # engine vs oracle
```
