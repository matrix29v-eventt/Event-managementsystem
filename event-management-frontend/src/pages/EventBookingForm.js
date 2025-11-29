// import React, { useState, useEffect } from 'react';
// import axiosInstance from '../axiosInstance';
// import { useNavigate } from 'react-router-dom';
// import { useAuth } from '../AuthContext'; // Import useAuth to get user ID
// import Header from '../components/Header';

// // --- Static Data for Event Name Options ---
// const EVENT_NAME_OPTIONS = [
//     { name: "Wedding Reception", cost: 15000 },
//     { name: "Alumni Gathering", cost: 8000 },
//     { name: "Annual Fest", cost: 12000 },
//     { name: "Product Launch", cost: 9500 },
//     { name: "Company Retreat", cost: 5000 }
// ];

// const CreateEventPage = () => {
//     // 💡 Get Client ID from context (assuming you updated AuthContext with ID, or use 2 for now)
//     const { userRole } = useAuth();
//     const CLIENT_ID = userRole === 'admin' ? 1 : 2; // Default to Client ID 2 if not admin

//     // --- State Management ---
//     const [venues, setVenues] = useState([]);
//     const [vendors, setVendors] = useState([]);
//     const [loadingData, setLoadingData] = useState(true);
//     const [submitting, setSubmitting] = useState(false);
    
//     const [formState, setFormState] = useState({
//         eventName: '',
//         venueId: '',
//         date: '',
//         vendorId: '',
//         vendorCost: 0,
//     });
//     const [feedback, setFeedback] = useState({ message: '', type: '' });
//     const navigate = useNavigate();

//     // --- 1. Fetch Prerequisite Data (Venues and Vendors) ---
//     useEffect(() => {
//         const fetchPrerequisites = async () => {
//             try {
//                 const [venuesRes, vendorsRes] = await Promise.all([
//                     axiosInstance.get('/venues/'),
//                     axiosInstance.get('/vendors/')
//                 ]);

//                 setVenues(venuesRes.data);
//                 setVendors(vendorsRes.data);
                
//                 // Set default selections if data is available
//                 if (venuesRes.data.length > 0) setFormState(prev => ({ ...prev, venueId: venuesRes.data[0].id }));
//                 if (vendorsRes.data.length > 0) setFormState(prev => ({ ...prev, vendorId: vendorsRes.data[0].id }));
//             } catch (error) {
//                 console.error("Error fetching prerequisites:", error);
//                 setFeedback({ message: "Failed to load venue/vendor lists.", type: 'error' });
//             } finally {
//                 setLoadingData(false);
//             }
//         };
//         fetchPrerequisites();
//     }, []);

//     // --- 2. Handle Form Input Changes ---
//     const handleChange = (e) => {
//         const { name, value } = e.target;

//         if (name === 'eventName') {
//             // Find the corresponding cost for the selected event name
//             const selectedEvent = EVENT_NAME_OPTIONS.find(opt => opt.name === value);
//             setFormState(prev => ({
//                 ...prev,
//                 eventName: value,
//                 vendorCost: selectedEvent ? selectedEvent.cost : 0
//             }));
//         } else {
//             setFormState(prev => ({ ...prev, [name]: value }));
//         }
//     };

//     // --- 3. Handle Secure Submission ---
//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setSubmitting(true);
//         setFeedback({ message: '', type: '' });

//         const { eventName, date, venueId, vendorId, vendorCost } = formState;

//         // Check date validation (Quick frontend check)
//         if (new Date(date) < new Date()) {
//             setFeedback({ message: "❌ Event date cannot be in the past.", type: 'error' });
//             setSubmitting(false);
//             return;
//         }

//         try {
//             // 1. POST Event (requires Client/Admin token and correct client_id)
//             const eventPayload = {
//                 name: eventName,
//                 date: date,
//                 client_id: CLIENT_ID, // Use the ID of the logged-in user
//                 venue_id: parseInt(venueId)
//             };
//             const eventResponse = await axiosInstance.post('/events/', eventPayload);
//             const newEventId = eventResponse.data.id;
            
//             // 2. POST Booking (requires Auth token)
//             const bookingPayload = {
//                 event_id: newEventId,
//                 vendor_id: parseInt(vendorId),
//                 service_cost: parseFloat(vendorCost)
//             };
//             await axiosInstance.post('/bookings/', bookingPayload);

//             // Success feedback and form reset
//             setFeedback({ message: '✅ Event booked successfully!', type: 'success' });
//             setFormState({ // Reset form fields
//                 eventName: '',
//                 venueId: venues.length > 0 ? venues[0].id : '',
//                 date: '',
//                 vendorId: vendors.length > 0 ? vendors[0].id : '',
//                 vendorCost: 0,
//             });

//         } catch (error) {
//             console.error("Booking submission failed:", error.response?.data);
//             setFeedback({ message: `❌ Error: ${error.response?.data?.detail || "Could not complete booking."}`, type: 'error' });
//         } finally {
//             setSubmitting(false);
//         }
//     };

//     if (loadingData) return (<div><Header /><p style={{ padding: '20px' }}>Loading prerequisites...</p></div>);

//     // --- 4. Render the Elegant Form ---
//     return (
//         <div>
//             <Header />
//             <div style={styles.container}>
//                 <h1 style={styles.header}>Create New Event & Booking</h1>
                
//                 {feedback.message && (
//                     <p style={feedback.type === 'success' ? styles.success : styles.error}>
//                         {feedback.message}
//                     </p>
//                 )}

//                 <form onSubmit={handleSubmit} style={styles.formGrid}>
//                     <div style={styles.sectionHeader}>Event & Venue Details (Client ID: {CLIENT_ID})</div>

//                     {/* 1. Event Name Dropdown */}
//                     <label htmlFor="eventName" style={styles.label}>Event Name:</label>
//                     <select name="eventName" value={formState.eventName} onChange={handleChange} required style={styles.input}>
//                         <option value="" disabled>Select Event Type</option>
//                         {EVENT_NAME_OPTIONS.map(opt => (
//                             <option key={opt.name} value={opt.name}>{opt.name}</option>
//                         ))}
//                     </select>

//                     {/* 2. Date Input */}
//                     <label htmlFor="date" style={styles.label}>Event Date:</label>
//                     <input name="date" value={formState.date} onChange={handleChange} type="date" required style={styles.input} />

//                     {/* 3. Venue Dropdown */}
//                     <label htmlFor="venueId" style={styles.label}>Select Venue (Capacity):</label>
//                     <select name="venueId" value={formState.venueId} onChange={handleChange} required style={styles.input}>
//                         {venues.map(venue => (
//                             <option key={venue.id} value={venue.id}>
//                                 {venue.name} (Cap: {venue.capacity})
//                             </option>
//                         ))}
//                     </select>

//                     <div style={styles.sectionHeader}>Vendor & Cost Details</div>

//                     {/* 4. Vendor Dropdown */}
//                     <label htmlFor="vendorId" style={styles.label}>Select Vendor:</label>
//                     <select name="vendorId" value={formState.vendorId} onChange={handleChange} required style={styles.input}>
//                         {vendors.map(vendor => (
//                             <option key={vendor.id} value={vendor.id}>
//                                 {vendor.name} ({vendor.service_type})
//                             </option>
//                         ))}
//                     </select>

//                     {/* 5. Cost Input (Dynamically set based on Event Name, but editable) */}
//                     <label htmlFor="vendorCost" style={styles.label}>Vendor/Service Cost:</label>
//                     <input 
//                         name="vendorCost" 
//                         value={formState.vendorCost} 
//                         onChange={handleChange} 
//                         type="number" 
//                         placeholder="0.00"
//                         required 
//                         style={styles.input} 
//                         readOnly={!!formState.eventName} // Make read-only if event name sets the cost
//                     />
//                     <p style={{ color: '#555', fontSize: '12px', gridColumn: '2/3', margin: 0 }}>
//                         {formState.eventName ? `*Cost suggested based on ${formState.eventName}` : '*Select event type to see suggested cost.'}
//                     </p>

//                     {/* 6. Submit Button */}
//                     <button type="submit" disabled={submitting} style={styles.submitButton}>
//                         {submitting ? 'Booking...' : 'Book Event'}
//                     </button>
//                 </form>
//             </div>
//         </div>
//     );
// };

// // --- Aesthetic Styling ---
// const styles = {
//     container: {
//         padding: '40px',
//         maxWidth: '800px',
//         margin: '30px auto',
//         border: '1px solid #ddd',
//         borderRadius: '8px',
//         boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
//         background: '#fff'
//     },
//     header: {
//         textAlign: 'center',
//         color: '#333',
//         marginBottom: '30px'
//     },
//     formGrid: {
//         display: 'grid',
//         gridTemplateColumns: '200px 1fr',
//         gap: '15px 30px',
//         alignItems: 'center',
//     },
//     sectionHeader: {
//         gridColumn: '1 / 3',
//         fontSize: '1.2em',
//         fontWeight: 'bold',
//         color: '#007bff',
//         marginTop: '20px',
//         marginBottom: '10px',
//         borderBottom: '2px solid #007bff'
//     },
//     label: {
//         fontWeight: 'bold',
//         color: '#555',
//     },
//     input: {
//         padding: '10px',
//         borderRadius: '4px',
//         border: '1px solid #ccc',
//         width: '100%',
//         boxSizing: 'border-box'
//     },
//     submitButton: {
//         gridColumn: '1 / 3',
//         padding: '15px',
//         background: '#28a745',
//         color: 'white',
//         border: 'none',
//         borderRadius: '4px',
//         cursor: 'pointer',
//         fontSize: '1.1em',
//         marginTop: '20px'
//     },
//     success: {
//         color: '#155724',
//         backgroundColor: '#d4edda',
//         padding: '10px',
//         borderRadius: '4px',
//         textAlign: 'center',
//         marginBottom: '20px'
//     },
//     error: {
//         color: '#721c24',
//         backgroundColor: '#f8d7da',
//         padding: '10px',
//         borderRadius: '4px',
//         textAlign: 'center',
//         marginBottom: '20px'
//     }
// };

// export default CreateEventPage;

import React, { useState, useEffect } from 'react';
import axiosInstance from '../axiosInstance';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import Header from '../components/Header';

// --- Static Data for Event Name Options ---
const EVENT_NAME_OPTIONS = [
    { name: "Wedding Reception", cost: 15000 },
    { name: "Alumni Gathering", cost: 8000 },
    { name: "Annual Fest", cost: 12000 },
    { name: "Product Launch", cost: 9500 },
    { name: "Company Retreat", cost: 5000 }
];

const EventBookingForm = () => {
    // 💡 FIX: Get userId dynamically from context
    const { userId } = useAuth();
    
    // --- State Management ---
    const [venues, setVenues] = useState([]);
    const [vendors, setVendors] = useState([]);
    const [loadingData, setLoadingData] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    
    const [formState, setFormState] = useState({
        eventName: '',
        venueId: '',
        date: '',
        vendorId: '',
        vendorCost: 0,
    });
    const [feedback, setFeedback] = useState({ message: '', type: '' });
    const navigate = useNavigate();

    // --- 1. Fetch Prerequisite Data (Venues and Vendors) ---
    // 💡 FIX: Ensure this runs only AFTER userId is available
    useEffect(() => {
        if (!userId) {
            setLoadingData(true);
            return;
        }
        
        const fetchPrerequisites = async () => {
            try {
                const [venuesRes, vendorsRes] = await Promise.all([
                    axiosInstance.get('/venues/'),
                    axiosInstance.get('/vendors/')
                ]);

                setVenues(venuesRes.data);
                setVendors(vendorsRes.data);
                
                // Set default selections
                if (venuesRes.data.length > 0) setFormState(prev => ({ ...prev, venueId: venuesRes.data[0].id }));
                if (vendorsRes.data.length > 0) setFormState(prev => ({ ...prev, vendorId: vendorsRes.data[0].id }));
            } catch (error) {
                console.error("Error fetching prerequisites:", error);
                setFeedback({ message: "Failed to load venue/vendor lists.", type: 'error' });
            } finally {
                setLoadingData(false);
            }
        };
        fetchPrerequisites();
    }, [userId]); // Depend on userId

    // --- 2. Handle Form Input Changes ---
    const handleChange = (e) => {
        const { name, value } = e.target;

        if (name === 'eventName') {
            const selectedEvent = EVENT_NAME_OPTIONS.find(opt => opt.name === value);
            setFormState(prev => ({
                ...prev,
                eventName: value,
                vendorCost: selectedEvent ? selectedEvent.cost : 0
            }));
        } else {
            setFormState(prev => ({ ...prev, [name]: value }));
        }
    };

    // --- 3. Handle Secure Submission ---
    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        setFeedback({ message: '', type: '' });

        const { eventName, date, venueId, vendorId, vendorCost } = formState;

        // Validation check (Quick frontend check)
        if (new Date(date) < new Date()) {
            setFeedback({ message: "❌ Event date cannot be in the past.", type: 'error' });
            setSubmitting(false);
            return;
        }

        try {
            // 1. POST Event
            const eventPayload = {
                name: eventName,
                date: date,
                client_id: userId, // 💡 FIX: Use dynamic userId for ownership
                venue_id: parseInt(venueId)
            };
            const eventResponse = await axiosInstance.post('/events/', eventPayload);
            const newEventId = eventResponse.data.id;
            
            // 2. POST Booking
            const bookingPayload = {
                event_id: newEventId,
                vendor_id: parseInt(vendorId),
                service_cost: parseFloat(vendorCost)
            };
            await axiosInstance.post('/bookings/', bookingPayload);

            // Success feedback and form reset
            setFeedback({ message: '✅ Event booked successfully!', type: 'success' });
            setFormState({ // Reset form fields
                eventName: '',
                venueId: venues.length > 0 ? venues[0].id : '',
                date: '',
                vendorId: vendors.length > 0 ? vendors[0].id : '',
                vendorCost: 0,
            });

        } catch (error) {
            console.error("Booking submission failed:", error.response?.data);
            setFeedback({ message: `❌ Error: ${error.response?.data?.detail || "Could not complete transaction."}`, type: 'error' });
        } finally {
            setSubmitting(false);
        }
    };

    if (loadingData) return (<div><Header /><p style={{ padding: '20px' }}>Loading prerequisites...</p></div>);

    // --- 4. Render the Elegant Form ---
    return (
        <div>
            
            <div style={styles.container}>
                <h1 style={styles.header}>Create New Event & Booking</h1>
                
                {/* Display Feedback */}
                {feedback.message && (
                    <p style={feedback.type === 'success' ? styles.success : styles.error}>
                        {feedback.message}
                    </p>
                )}

                <form onSubmit={handleSubmit} style={styles.formGrid}>
                    <div style={styles.sectionHeader}>Event & Venue Details (Client ID: {userId})</div>

                    {/* 1. Event Name Dropdown */}
                    <label htmlFor="eventName" style={styles.label}>Event Name:</label>
                    <select name="eventName" value={formState.eventName} onChange={handleChange} required style={styles.input}>
                        <option value="" disabled>Select Event Type</option>
                        {EVENT_NAME_OPTIONS.map(opt => (
                            <option key={opt.name} value={opt.name}>{opt.name}</option>
                        ))}
                    </select>

                    {/* 2. Date Input */}
                    <label htmlFor="date" style={styles.label}>Event Date:</label>
                    <input name="date" value={formState.date} onChange={handleChange} type="date" required style={styles.input} />

                    {/* 3. Venue Dropdown */}
                    <label htmlFor="venueId" style={styles.label}>Select Venue (Capacity):</label>
                    <select name="venueId" value={formState.venueId} onChange={handleChange} required style={styles.input}>
                        {venues.map(venue => (
                            <option key={venue.id} value={venue.id}>
                                {venue.name} (Cap: {venue.capacity})
                            </option>
                        ))}
                    </select>

                    <div style={styles.sectionHeader}>Vendor & Cost Details</div>

                    {/* 4. Vendor Dropdown */}
                    <label htmlFor="vendorId" style={styles.label}>Select Vendor:</label>
                    <select name="vendorId" value={formState.vendorId} onChange={handleChange} required style={styles.input}>
                        {vendors.map(vendor => (
                            <option key={vendor.id} value={vendor.id}>
                                {vendor.name} ({vendor.service_type})
                            </option>
                        ))}
                    </select>

                    {/* 5. Cost Input */}
                    <label htmlFor="vendorCost" style={styles.label}>Vendor/Service Cost:</label>
                    <input 
                        name="vendorCost" 
                        value={formState.vendorCost} 
                        onChange={handleChange} 
                        type="number" 
                        placeholder="0.00"
                        required 
                        style={styles.input} 
                        readOnly={!!formState.eventName} 
                    />
                    <p style={{ color: '#555', fontSize: '12px', gridColumn: '2/3', margin: 0 }}>
                        {formState.eventName ? `*Cost suggested based on ${formState.eventName}` : '*Select event type to see suggested cost.'}
                    </p>

                    {/* 6. Submit Button */}
                    <button type="submit" disabled={submitting} style={styles.submitButton}>
                        {submitting ? 'Booking...' : 'Book Event'}
                    </button>
                </form>
            </div>
        </div>
    );
};

// --- Aesthetic Styling ---
const styles = {
    container: {
        padding: '40px',
        maxWidth: '800px',
        margin: '30px auto',
        border: '1px solid #ddd',
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
        background: '#fff'
    },
    header: {
        textAlign: 'center',
        color: '#333',
        marginBottom: '30px'
    },
    formGrid: {
        display: 'grid',
        gridTemplateColumns: '200px 1fr',
        gap: '15px 30px',
        alignItems: 'center',
    },
    sectionHeader: {
        gridColumn: '1 / 3',
        fontSize: '1.2em',
        fontWeight: 'bold',
        color: '#007bff',
        marginTop: '20px',
        marginBottom: '10px',
        borderBottom: '2px solid #007bff'
    },
    label: {
        fontWeight: 'bold',
        color: '#555',
    },
    input: {
        padding: '10px',
        borderRadius: '4px',
        border: '1px solid #ccc',
        width: '100%',
        boxSizing: 'border-box'
    },
    submitButton: {
        gridColumn: '1 / 3',
        padding: '15px',
        background: '#108a6dff',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '1.1em',
        marginTop: '20px'
    },
    success: {
        color: '#155724',
        backgroundColor: '#d4edda',
        padding: '10px',
        borderRadius: '4px',
        textAlign: 'center',
        marginBottom: '20px'
    },
    error: {
        color: '#721c24',
        backgroundColor: '#f8d7da',
        padding: '10px',
        borderRadius: '4px',
        textAlign: 'center',
        marginBottom: '20px'
    }
};

export default EventBookingForm;