const CACHE_NAME = 'CACHE_v1';

const STATIC_ASSETS = [
  'index.html',
  'css/style.css',
  'js/game.js',
  'manifest.webmanifest',
  'icons/icon.svg',
  'data/questions.enc'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(name) {
          return name !== CACHE_NAME;
        }).map(function(name) {
          return caches.delete(name);
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(event) {
  var requestUrl = event.request.url;
  var isDataEnc = requestUrl.indexOf('questions.enc') !== -1;
  var isStatic = STATIC_ASSETS.some(function(asset) {
    return requestUrl.indexOf(asset) !== -1;
  });

  if (isDataEnc) {
    event.respondWith(
      caches.open(CACHE_NAME).then(function(cache) {
        return cache.match(event.request).then(function(cachedResponse) {
          var fetchPromise = fetch(event.request).then(function(networkResponse) {
            if (networkResponse && networkResponse.ok) {
              cache.put(event.request, networkResponse.clone());
            }
            return networkResponse;
          }).catch(function() {
            return cachedResponse;
          });
          return cachedResponse || fetchPromise;
        });
      })
    );
  } else if (isStatic) {
    event.respondWith(
      fetch(event.request).then(function(networkResponse) {
        if (networkResponse && networkResponse.ok) {
          var clone = networkResponse.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(event.request, clone);
          });
        }
        return networkResponse;
      }).catch(function() {
        return caches.match(event.request);
      })
    );
  } else {
    event.respondWith(
      fetch(event.request).catch(function() {
        return caches.match(event.request);
      })
    );
  }
});
