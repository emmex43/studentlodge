// housing/templates/sw.js

// Listen for the install event
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installed successfully');
    // Force the waiting service worker to become the active service worker
    self.skipWaiting();
});

// Listen for the activate event
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activated successfully');
});

// Listen for network requests and pass them through to the internet
self.addEventListener('fetch', (event) => {
    event.respondWith(fetch(event.request));
});