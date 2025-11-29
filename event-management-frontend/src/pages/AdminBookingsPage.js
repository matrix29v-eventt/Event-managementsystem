import React, { useState, useEffect } from 'react';
import axiosInstance from '../axiosInstance';
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';

// Component to display all booking details for the Admin
const AdminBookingsPage = () => {
    const { isAuthenticated, userRole } = useAuth();
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // Redirect if not authenticated (though AdminRoute should handle this)
    useEffect(() => {
        if (!isAuthenticated || userRole !== 'admin') {
            navigate('/dashboard'); 
        }
    }, [isAuthenticated, userRole, navigate]);


    useEffect(() => {
        const fetchBookings = async () => {
            try {
                // 💡 Call the NEW detailed Admin endpoint
                const response = await axiosInstance.get('/bookings/admin/details'); 
                setBookings(response.data);
            } catch (error) {
                console.error("Failed to fetch detailed bookings:", error.response);
            } finally {
                setLoading(false);
            }
        };
        fetchBookings();
    }, []);

    // --- Styling for Hover Effect ---
    const cardStyle = {
        background: '#fff',
        border: '1px solid #ddd',
        borderRadius: '8px',
        padding: '20px',
        transition: 'transform 0.2s, box-shadow 0.2s',
        cursor: 'default',
        boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
        marginBottom: '20px'
    };

    const handleHover = (e, isHovering) => {
        e.currentTarget.style.transform = isHovering ? 'translateY(-3px)' : 'translateY(0)';
        e.currentTarget.style.boxShadow = isHovering ? '0 8px 15px rgba(0,0,0,0.15)' : '0 2px 4px rgba(0,0,0,0.05)';
    };

    

    if (loading) return <div>Loading All Booking Data...</div>;

    return (
        <div>
            <h1 style={{ borderBottom: '2px solid #333', paddingBottom: '10px', marginBottom: '30px' }}>
                All System Bookings Overview
            </h1>

            {bookings.length === 0 ? (
                <p>No bookings found in the system.</p>
            ) : (
                <div style={styles.grid}>
                    {bookings.map(booking => (
                        <div 
                            key={booking.booking_id} 
                            style={cardStyle}
                            onMouseEnter={(e) => handleHover(e, true)}
                            onMouseLeave={(e) => handleHover(e, false)}
                        >
                            <h3 style={styles.sectionTitle}>📅 {booking.event_name} (ID: {booking.event_id})</h3>
                            <p style={styles.detail}>**Date:** {booking.event_date}</p>
                            
                            <h4 style={styles.subTitle}>👤 Client Details</h4>
                            <p style={styles.detail}>**Name:** {booking.client_name}</p>
                            <p style={styles.detail}>**Email:** {booking.client_email}</p>
                            <p style={styles.detail}>**Client ID:** {booking.client_id}</p>
                            
                            <h4 style={styles.subTitle}>💰 Financial & Vendor</h4>
                            <p style={styles.detail}>**Booking ID:** {booking.booking_id}</p>
                            <p style={styles.detail}>**Vendor:** {booking.vendor_name} ({booking.service_type})</p>
                            <p style={styles.cost}>**Cost:** ${booking.service_cost.toFixed(2)}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

// --- Aesthetic Styling ---
const styles = {
    grid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
        gap: '20px',
    },
    sectionTitle: {
        color: '#007bff',
        borderBottom: '1px solid #eee',
        paddingBottom: '5px',
        marginBottom: '10px',
        fontSize: '1.2em'
    },
    subTitle: {
        color: '#555',
        marginTop: '15px',
        marginBottom: '5px',
        fontSize: '1em'
    },
    detail: {
        margin: '5px 0',
        fontSize: '0.95em',
    },
    cost: {
        marginTop: '10px',
        fontSize: '1.1em',
        fontWeight: 'bold',
        color: 'darkgreen'
    }
};

export default AdminBookingsPage;