// Progressive enhancement: the lists are complete without this. It adds filters on the works and quotes pages.
// It never rewrites a link hash it does not own, so deep links like works.html#w-15 still scroll to their item.
(function () {
  var chips = document.getElementById("subject-chips");
  var legend = document.getElementById("tier-legend");
  var key = chips ? "subject" : legend ? "tier" : null;
  if (!key) return;
  var items = Array.prototype.slice.call(document.querySelectorAll(key === "subject" ? ".work" : ".q"));
  var count = document.getElementById("count");
  var buttons;
  if (key === "subject") {
    buttons = Array.prototype.slice.call(chips.querySelectorAll("button"));
    chips.hidden = false;
  } else {
    // the legend rows become the filter: one control, not a legend plus a repeat of it
    Array.prototype.slice.call(legend.querySelectorAll("li[data-tier]")).forEach(function (li) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "tierbtn"; b.setAttribute("data-tier", li.getAttribute("data-tier"));
      while (li.firstChild) b.appendChild(li.firstChild);
      li.appendChild(b);
    });
    buttons = Array.prototype.slice.call(legend.querySelectorAll("button"));
  }
  var valid = buttons.map(function (b) { return b.getAttribute("data-" + key) || ""; });
  function apply(value, writeHash) {
    var n = 0;
    items.forEach(function (el) { var show = !value || el.getAttribute("data-" + key) === value; el.hidden = !show; if (show) n++; });
    buttons.forEach(function (b) { var on = (b.getAttribute("data-" + key) || "") === value; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on ? "true" : "false"); });
    count.textContent = (value ? "Showing " + n + " of " + items.length : "Showing all " + items.length) + (key === "subject" ? " books" : " quotes") + (key === "tier" ? (value ? ". Tap the mark again to show all." : ". Tap a mark to show only those.") : "");
    if (writeHash) { try { history.replaceState(null, "", value ? "#" + key + "=" + value : location.pathname + location.search); } catch (e) {} }
  }
  (legend || chips).addEventListener("click", function (ev) {
    var b = ev.target.closest("button"); if (!b) return;
    var v = b.getAttribute("data-" + key) || "";
    if (key === "tier" && b.classList.contains("on")) v = "";   // tapping the active mark clears the filter
    apply(v, true);
  });
  var m = location.hash.toLowerCase().match(new RegExp("^#" + key + "=([a-z]+)$"));
  apply(m && valid.indexOf(m[1]) > -1 ? m[1] : "", false);
})();
