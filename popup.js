const box = document.getElementById("dark");

chrome.storage.sync.get({ dark: true }, ({ dark }) => {
  box.checked = dark;
});

box.addEventListener("change", () => {
  chrome.storage.sync.set({ dark: box.checked });
});
