import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const Header = () => {
    const { isAuthenticated, isAdmin, logout } = useAuth();

    return (
        <header style={{ margin: '0', padding: '30px 20px', background: '#160337ff', color: 'white', display: 'flex', justifyContent: 'space-between' }}>
            <div className="logo">
                <Link to="/dashboard" style={{ fontSize: '32px', color: 'white', textDecoration: 'none', fontWeight: 'bold' }}>
                    EMS Admin Portal
                </Link>
            </div>
            <nav>
                {/* 1. Admin Link (Visible only to Admin) */}
                {isAdmin && (
                    <Link to="/admin/clients" style={{ color: 'gold', marginLeft: '20px' }}>
                        Admin Panel
                    </Link>
                )}

                {/* 2. Authentication Links */}
                {isAuthenticated ? (
                    <button 
                        onClick={logout} 
                        style={{ fontSize: '22px', background: 'none', border: 'none', color: 'white', cursor: 'pointer', marginLeft: '20px' }}
                    >
                        Logout
                    </button>
                ) : (
                    <Link to="/login" style={{ fontSize: '22px', color: 'white', marginLeft: '20px' }}>
                        Login
                    </Link>
                )}
            </nav>
        </header>
    );
};

export default Header;