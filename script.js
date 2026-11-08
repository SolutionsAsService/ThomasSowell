// Progressive enhancement: the lists work without this; it adds filters on the works and quotes pages.
(function () {
  var chips = document.getElementById("subject-chips") || document.getElementById("tier-chips");
  if (!chips) return;
  var key = chips.id === "subject-chips" ? "subject" : "tier";
  var items = Array.prototype.slice.call(document.querySelectorAll(key === "subject" ? ".work" : ".q"));
  var count = document.getElementById("count");
  var buttons = Array.prototype.slice.call(chips.querySelectorAll("button"));
  chips.hidden = false;
  function apply(value) {
    var n = 0;
    items.forEach(function (el) { var show = !value || el.getAttribute("data-" + key) === value; el.hidden = !show; if (show) n++; });
    buttons.forEach(function (b) { var on = (b.getAttribute("data-" + key) || "") === value; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on ? "true" : "false"); });
    count.textContent = "Showing " + n + " of " + items.length + (key === "subject" ? " books" : " quotes");
    try { history.replaceState(null, "", value ? "#" + key + "=" + value : location.pathname); } catch (e) {}
  }
  chips.addEventListener("click", function (ev) {
    var b = ev.target.closest("button"); if (b) apply(b.getAttribute("data-" + key) || "");
  });
  var m = location.hash.match(new RegExp("^#" + key + "=([a-z]+)$"));
  apply(m ? m[1] : "");
})();
