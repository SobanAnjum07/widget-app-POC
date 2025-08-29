import {useState} from 'react'

export default function ProductCard({ product, onAdd }) {
  const [qty, setQty] = useState(1)

  function inc() { setQty(q => q + 1) }
  function dec() { setQty(q => Math.max(1, q - 1)) }
  function add() { onAdd(product.code, qty); setQty(1) }

  return (
    <div className="card">
      <div className="card-title">{product.name}</div>
      <div className="card-sub">{product.code}</div>
      <div className="price">${Number(product.price).toFixed(2)}</div>
      <div className="row">
        <div className="counter">
          <button type="button" onClick={dec}>-</button>
          <span>{qty}</span>
          <button type="button" onClick={inc}>+</button>
        </div>
        <button type="button" onClick={add}>Add</button>
      </div>
    </div>
  )
}
