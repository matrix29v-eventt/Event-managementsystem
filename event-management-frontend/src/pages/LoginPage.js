

// import React, { useState } from 'react';
// import axios from 'axios';
// import { useNavigate } from 'react-router-dom';
// import { useAuth } from '../AuthContext';
// import Header from '../components/Header';

// const API_URL = 'http://127.0.0.1:8000';

// const LoginPage = () => {
//     const [email, setEmail] = useState('');
//     const [password, setPassword] = useState('');
//     const [error, setError] = useState('');
    
//     const { login } = useAuth();
//     const navigate = useNavigate();

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setError('');
//         try {
//             const response = await axios.post(`${API_URL}/auth/token`, { email, password });
//             const token = response.data.access_token;
            
//             // 💡 NEW FIX: Extract the client_id from the API response body
//             const userId = response.data.client_id;
            
//             // Temporary role assignment (lab fix)
//             const role = email === 'admin@ems.com' ? 'admin' : 'client'; 
            
//             // Pass token, role, AND ID to the login function
//             login(token, role, userId); 
//             navigate('/dashboard'); 

//         } catch (err) {
//             const detail = err.response?.data?.detail || 'An unexpected error occurred.';
//             setError(`Login failed: ${detail}`);
//         }
//     };

//     return (
//         <>
//             <Header />
//             <div style={{ padding: '40px', maxWidth: '400px', margin: '50px auto', border: '1px solid #ccc' }}>
//                 <h2>Client Login</h2>
//                 <form onSubmit={handleSubmit}>
//                     {error && <p style={{ color: 'red' }}>{error}</p>}
                    
//                     <div style={{ marginBottom: '15px' }}>
//                         <label htmlFor="email">Email (Username):</label>
//                         <input 
//                             type="email" 
//                             id="email"
//                             value={email} 
//                             onChange={(e) => setEmail(e.target.value)} 
//                             required 
//                             style={{ width: '100%', padding: '8px' }}
//                         />
//                     </div>

//                     <div style={{ marginBottom: '15px' }}>
//                         <label htmlFor="password">Password:</label>
//                         <input 
//                             type="password" 
//                             id="password"
//                             value={password} 
//                             onChange={(e) => setPassword(e.target.value)} 
//                             required 
//                             style={{ width: '100%', padding: '8px' }}
//                         />
//                     </div>

//                     <button type="submit" style={{ width: '100%', padding: '10px', background: '#160337ff', color: 'white', border: 'none', cursor: 'pointer' }}>
//                         Log In
//                     </button>
//                 </form>
//             </div>
//         </>
//     );
// };

// export default LoginPage;


// src/pages/LoginPage.js

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom'; // Ensure Link is imported for Sign Up link
import { useAuth } from '../AuthContext'; 
import Header from '../components/Header'; 

const API_URL = 'http://127.0.0.1:8000';

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await axios.post(`${API_URL}/auth/token`, { email, password });
            
            const token = response.data.access_token;
            const userId = response.data.client_id; // Get ID from response
            
            // Temporary role assignment (lab fix)
            const role = email === 'admin@ems.com' ? 'admin' : 'client'; 
            
            // Pass token, role, AND ID to the login function
            login(token, role, userId); 
            navigate('/dashboard'); 

        } catch (err) {
            // Handle 401 Unauthorized or other API errors
            const detail = err.response?.data?.detail || 'An unexpected error occurred.';
            setError(`Login failed: ${detail}`);
        }
    }; // <--- **This is the closing bracket for handleSubmit**

    // This is the component's final render function.
    return (
        <>
            <Header />
            <div style={styles.container}> 
                <h2>Client Login</h2>
                
                <form onSubmit={handleSubmit}>
                    {error && <p style={styles.error}>{error}</p>}
                    
                    <div style={styles.inputGroup}>
                        <label htmlFor="email">Email (Username):</label>
                        <input 
                            type="email" 
                            id="email"
                            value={email} 
                            onChange={(e) => setEmail(e.target.value)} 
                            required 
                            style={styles.input}
                        />
                    </div>

                    <div style={styles.inputGroup}>
                        <label htmlFor="password">Password:</label>
                        <input 
                            type="password" 
                            id="password"
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)} 
                            required 
                            style={styles.input}
                        />
                    </div>

                    <button type="submit" style={styles.button}>
                        Log In
                    </button>
                </form>

                {/* Link to Registration Page */}
                <p style={styles.linkText}>
                    Don't have an account? <Link to="/register" style={styles.link}>Sign Up</Link>
                </p>
            </div>
        </>
    );
}; // <--- **This is the closing bracket for the LoginPage component**

// --- Aesthetic Styling ---
const styles = {
    container: {
        padding: '40px',
        maxWidth: '400px',
        margin: '50px auto',
        border: '1px solid #ddd',
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        background: '#fff',
        textAlign: 'center',
    },
    inputGroup: {
        marginBottom: '15px',
        textAlign: 'left',
    },
    input: {
        width: '100%',
        padding: '10px',
        marginTop: '5px',
        borderRadius: '4px',
        border: '1px solid #ccc',
        boxSizing: 'border-box'
    },
    button: {
        width: '100%',
        padding: '10px',
        background: '#160337ff',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '1em',
        marginTop: '10px',
    },
    error: {
        color: '#721c24',
        backgroundColor: '#f8d7da',
        padding: '10px',
        borderRadius: '4px',
        marginBottom: '15px'
    },
    linkText: {
        marginTop: '20px',
        fontSize: '0.9em'
    },
    link: {
        color: '#007bff'
    }
};

export default LoginPage;