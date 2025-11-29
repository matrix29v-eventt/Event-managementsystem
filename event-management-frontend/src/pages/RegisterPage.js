import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import Header from '../components/Header';

const API_URL = 'http://127.0.0.1:8000';

const RegisterPage = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState(''); // 💡 NEW: Confirm Password State
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        // 💡 CLIENT-SIDE VALIDATION: Check if passwords match
        if (password !== confirmPassword) {
            setError('Passwords do not match.');
            return;
        }

        // 💡 CRITICAL: Browser prompts for saving password only if form elements are correct.
        // We ensure a successful POST triggers the prompt.
        const registrationData = { name, email, phone, password };

        try {
            await axios.post(`${API_URL}/clients/`, registrationData);
            
            setSuccess('Registration successful! Please log in with your new account.');
            
            // Redirect to login page after successful registration
            setTimeout(() => {
                navigate('/login');
            }, 1500);

        } catch (err) {
            console.error("Registration failed:", err.response);
            const detail = err.response?.data?.detail || 'An unexpected error occurred.';
            setError(`Registration failed: ${detail}. Email may already be registered.`);
        }
    };

    return (
        <>
            <Header />
            <div style={styles.container}>
                <h2 style={styles.header}>New Client Sign Up</h2>
                
                {success && <p style={styles.success}>{success}</p>}
                {error && <p style={styles.error}>{error}</p>}
                
                {/* 💡 UX FIX: Form must have autocomplete="on" */}
                <form onSubmit={handleSubmit} autoComplete="on">
                    
                    {/* Name and Email */}
                    <input type="text" placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} required style={styles.input} autoComplete="name" />
                    <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required style={styles.input} autoComplete="email" />
                    <input type="tel" placeholder="Phone (Optional)" value={phone} onChange={(e) => setPhone(e.target.value)} style={styles.input} autoComplete="tel" />
                    
                    <hr style={{margin: '20px 0'}}/>

                    {/* 💡 PASSWORD FIELDS (Save Password Prompt relies on these): */}
                    <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required style={styles.input} autoComplete="new-password" />
                    
                    <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required style={styles.input} autoComplete="new-password" />
                    
                    <button type="submit" style={styles.button}>Sign Up</button>
                </form>

                <p style={styles.linkText}>
                    Already have an account? <Link to="/login">Sign In</Link>
                </p>
            </div>
        </>
    );
};

// --- Aesthetic Styling ---
const styles = {
    // ... (Your existing styles) ...
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
    header: {
        marginBottom: '20px',
        color: '#333'
    },
    input: {
        width: '100%',
        padding: '10px',
        marginBottom: '15px',
        borderRadius: '4px',
        border: '1px solid #ccc',
        boxSizing: 'border-box'
    },
    button: {
        width: '100%',
        padding: '12px',
        background: '#160337ff',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '1em',
        marginBottom: '15px'
    },
    success: {
        color: '#155724',
        backgroundColor: '#d4edda',
        padding: '10px',
        borderRadius: '4px',
        marginBottom: '15px'
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
    }
};

export default RegisterPage;