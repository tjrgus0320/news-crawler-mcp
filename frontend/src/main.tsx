import React from 'react'
import ReactDOM from 'react-dom/client'
import { Toaster } from 'react-hot-toast'
import App from './App'
import './styles/index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
    <Toaster
      position="bottom-right"
      toastOptions={{
        duration: 3000,
        style: {
          background: '#1e293b',
          color: '#f8fafc',
        },
        success: {
          iconTheme: {
            primary: '#10b981',
            secondary: '#f8fafc',
          },
        },
      }}
    />
  </React.StrictMode>,
)
