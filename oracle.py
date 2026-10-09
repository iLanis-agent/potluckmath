#!/usr/bin/env python3
# Oracle for potluckmath. Mirrors engine.js float ops exactly (IEEE 754 doubles).
import math, json, os

APPETITE = {'light': 400, 'normal': 550, 'hungry': 700}
DISHES = {'main': (8, 350), 'side': (10, 150), 'salad': (12, 100), 'dessert': (12, 120)}

def jround(x):
    return math.floor(x + 0.5)

def coverage(guests, appetite, mains, sides, salads, desserts):
    a = APPETITE[appetite]
    needed = guests * a
    brought = mains * 350 + sides * 150 + salads * 100 + desserts * 120
    pct = jround(brought / needed * 1000) / 10
    verdict = 'short - ask for another dish' if pct < 90 else 'just right' if pct <= 120 else 'a feast'
    return {'needed_g': needed, 'brought_g': brought, 'coverage_pct': pct, 'verdict': verdict}

def batches(portions, dish):
    b, _ = DISHES[dish]
    n = math.ceil(portions / b)
    leftover = n * b - portions
    verdict = 'exact' if leftover == 0 else 'a little extra' if leftover <= 2 else 'plenty of seconds'
    return {'batches': n, 'servings': n * b, 'leftover': leftover, 'verdict': verdict}

def drinks(guests, hours):
    total = guests * math.ceil(hours * 1.5)
    ice = guests * hours * 150
    verdict = 'a short toast' if hours <= 1 else 'an evening' if hours <= 4 else 'a long night'
    return {'drinks': total, 'ice_g': ice, 'verdict': verdict}

FUN = {'coverage': coverage, 'batches': batches, 'drinks': drinks}

CASES = [
  {'card':'coverage','args':[8,'normal',2,3,2,2]}, {'card':'coverage','args':[8,'normal',4,4,2,2]},
  {'card':'coverage','args':[8,'normal',6,5,3,3]}, {'card':'coverage','args':[12,'light',2,2,2,1]},
  {'card':'coverage','args':[12,'hungry',3,3,2,2]}, {'card':'coverage','args':[20,'normal',4,4,3,2]},
  {'card':'coverage','args':[4,'hungry',1,1,1,1]}, {'card':'coverage','args':[30,'light',6,6,4,4]},
  {'card':'coverage','args':[8,'normal',0,0,0,0]},  {'card':'coverage','args':[15,'normal',3,4,2,3]},
  {'card':'coverage','args':[6,'light',1,2,1,1]},   {'card':'coverage','args':[25,'hungry',8,7,5,4]},
  {'card':'coverage','args':[0,'normal',2,2,2,2],'error':'positive'},
  {'card':'coverage','args':[8,'normal',-1,0,0,0],'error':'zero or more'},
  {'card':'coverage','args':[8,'ravenous',2,2,2,2],'error':'appetite is'},
  {'card':'coverage','args':[8,'normal',2.5,0,0,0],'error':'whole numbers'},
  {'card':'coverage','args':[150,'normal',2,2,2,2],'error':'under 101'},
  {'card':'batches','args':[8,'main']},   {'card':'batches','args':[9,'main']},
  {'card':'batches','args':[16,'main']},  {'card':'batches','args':[17,'main']},
  {'card':'batches','args':[10,'side']},  {'card':'batches','args':[11,'side']},
  {'card':'batches','args':[21,'side']},  {'card':'batches','args':[12,'salad']},
  {'card':'batches','args':[13,'salad']}, {'card':'batches','args':[24,'dessert']},
  {'card':'batches','args':[25,'dessert']},{'card':'batches','args':[100,'main']},
  {'card':'batches','args':[1,'salad']},  {'card':'batches','args':[55,'side']},
  {'card':'batches','args':[0,'main'],'error':'positive'},
  {'card':'batches','args':[9,'roast'],'error':'dish is'},
  {'card':'batches','args':[2.5,'main'],'error':'whole numbers'},
  {'card':'batches','args':[250,'main'],'error':'under 201'},
  {'card':'drinks','args':[8,1]},   {'card':'drinks','args':[8,2]},
  {'card':'drinks','args':[8,3]},   {'card':'drinks','args':[12,4]},
  {'card':'drinks','args':[4,1]},   {'card':'drinks','args':[20,5]},
  {'card':'drinks','args':[6,6]},   {'card':'drinks','args':[30,2]},
  {'card':'drinks','args':[15,3]},  {'card':'drinks','args':[2,12]},
  {'card':'drinks','args':[50,4]},  {'card':'drinks','args':[10,8]},
  {'card':'drinks','args':[0,2],'error':'positive'},
  {'card':'drinks','args':[8,0],'error':'positive'},
  {'card':'drinks','args':[8,2.5],'error':'whole numbers'},
  {'card':'drinks','args':[8,13],'error':'under 13'},
]

out = []
for c in CASES:
    row = dict(c)
    if 'error' not in c:
        row['expect'] = FUN[c['card']](*c['args'])
    out.append(row)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expected.json')
with open(path, 'w') as fh:
    json.dump(out, fh, indent=1)
    fh.write('\n')
print(len(out), 'cases written')
