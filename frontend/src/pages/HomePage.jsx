import {useState, useEffect} from 'react'
import { api } from '../api/client.js'
import SearchBar from '../components/SearchBar.jsx'
import ProductList from '../components/ProductList.jsx'
import SidebarOffers from '../components/SidebarOffers.jsx'
import SidebarDelivery from '../components/SidebarDelivery.jsx'
import Basket from '../components/Basket.jsx'

const LS_KEY = 'widget_basket'

export default function HomePage() {
  const [products, setProducts] = useState([])
  const [offers, setOffers] = useState([])
  const [rules, setRules] = useState([])
  const [search, setSearch] = useState('')
  const [basket, setBasket] = useState([])

  useEffect(() => {
    // hydrate basket (getting the data from the local storage)
    try { const saved = JSON.parse(localStorage.getItem(LS_KEY) || '[]'); if (Array.isArray(saved)) setBasket(saved) } catch {}
    ;(async () => {
      const [p, o, r] = await Promise.all([
        api.listProducts(),
        api.listOffers(),
        api.listDeliveryRules(),
      ])
      setProducts(p); setOffers(o); setRules(r)
    })()
  }, [])

  useEffect(() => {
    localStorage.setItem(LS_KEY, JSON.stringify(basket))
  }, [basket])

  function addQty(code, qty) {
    setBasket(prev => {
      const idx = prev.findIndex(i => i.product_code === code)
      if (idx >= 0) {
        const updated = prev.map((it, i) => i === idx ? { ...it, quantity: it.quantity + qty } : it)
        return updated
      }
      return [...prev, { product_code: code, quantity: qty }]
    })
  }

  const filtered = products.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.code.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="page grid">
      <div className="content">
        <div className="row">
          <h2>Products</h2>
          <SearchBar value={search} onChange={setSearch} placeholder="Search products..." />
        </div>
        <ProductList products={filtered} onAdd={addQty} />
      </div>
      <aside className="sidebar">
        <SidebarOffers offers={offers} />
        <SidebarDelivery rules={rules} />
        <Basket items={basket} setItems={setBasket} />
      </aside>
    </div>
  )
}
