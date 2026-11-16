/* tabs.js — small extras for the tabs on a season log (Wild Rift).

   The tabs already work without this file: they're radio buttons styled as
   tabs (see _includes/season-log.html and the "Tabs" part of reads.css).
   This only adds two conveniences:
   - A link ending in #season, #player or #history opens that tab, so a
     tab can be shared or bookmarked.
   - Picking a tab updates the address bar to match, without adding a
     Back-button step for every tap.
   - A link to a single entry (#e-...) switches to Journal and scrolls to it.
*/
(function () {
  'use strict';
  var radios = document.querySelectorAll('input[name="log-tab"]');
  if (!radios.length) return;

  // Open whichever tab the address asks for. A link to one entry (#e-...)
  // opens Journal, where the entries are, and scrolls to it.
  // Tripped me up: at first only tab names were handled, so following an
  // entry link while another tab was open left the entry hidden.
  function openFromHash() {
    var want = window.location.hash.slice(1);
    if (!want) return;
    var matched = false;
    radios.forEach(function (r) { if (r.dataset.tab === want) { r.checked = true; matched = true; } });
    if (matched) return;
    var target = document.getElementById(want);
    var journal = document.getElementById('tab-journal');
    if (target && journal && target.closest('.panel-journal')) {
      journal.checked = true;
      target.scrollIntoView();
    }
  }

  radios.forEach(function (r) {
    r.addEventListener('change', function () {
      // Journal is the default, so it gets a clean address with no #.
      var hash = r.dataset.tab === 'journal' ? '' : '#' + r.dataset.tab;
      history.replaceState(null, '', window.location.pathname + window.location.search + hash);
    });
  });

  openFromHash();
  window.addEventListener('hashchange', openFromHash);
})();
