// QuestForgeAI — Service Worker v2.0
// Caching strategy: Cache-first for assets, Network-first for API calls

const CACHE_NAME    = 'questforge-v2';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  // CDN assets cached on first load (listed for reference; sw caches them dynamically)
];

// CDN origins to cache on fetch
const CACHE_CDN_ORIGINS = [
  'cdn.tailwindcss.com',
  'cdnjs.cloudflare.com',
  'cdn.jsdelivr.net',
  'unpkg.com',
  'fonts.googleapis.com',
  'fonts.gstatic.com',
];

// ── Install ──────────────────────────────────────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// ── Activate ─────────────────────────────────────────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch ─────────────────────────────────────────────────────────────────────
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET and chrome-extension requests
  if (request.method !== 'GET' || url.protocol === 'chrome-extension:') return;

  // Network-first for API calls (Colab/Pinggy backend)
  if (isAPICall(url)) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Network-first for Pollinations image generation (dynamic content)
  if (url.hostname === 'image.pollinations.ai') {
    event.respondWith(networkFirstWithCache(request, 'questforge-art-v2'));
    return;
  }

  // Cache-first for CDN assets and app shell
  event.respondWith(cacheFirst(request));
});

// ── Helpers ───────────────────────────────────────────────────────────────────
function isAPICall(url) {
  // Treat any non-cached, non-CDN cross-origin POST target as an API call
  return (
    !url.hostname.includes('pollinations.ai') &&
    !CACHE_CDN_ORIGINS.some(o => url.hostname.includes(o)) &&
    url.hostname !== self.location.hostname &&
    !url.hostname.endsWith('fonts.gstatic.com')
  );
}

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    // Cache successful CDN/same-origin responses
    if (response.ok) {
      const url = new URL(request.url);
      const shouldCache =
        url.hostname === self.location.hostname ||
        CACHE_CDN_ORIGINS.some(o => url.hostname.includes(o));
      if (shouldCache) {
        const cache = await caches.open(CACHE_NAME);
        cache.put(request, response.clone());
      }
    }
    return response;
  } catch {
    // Offline fallback — return cached index.html for navigation requests
    if (request.mode === 'navigate') {
      return caches.match('/index.html');
    }
    return new Response('Offline', { status: 503 });
  }
}

async function networkFirst(request) {
  try {
    return await fetch(request);
  } catch {
    const cached = await caches.match(request);
    return cached || new Response(
      JSON.stringify({ error: 'Offline — no cached response available' }),
      { status: 503, headers: { 'Content-Type': 'application/json' } }
    );
  }
}

async function networkFirstWithCache(request, cacheName) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request, { cacheName });
    return cached || new Response('Art unavailable offline', { status: 503 });
  }
}

// ── Background sync (future: queue failed forge requests) ────────────────────
self.addEventListener('sync', event => {
  if (event.tag === 'forge-retry') {
    event.waitUntil(retryPendingForge());
  }
});

async function retryPendingForge() {
  // Placeholder: in production, read from IndexedDB and replay
  console.log('[SW] Background sync: forge-retry');
}

// ── Push notifications ────────────────────────────────────────────────────────
self.addEventListener('push', event => {
  const data = event.data?.json() || {};
  event.waitUntil(
    self.registration.showNotification(data.title || 'QuestForgeAI', {
      body:  data.body  || 'Your forge is ready',
      icon:  data.icon  || '/icons/icon-192.png',
      badge: data.badge || '/icons/icon-72.png',
      data:  data,
      actions: [
        { action: 'view', title: 'View' },
        { action: 'dismiss', title: 'Dismiss' },
      ],
    })
  );
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  if (event.action !== 'dismiss') {
    event.waitUntil(clients.openWindow('/'));
  }
});
