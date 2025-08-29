const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  if (res.status === 204) return null
  return res.json()
}

export const api = {
  listProducts: () => request('/catalogue/products'),
  createProduct: (data) => request('/catalogue/products', { method: 'POST', body: JSON.stringify(data) }),
  updateProduct: (code, data) => request(`/catalogue/products/${code}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteProduct: (code) => request(`/catalogue/products/${code}`, { method: 'DELETE' }),

  listOffers: () => request('/catalogue/offers'),
  createOffer: (data) => request('/catalogue/offers', { method: 'POST', body: JSON.stringify(data) }),
  updateOffer: (id, data) => request(`/catalogue/offers/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteOffer: (id) => request(`/catalogue/offers/${id}`, { method: 'DELETE' }),

  listDeliveryRules: () => request('/catalogue/delivery-rules'),
  createDeliveryRule: (data) => request('/catalogue/delivery-rules', { method: 'POST', body: JSON.stringify(data) }),
  updateDeliveryRule: (id, data) => request(`/catalogue/delivery-rules/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteDeliveryRule: (id) => request(`/catalogue/delivery-rules/${id}`, { method: 'DELETE' }),

  basketTotal: (items) => request('/checkout/total', { method: 'POST', body: JSON.stringify({ items }) }),
}
