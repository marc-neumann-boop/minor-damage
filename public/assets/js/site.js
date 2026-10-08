/* PREHEAT — files and SoundCloud consent. No cookies are set by this script.
   The consent decision is kept in localStorage ("md-consent-soundcloud": "granted" | "denied"). */
(function () {
  "use strict";
  var KEY = "md-consent-soundcloud";

  function getConsent() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function setConsent(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }

  /* ——— SoundCloud slots ——— */
  function visible(el) { return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length); }

  function loadSlot(slot) {
    if (slot.getAttribute("data-loaded")) return;
    var f = document.createElement("iframe");
    f.src = slot.getAttribute("data-src");
    f.title = slot.getAttribute("data-title") || "SoundCloud player";
    f.setAttribute("allow", "autoplay; encrypted-media");
    f.setAttribute("loading", "lazy");
    f.setAttribute("scrolling", "no");
    slot.innerHTML = "";
    slot.appendChild(f);
    slot.setAttribute("data-loaded", "1");
  }
  function loadVisibleSlots(root) {
    if (getConsent() !== "granted") return;
    var slots = (root || document).querySelectorAll(".sc[data-src]");
    for (var i = 0; i < slots.length; i++) if (visible(slots[i])) loadSlot(slots[i]);
  }

  document.addEventListener("click", function (e) {
    var once = e.target.closest && e.target.closest("[data-sc-once]");
    if (once) { loadSlot(once.closest(".sc")); return; }
    var always = e.target.closest && e.target.closest("[data-sc-always]");
    if (always) { decide("granted"); return; }
  });

  /* ——— consent banner ——— */
  var banner = document.getElementById("consent");
  function showBanner() { if (banner) banner.hidden = false; }
  function hideBanner() { if (banner) banner.hidden = true; }
  function decide(v) {
    var prev = getConsent();
    setConsent(v);
    hideBanner();
    if (v === "granted") loadVisibleSlots();
    else if (prev === "granted") location.reload(); /* remove players already loaded */
  }
  if (banner) {
    banner.querySelector("[data-accept]").addEventListener("click", function () { decide("granted"); });
    banner.querySelector("[data-reject]").addEventListener("click", function () { decide("denied"); });
  }
  var settings = document.querySelectorAll("[data-consent-settings]");
  for (var s = 0; s < settings.length; s++) settings[s].addEventListener("click", showBanner);
  if (!getConsent()) showBanner();

  /* ——— archive files ——— */
  function setOpen(btn, open, scroll) {
    var file = document.getElementById(btn.getAttribute("aria-controls"));
    if (!file) return;
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    var lbl = btn.querySelector("[data-toggle-label]");
    if (lbl) lbl.textContent = open ? "Close —" : "Open file +";
    file.hidden = !open;
    if (open) {
      loadVisibleSlots(file);
      if (scroll) file.scrollIntoView({ behavior: "smooth", block: "start" });
      if (history.replaceState) history.replaceState(null, "", "#" + file.id);
    } else if (location.hash === "#" + file.id && history.replaceState) {
      history.replaceState(null, "", location.pathname);
    }
  }
  var toggles = document.querySelectorAll("button[data-file-toggle]");
  for (var t = 0; t < toggles.length; t++) {
    toggles[t].addEventListener("click", function () {
      setOpen(this, this.getAttribute("aria-expanded") !== "true", false);
    });
  }
  var closers = document.querySelectorAll("[data-file-close]");
  for (var c = 0; c < closers.length; c++) {
    closers[c].addEventListener("click", function () {
      var btn = document.querySelector('button[aria-controls="' + this.getAttribute("data-file-close") + '"]');
      if (btn) { setOpen(btn, false, false); btn.focus(); }
    });
  }
  function openFromHash() {
    var id = location.hash.slice(1);
    if (!/^file-\d{3}$/.test(id)) return;
    var btn = document.querySelector('button[aria-controls="' + id + '"]');
    if (btn) setOpen(btn, true, true);
  }
  window.addEventListener("hashchange", openFromHash);
  openFromHash();
  loadVisibleSlots();
})();
