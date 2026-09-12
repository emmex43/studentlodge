// sw.js - Service Worker for PWA

// Listen for the install event
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installed successfully');
});

// Listen for network requests and pass them through
self.addEventListener('fetch', (event) => {
    event.respondWith(fetch(event.request));
});