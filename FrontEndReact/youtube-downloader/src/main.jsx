import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import {createBrowserRouter, RouterProvider, Route} from 'react-router-dom'
import './index.css'
import Home from './routes/Home'

const router = createBrowserRouter([
  {
    element: <App/>,
    children: [
    {
      path: "/new",
      element: <Home/>
    },
  ]}
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
