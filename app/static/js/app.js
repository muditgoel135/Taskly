// Register service worker for PWA/offline + notifications
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/js/sw.js');
}
