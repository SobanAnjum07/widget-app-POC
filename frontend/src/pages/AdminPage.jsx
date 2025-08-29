import { useState, useEffect } from 'react'
import { api } from '../api/client.js'

export default function AdminPage() {
  const [products, setProducts] = useState([])
  const [offers, setOffers] = useState([])
  const [rules, setRules] = useState([])

  const [newProd, setNewProd] = useState({ code: '', name: '', price: '' })
  const [newOffer, setNewOffer] = useState({ type: 'BOGO_HALF', product_code: '' })
  const [newRule, setNewRule] = useState({ min_total: '', charge: '' })

  const [editingOffer, setEditingOffer] = useState(null)
  const [editingRule, setEditingRule] = useState(null)
  const [message, setMessage] = useState(null)

  async function initialLoad() {
    const [p, o, r] = await Promise.all([
      api.listProducts(), api.listOffers(), api.listDeliveryRules()
    ])
    setProducts(p); setOffers(o); setRules(r)
  }
  useEffect(() => { initialLoad() }, [])

  function notify(msg, type='success'){ setMessage({ msg, type }); setTimeout(()=>setMessage(null), 2500) }

  // Products
  async function createProduct(e) {
    e.preventDefault()
    if (!newProd.code || !newProd.name || !newProd.price) return notify('All product fields are required','error')
    try {
      const created = await api.createProduct({ ...newProd, price: parseFloat(newProd.price) })
      setProducts(prev => [...prev, created])
      setNewProd({ code: '', name: '', price: '' })
      notify('Product created')
    } catch(err){ notify(err.message,'error') }
  }
  async function deleteProduct(code) {
    await api.deleteProduct(code)
    setProducts(prev => prev.filter(p => p.code !== code))
    notify('Product deleted')
  }

  // Offers
  async function createOffer(e) {
    e.preventDefault()
    if (!newOffer.type) return notify('Offer type is required','error')
    try {
      const created = await api.createOffer({ ...newOffer, product_code: newOffer.product_code || null })
      setOffers(prev => [...prev, created])
      setNewOffer({ type: 'BOGO_HALF', product_code: '' })
      notify('Offer created')
    } catch(err){ notify(err.message,'error') }
  }
  function startEditOffer(o){ setEditingOffer({ ...o }) }
  function cancelEditOffer(){ setEditingOffer(null) }
  async function saveOffer(){
    if (!editingOffer) return
    try {
      const updated = await api.updateOffer(editingOffer.id, { type: editingOffer.type, product_code: editingOffer.product_code || null })
      setOffers(prev => prev.map(o => o.id === updated.id ? updated : o))
      setEditingOffer(null)
      notify('Offer updated')
    } catch(err){ notify(err.message,'error') }
  }
  async function deleteOffer(id) {
    await api.deleteOffer(id)
    setOffers(prev => prev.filter(o => o.id !== id))
    notify('Offer deleted')
  }

  // Delivery rules
  async function createRule(e) {
    e.preventDefault()
    const mt = parseFloat(newRule.min_total)
    const ch = parseFloat(newRule.charge)
    if (Number.isNaN(mt) || Number.isNaN(ch)) return notify('Enter valid numbers','error')
    try {
      const created = await api.createDeliveryRule({ min_total: mt, charge: ch })
      setRules(prev => [...prev, created])
      setNewRule({ min_total: '', charge: '' })
      notify('Rule created')
    } catch(err){ notify(err.message,'error') }
  }
  function startEditRule(r){ setEditingRule({ ...r, min_total: String(r.min_total), charge: String(r.charge) }) }
  function cancelEditRule(){ setEditingRule(null) }
  async function saveRule(){
    if (!editingRule) return
    const mt = parseFloat(editingRule.min_total)
    const ch = parseFloat(editingRule.charge)
    if (Number.isNaN(mt) || Number.isNaN(ch)) return notify('Enter valid numbers','error')
    try {
      const updated = await api.updateDeliveryRule(editingRule.id, { min_total: mt, charge: ch })
      setRules(prev => prev.map(r => r.id === updated.id ? updated : r))
      setEditingRule(null)
      notify('Rule updated')
    } catch(err){ notify(err.message,'error') }
  }
  async function deleteRule(id) {
    await api.deleteDeliveryRule(id)
    setRules(prev => prev.filter(r => r.id !== id))
    notify('Rule deleted')
  }

  return (
    <div className="page grid">
      <div className="content">
        {message && <div className={message.type==='error'?'error':'success'}>{message.msg}</div>}

        <section>
          <h2>Products</h2>
          <form onSubmit={createProduct} className="form-grid">
            <input placeholder="Code" value={newProd.code} onChange={e => setNewProd({ ...newProd, code: e.target.value })} />
            <input placeholder="Name" value={newProd.name} onChange={e => setNewProd({ ...newProd, name: e.target.value })} />
            <input placeholder="Price" type="number" step="0.01" value={newProd.price} onChange={e => setNewProd({ ...newProd, price: e.target.value })} />
            <button type="submit">Add</button>
          </form>
          <ul className="list">
            {products.map(p => (
              <li key={p.code}>
                <span>{p.code} - {p.name} - <span className="badge">${Number(p.price).toFixed(2)}</span></span>
                <button onClick={() => deleteProduct(p.code)}>Delete</button>
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h2>Offers</h2>
          <form onSubmit={createOffer} className="form-grid">
            <select value={newOffer.type} onChange={e => setNewOffer({ ...newOffer, type: e.target.value })}>
              <option value="BOGO_HALF">BOGO_HALF</option>
              <option value="BOGO_FREE">BOGO_FREE</option>
            </select>
            <input placeholder="Product code (optional)" value={newOffer.product_code} onChange={e => setNewOffer({ ...newOffer, product_code: e.target.value })} />
            <button type="submit">Add</button>
          </form>
          <ul className="list">
            {offers.map(o => (
              <li key={o.id}>
                {editingOffer && editingOffer.id === o.id ? (
                  <span className="row">
                    <select value={editingOffer.type} onChange={e => setEditingOffer({ ...editingOffer, type: e.target.value })}>
                      <option value="BOGO_HALF">BOGO_HALF</option>
                      <option value="BOGO_FREE">BOGO_FREE</option>
                    </select>
                    <input placeholder="Product code" value={editingOffer.product_code || ''} onChange={e => setEditingOffer({ ...editingOffer, product_code: e.target.value })} />
                  </span>
                ) : (
                  <span>{o.type} {o.product_code ? `on ${o.product_code}` : ''}</span>
                )}
                <span className="row">
                  {editingOffer && editingOffer.id === o.id ? (
                    <>
                      <button onClick={saveOffer}>Save</button>
                      <button onClick={cancelEditOffer}>Cancel</button>
                    </>
                  ) : (
                    <>
                      <button onClick={() => startEditOffer(o)}>Edit</button>
                      <button onClick={() => deleteOffer(o.id)}>Delete</button>
                    </>
                  )}
                </span>
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h2>Delivery Rules</h2>
          <form onSubmit={createRule} className="form-grid">
            <input placeholder="Min total" type="number" step="0.01" value={newRule.min_total} onChange={e => setNewRule({ ...newRule, min_total: e.target.value })} />
            <input placeholder="Charge" type="number" step="0.01" value={newRule.charge} onChange={e => setNewRule({ ...newRule, charge: e.target.value })} />
            <button type="submit">Add</button>
          </form>
          <ul className="list">
            {rules.map(r => (
              <li key={r.id}>
                {editingRule && editingRule.id === r.id ? (
                  <span className="row">
                    <input placeholder="Min total" type="number" step="0.01" value={editingRule.min_total} onChange={e => setEditingRule({ ...editingRule, min_total: e.target.value })} />
                    <input placeholder="Charge" type="number" step="0.01" value={editingRule.charge} onChange={e => setEditingRule({ ...editingRule, charge: e.target.value })} />
                  </span>
                ) : (
                  <span>Spend ≥ ${Number(r.min_total).toFixed(2)}: delivery ${Number(r.charge).toFixed(2)}</span>
                )}
                <span className="row">
                  {editingRule && editingRule.id === r.id ? (
                    <>
                      <button onClick={saveRule}>Save</button>
                      <button onClick={cancelEditRule}>Cancel</button>
                    </>
                  ) : (
                    <>
                      <button onClick={() => startEditRule(r)}>Edit</button>
                      <button onClick={() => deleteRule(r.id)}>Delete</button>
                    </>
                  )}
                </span>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  )
}
