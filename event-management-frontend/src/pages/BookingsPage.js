import React, { useState, useEffect } from 'react';
import axiosInstance from '../axiosInstance';
import Header from '../components/Header';
import { useAuth } from '../AuthContext';

const BookingsPage = () => {
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);
    const { logout } = useAuth();

    useEffect(() => {
        const fetchBookings = async () => {
            try {
                // Calls the endpoint which returns detailed client data
                const response = await axiosInstance.get('/bookings/my-bookings'); 
                setBookings(response.data);
            } catch (error) {
                console.error("Failed to fetch user bookings:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchBookings();
    }, []);

     // --- NEW: Delete Handler ---
    const handleDelete = async (bookingId) => {
        if (window.confirm(`Are you sure you want to cancel Booking Ref #${bookingId}?`)) {
            try {
                // 💡 Call the new DELETE endpoint
                await axiosInstance.delete(`/bookings/${bookingId}`);
                
                // 💡 FIX: Update the state to remove the deleted booking instantly
                setBookings(bookings.filter(b => b.booking_id !== bookingId));
                
            } catch (error) {
                console.error("Deletion failed:", error.response);
                alert('Deletion failed: You may not have permission, or the booking is already gone.');
            }
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    };

    // Styling handler for lighter hover effect
    const handleHover = (e, isHovering) => {
        e.currentTarget.style.transform = isHovering ? 'translateY(-3px)' : 'translateY(0)';
        e.currentTarget.style.boxShadow = isHovering ? '0 6px 15px rgba(0,0,0,0.1)' : '0 1px 5px rgba(0,0,0,0.05)';
    };

    return (
        <div>
            <h1 style={styles.header}>My Event Bookings</h1>
            
            {loading ? (
                <p>Loading bookings...</p>
            ) : (
                bookings.length > 0 ? (
                    <div style={styles.grid}>
                        {bookings.map(booking => (
                            <div 
                                key={booking.booking_id} 
                                style={styles.card}
                                onMouseEnter={(e) => handleHover(e, true)}
                                onMouseLeave={(e) => handleHover(e, false)}
                            >
                                <div style={styles.statusPill}>BOOKED</div>
                                <h3 style={styles.eventTitle}>{booking.event_name}</h3>
                                
                                <div style={styles.detailContainer}>
                                    <p style={styles.detail}>📅 Date: {formatDate(booking.event_date)}</p>
                                    <p style={styles.detail}>📍 Venue: {booking.venue_name}</p>
                                    <p style={styles.detail}>🧑‍🍳 Vendor: {booking.vendor_name}</p>
                                </div>
                                
                                <div style={styles.costBox}>
                                    <span style={styles.costLabel}>Booking Ref #: {booking.booking_id}</span>
                                    <span style={styles.costValue}>${booking.service_cost.toFixed(2)}</span>
                                </div>

                                {/* 💡 NEW: Delete Button */}
                                <button 
                                    onClick={() => handleDelete(booking.booking_id)} 
                                    style={styles.deleteButton}
                                >
                                    Cancel Booking
                                </button>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p style={{ marginTop: '20px', fontSize: '1.1em' }}>You have no current or past bookings.</p>
                )
            )}
        </div>
    );
};

// --- Aesthetic Styling (Lighter/Minimalist) ---
const styles = {

    deleteButton: {
        background: '#820411ff', /* Red */
        color: 'white',
        border: 'none',
        padding: '8px 12px',
        borderRadius: '5px',
        cursor: 'pointer',
        marginTop: '15px',
        width: '60%',
        fontSize: '0.98em',
        transition: 'background-color 0.2s',
        '&:hover': {
            backgroundColor: '#150002ff',
        }
    },

    header: {
        borderBottom: '2px solid #007bff',
        paddingBottom: '10px',
        marginBottom: '30px',
        color: '#333'
    },
    grid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
        gap: '20px',
    },
    card: {
        background: '#fff',
        border: '1px solid #eee', // Lighter border
        borderRadius: '10px',
        padding: '20px',
        transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
        cursor: 'pointer',
        position: 'relative',
        boxShadow: '0 1px 5px rgba(0,0,0,0.05)',
        minHeight: '200px'
    },
    eventTitle: {
        color: '#1a1a1a',
        marginBottom: '10px',
        fontSize: '1.4em',
        fontWeight: '700'
    },
    detailContainer: {
        marginBottom: '15px',
        paddingLeft: '10px',
        borderLeft: '3px solid #ccc'
    },
    detail: {
        margin: '5px 0',
        fontSize: '1.1em',
        color: '#393939ff',
    },
    statusPill: {
        position: 'absolute',
        top: '20px',
        right: '20px',
        background: '#d4edda',
        color: '#155724',
        padding: '5px 10px',
        borderRadius: '20px',
        fontSize: '0.8em',
        fontWeight: 'bold',
    },
    costBox: {
        marginTop: 'auto',
        paddingTop: '10px',
        borderTop: '1px solid #f0f0f0',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    costLabel: {
        fontSize: '0.9em',
        color: '#777'
    },
    costValue: {
        fontSize: '1.3em',
        fontWeight: 'bold',
        color: 'darkgreen'
    }
};

export default BookingsPage;