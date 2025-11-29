import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import Header from './Header'; // Keep the header for log out functionality

const SIDEBAR_WIDTH = '20%';

const Layout = ({ children }) => {
    const { logout, isAuthenticated, isAdmin } = useAuth();
    const location = useLocation(); 

     // Define navigation items
    const allNavItems = [
        // 💡 1. CLIENT LINKS: Only show if the user is NOT an Admin
        { name: 'Home (Book Event)', path: '/dashboard', roles: ['client'] },
        { name: 'My Bookings', path: '/my-bookings', roles: ['client'] },
        
        // 💡 2. ADMIN LINKS: Only show if the user IS an Admin
        { name: 'All System Bookings', path: '/admin/bookings', roles: ['admin'] },
        { name: 'Admin Clients', path: '/admin/clients', roles: ['admin'] }
    ];
    
    // 💡 FILTER FIX: Filter navigation items based on the user's role
    const navItems = allNavItems.filter(item => 
        (item.roles.includes('admin') && isAdmin) || (item.roles.includes('client') && !isAdmin)
    );
    
    // Style for active navigation link
    const linkStyle = (path) => ({
        textDecoration: 'none',
        padding: '10px 15px',
        margin: '5px 0',
        display: 'block',
        color: location.pathname === path ? '#111' : '#555',
        background: location.pathname === path ? '#f0f0f0' : 'transparent',
        fontWeight: location.pathname === path ? 'bold' : 'normal',
        borderRadius: '4px',
    });

    return (
        <div style={styles.appContainer}>
            
            {/* --- LEFT SIDEBAR (CONSTANT VERTICAL DASHBOARD) --- */}
            <aside style={{ ...styles.sidebar, width: SIDEBAR_WIDTH }}>
                <div style={styles.sidebarHeader}>
                    EMS Dashboard
                </div>
                
                <nav>
                    {navItems.map(item => (
                        <Link key={item.name} to={item.path} style={linkStyle(item.path)}>
                            {item.name}
                        </Link>
                    ))}
                </nav>
                
                {/* Logout button moved to the bottom of the sidebar for common UX */}
                <button 
                    onClick={logout} 
                    style={styles.logoutButton}
                >
                    Logout
                </button>
            </aside>
            
            {/* --- RIGHT CONTENT AREA --- */}
            <div style={styles.contentArea}>
                {/* We remove the old top Header bar. We'll keep the top-right corner empty or add a welcome message.
                   We only render the children (the specific page content) here.
                */}
                <div style={styles.mainContent}>
                    {children}
                </div>
            </div>
        </div>
    );
};

// --- Aesthetic Styling ---
const styles = {
    appContainer: {
        display: 'flex',
        minHeight: '100vh',
    },
    sidebar: {
        background: '#108a6dff', /* 💡 REQUIRED BACKGROUND COLOR */
        padding: '15px 10px',
        boxShadow: '2px 0 5px rgba(0,0,0,0.1)',
        display: 'flex',
        minHeight: 'screen',
        flexDirection: 'column',
        justifyContent: 'space-between',
        position: 'fixed', // Keep it attached to the left
        height: '100%',
        zIndex: 100,
    },
    sidebarHeader: {
        fontSize: '1.4em',
        fontWeight: 'bold',
        padding: '10px 0 20px 0',
        textAlign: 'center',
        borderBottom: '1px solid #ffcc00', // Darker yellow line
        marginBottom: '15px',
    },
    contentArea: {
        marginLeft: SIDEBAR_WIDTH, // Shifts the content area over by the sidebar width
        width: `calc(100% - ${SIDEBAR_WIDTH})`,
    },
    mainContent: {
        padding: '40px',
    },
    logoutButton: {
        background: '#828282ff',
        color: 'white',
        padding: '10px',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        marginTop: 'auto', // Pushes button to the bottom
    }
};

export default Layout;