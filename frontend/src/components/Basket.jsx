import {useState} from 'react'
import { api } from '../api/client.js'

export default function Basket({ items, setItems }) {
  const [totals, setTotals] = useState(null)

  function inc(code) {
    setItems(prev => prev.map(it => it.product_code === code ? { ...it, quantity: it.quantity + 1 } : it))
  }
  function dec(code) {
    setItems(prev => {
      const next = prev.map(it => it.product_code === code ? { ...it, quantity: it.quantity - 1 } : it)
      return next.filter(it => it.quantity > 0)
    })
  }
  function remove(code) {
    setItems(prev => prev.filter(i => i.product_code !== code))
  }
  function clear() {
    setItems([])
    setTotals(null)
  }

  async function calculate() {
    const normalized = Object.values(items.reduce((acc, it) => {
      acc[it.product_code] = acc[it.product_code] || { product_code: it.product_code, quantity: 0 }
      acc[it.product_code].quantity += it.quantity
      return acc
    }, {}))
    const res = await api.basketTotal(normalized)
    setTotals(res)
  }

  return (
    <div className="basket">
      <h3>Basket</h3>
      {!items.length && <div>No items</div>}
      <ul>
        {items.map(i => (
          <li key={i.product_code}>
            <span>{i.product_code} x {i.quantity}</span>
            <span>
              <button type="button" onClick={() => dec(i.product_code)}>-</button>
              <button type="button" onClick={() => inc(i.product_code)}>+</button>
              <button type="button" onClick={() => remove(i.product_code)}>Delete</button>
            </span>
          </li>
        ))}
      </ul>
      <div className="row">
        <button type="button" onClick={calculate} disabled={!items.length}>Calculate</button>
        <button type="button" onClick={clear} disabled={!items.length}>Clear</button>
      </div>
      {totals && (
        <div className="totals">
          <div>Subtotal: ${totals.subtotal.toFixed(2)}</div>
          <div>Discount: -${totals.discount.toFixed(2)}</div>
          <div>Delivery: ${totals.delivery.toFixed(2)}</div>
          <div><strong>Total: ${totals.total.toFixed(2)}</strong></div>
        </div>
      )}
    </div>
  )
}
