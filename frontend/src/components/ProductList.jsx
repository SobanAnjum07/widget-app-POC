import ProductCard from './ProductCard.jsx'

export default function ProductList({ products, onAdd }) {
  return (
    <div className="cards">
      {products.map(p => (
        <ProductCard key={p.code} product={p} onAdd={onAdd} />)
      )}
    </div>
  )
}
