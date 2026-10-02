/**
 * sw.js — Service Worker for Kaam Milega (v7)
 * Caches core assets and emergency numbers for offline accessibility in rural areas.
 * Employs Network-First caching strategy to guarantee instant client updates while online.
 */

const CACHE_NAME = 'kaam-milega-v8';
const ASSETS_TO_CACHE = [
  '/',
  '/privacy',
  '/terms',
  '/static/css/app.css',
  '/static/js/i18n.js',
  '/static/js/speech.js',
  '/static/js/wizard.js',
  '/static/js/search.js',
  '/static/js/compliance.js',
  '/static/js/work_slip.js',
  '/static/js/jobs.js',
  '/static/js/app.js',
  '/static/images/icons/logo.svg',
  '/static/images/icons/mason.svg',
  '/static/images/icons/plumber.svg',
  '/static/images/icons/electrician.svg',
  '/static/images/icons/boring.svg',
  '/static/images/icons/carpenter.svg',
  '/static/images/icons/painter.svg',
  '/static/images/icons/welder.svg',
  '/static/images/icons/labor.svg',
  '/static/images/icons/halwai.svg',
  '/static/images/icons/event_cook.svg',
  '/static/images/icons/catering_helper.svg',
  '/static/images/icons/tent_decorator.svg'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  // Network first for all requests, fallback to cache when offline
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request);
      })
  );
});
