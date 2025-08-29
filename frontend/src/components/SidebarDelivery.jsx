export default function SidebarDelivery({ rules }) {
  const sorted = [...rules].sort((a,b)=> Number(a.min_total)-Number(b.min_total))
  return (
    <section>
      <h3>Delivery</h3>
      <ul>
        {sorted.map(r => (
          <li key={r.id}>Spend ≥ ${Number(r.min_total).toFixed(2)}: delivery ${Number(r.charge).toFixed(2)}</li>
        ))}
      </ul>
    </section>
  )
}
