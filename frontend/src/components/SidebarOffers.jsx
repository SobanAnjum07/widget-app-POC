function humanizeOffer(o) {
  if (o.type === 'BOGO_HALF') return `Buy 1 ${o.product_code || ''}, 2nd half price`.trim()
  if (o.type === 'BOGO_FREE') return `Buy 1 ${o.product_code || ''}, get 1 free`.trim()
  return o.type
}

export default function SidebarOffers({ offers }) {
  return (
    <section>
      <h3>Offers</h3>
      <ul>
        {offers.map(o => (
          <li key={o.id}>{humanizeOffer(o)}</li>
        ))}
      </ul>
    </section>
  )
}
