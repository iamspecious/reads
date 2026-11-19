/* log-order.js — the "Oldest first | Newest first" buttons on a log page.

   The page arrives already in its usual order (books oldest first, so they
   read from chapter 1 down; games newest first, so the latest session is on
   top). These buttons let each reader flip it to the way that makes sense
   to them.

   How: the list of entries is the element right after the buttons. Flipping
   it just moves each entry to the front, one by one, which reverses it.
   Nothing is reloaded and links to a single entry (#e-...) keep working.

   The choice is remembered in this browser only, separately for books and
   games, so a reader who likes newest first gets it on every book.
   Tripped me up (well, nearly): saved settings can be blocked (private
   windows), so every read and write is wrapped in try/catch and the page
   works the same without them.
*/
(function () {
  'use strict';
  document.querySelectorAll('.order-toggle').forEach(function (box) {
    var list = box.nextElementSibling;
    if (!list) return;
    var key = 'reads-order-' + (box.dataset.kind || 'log');
    var current = box.dataset.order;

    function show(order) {
      box.querySelectorAll('button').forEach(function (b) {
        b.setAttribute('aria-pressed', b.dataset.want === order ? 'true' : 'false');
      });
    }

    function flipTo(order) {
      if (order === current) return;
      var items = Array.prototype.slice.call(list.children);
      items.forEach(function (el) { list.insertBefore(el, list.firstChild); });
      current = order;
      show(order);
    }

    box.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        flipTo(b.dataset.want);
        try { localStorage.setItem(key, b.dataset.want); } catch (e) { /* not saved, still flipped */ }
      });
    });

    var saved = null;
    try { saved = localStorage.getItem(key); } catch (e) { saved = null; }
    if (saved === 'oldest' || saved === 'newest') flipTo(saved);

    // Only one entry (or none): nothing to flip, so no buttons.
    if (list.children.length > 1) box.hidden = false;

    // A link to one entry should still land on it after a flip.
    if (window.location.hash.indexOf('#e-') === 0) {
      var target = document.getElementById(window.location.hash.slice(1));
      if (target) target.scrollIntoView();
    }
  });
})();
