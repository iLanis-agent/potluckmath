/* Potluck math - exact arithmetic, labeled planning norms.
   Labeled norms shown in the UI: appetite per guest (light 400 g, normal 550 g,
   hungry 700 g); grams per serving by dish (main 350, side 150, salad 100,
   dessert 120); servings per batch (main 8, side 10, salad 12, dessert 12);
   drinks 1.5 per guest per hour, ice 150 g per guest per hour. */
(function (root) {
  'use strict';

  var APPETITE = { light: 400, normal: 550, hungry: 700 };
  var DISHES = {
    main:    { batch: 8,  grams: 350 },
    side:    { batch: 10, grams: 150 },
    salad:   { batch: 12, grams: 100 },
    dessert: { batch: 12, grams: 120 }
  };

  function num(v, name) {
    if (typeof v !== 'number' || !isFinite(v)) throw new Error(name + ' must be a number');
    return v;
  }
  function count(v, name, max) {
    v = num(v, name);
    if (!Number.isInteger(v)) throw new Error('count ' + name + ' in whole numbers');
    if (v < 0) throw new Error(name + ' must be zero or more');
    if (v > max) throw new Error('keep ' + name + ' under ' + (max + 1) + ' (labeled)');
    return v;
  }
  function dishOf(dish) {
    var d = DISHES[String(dish).toLowerCase()];
    if (!d) throw new Error('dish is main, side, salad or dessert (labeled)');
    return d;
  }

  function coverage(guests, appetite, mains, sides, salads, desserts) {
    guests = count(guests, 'guests', 100);
    if (guests === 0) throw new Error('guests must be positive');
    var a = APPETITE[String(appetite).toLowerCase()];
    if (a === undefined) throw new Error('appetite is light, normal or hungry (labeled)');
    mains = count(mains, 'mains', 100); sides = count(sides, 'sides', 100);
    salads = count(salads, 'salads', 100); desserts = count(desserts, 'desserts', 100);
    var needed = guests * a;
    var brought = mains * DISHES.main.grams + sides * DISHES.side.grams +
                  salads * DISHES.salad.grams + desserts * DISHES.dessert.grams;
    var pct = Math.round(brought / needed * 1000) / 10;
    var verdict = pct < 90 ? 'short - ask for another dish' : pct <= 120 ? 'just right' : 'a feast';
    return { needed_g: needed, brought_g: brought, coverage_pct: pct, verdict: verdict };
  }

  function batches(portions, dish) {
    portions = count(portions, 'portions', 200);
    if (portions === 0) throw new Error('portions must be positive');
    var d = dishOf(dish);
    var n = Math.ceil(portions / d.batch);
    var leftover = n * d.batch - portions;
    var verdict = leftover === 0 ? 'exact' : leftover <= 2 ? 'a little extra' : 'plenty of seconds';
    return { batches: n, servings: n * d.batch, leftover: leftover, verdict: verdict };
  }

  function drinks(guests, hours) {
    guests = count(guests, 'guests', 100);
    if (guests === 0) throw new Error('guests must be positive');
    hours = count(hours, 'hours', 12);
    if (hours === 0) throw new Error('hours must be positive');
    var total = guests * Math.ceil(hours * 1.5);
    var ice = guests * hours * 150;
    var verdict = hours <= 1 ? 'a short toast' : hours <= 4 ? 'an evening' : 'a long night';
    return { drinks: total, ice_g: ice, verdict: verdict };
  }

  var api = { coverage: coverage, batches: batches, drinks: drinks };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.PotluckMath = api;
})(typeof window !== 'undefined' ? window : globalThis);
