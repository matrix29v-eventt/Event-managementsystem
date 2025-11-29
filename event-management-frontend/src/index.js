import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';
import App from './App';
import { AuthProvider } from './AuthContext'; 
// 💡 CLEANUP: Remove 'import reportWebVitals from './reportWebVitals';'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AuthProvider> 
      <Router>
        <App />
      </Router>
    </AuthProvider>
  </React.StrictMode>
);

// 💡 CLEANUP: Remove the call to reportWebVitals at the bottom of the file