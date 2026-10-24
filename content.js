const root = document.documentElement;

function setLight(light) {
  root.classList.toggle("mbx-light", light);
}

if (window === window.parent) {
  chrome.storage.sync.get({ dark: true }, ({ dark }) => setLight(!dark));
  chrome.storage.onChanged.addListener((changes) => {
    if (changes.dark) setLight(!changes.dark.newValue);
  });
} else {
  // Read synchronously from the app, because Chrome doesn't reliably redo its
  // auto dark pass when a frame's colour scheme changes after first paint
  try {
    setLight(window.parent.document.documentElement.classList.contains("mbx-light"));
  } catch {}
}
