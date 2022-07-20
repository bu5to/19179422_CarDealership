var cacheName = 'PredictingCars';
var filesToCache = [
  './static/assets/css/style.css',
  './static/assets/css/responsive.css',
  './static/assets/css/wizard.css',
  './templates/base.html',
  './templates/car.html',
  './templates/properties.html',
  './templates/submit-property.html',
  './templates/account-settings.html',
  './templates/login.html',
  './templates/register.html'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});