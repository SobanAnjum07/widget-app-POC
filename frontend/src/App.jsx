import React from 'react'
import HomePage from './pages/HomePage.jsx'
import AdminPage from './pages/AdminPage.jsx'

export default function App() {
  const [page, setPage] = React.useState('home')
  return (
    <div className="container">
      <header className="header">
        <h1>Widget</h1>
        <nav>
          <button onClick={() => setPage('home')}>Home</button>
          <button onClick={() => setPage('admin')}>Admin</button>
        </nav>
      </header>
      <main>
        {page === 'home' ? <HomePage /> : <AdminPage />}
      </main>
    </div>
  )
}
