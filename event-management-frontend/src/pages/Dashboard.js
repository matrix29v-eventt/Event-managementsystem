// import React, { useState, useEffect } from 'react';
// import axiosInstance from '../axiosInstance';
// import { useAuth } from '../AuthContext';
// import Header from '../components/Header';
// import { Link } from 'react-router-dom';

// const Dashboard = () => {
//     const { userRole } = useAuth();
    
//     const [venues, setVenues] = useState([]);
//     const [vendors, setVendors] = useState([]); 
//     const [loading, setLoading] = useState(true); 

//     useEffect(() => {
//         const fetchData = async () => {
//             try {
//                 // Fetch both Venues and Vendors concurrently
//                 const [venuesResponse, vendorsResponse] = await Promise.all([
//                     axiosInstance.get('/venues/'),
//                     axiosInstance.get('/vendors/') 
//                 ]);
                
//                 setVenues(venuesResponse.data); 
//                 setVendors(vendorsResponse.data); 
//             } catch (error) {
//                 // Log error if fetch fails (e.g., server down, token expired)
//                 console.error("Failed to fetch data:", error);
//                 // Optionally handle 401 or 403 errors here for user feedback
//             } finally {
//                 setLoading(false);
//             }
//         };
//         fetchData();
//     }, []);

//     return (
//         <div>
            
//             <div style={{ padding: '20px' }}>
//                 <h1>Welcome, {userRole ? userRole.toUpperCase() : 'User'}!</h1>
                
//                 {/* Link to the event creation page */}
//                 <Link to="/create-event" style={{ display: 'inline-block', padding: '10px 20px', background: 'green', color: 'white', textDecoration: 'none', marginBottom: '20px', marginRight: '20px' }}>
//                     Create New Event & Booking
//                 </Link>

//                 {/* Link to Admin Panel (if not already in the Header) */}
//                  {userRole === 'admin' && (
//                     <Link to="/admin/clients" style={{ display: 'inline-block', padding: '10px 20px', background: 'darkred', color: 'white', textDecoration: 'none', marginBottom: '20px' }}>
//                         Go to Admin Panel
//                     </Link>
//                 )}


//                 {loading ? (
//                     <p>Loading data...</p>
//                 ) : (
//                     <>
//                         {/* --- VENUES LIST --- */}
//                         <h2>Available Venues</h2>
//                         <ul>
//                             {venues.length > 0 ? (
//                                 venues.map(venue => (
//                                     <li key={venue.id}>{venue.name} - Capacity: {venue.capacity}</li>
//                                 ))
//                             ) : (
//                                 <li>No venues found.</li>
//                             )}
//                         </ul>

//                         <hr style={{ margin: '30px 0' }} />

//                         {/* --- VENDOR LIST --- */}
//                         <h2>Available Vendors</h2>
//                         <ul>
//                             {vendors.length > 0 ? (
//                                 vendors.map(vendor => (
//                                     <li key={vendor.id}>{vendor.name} ({vendor.service_type}) - Contact: {vendor.contact}</li>
//                                 ))
//                             ) : (
//                                 <li>No vendors found.</li>
//                             )}
//                         </ul>
//                     </>
//                 )}
//             </div>
//         </div>
//     );
// };

// export default Dashboard;

// src/pages/Dashboard.js (The new Home Page)

import React from 'react';
// 💡 Import the Event Booking Form component
import EventBookingForm from '../pages/EventBookingForm'; 
// NOTE: Assuming EventBookingForm.js is the content of your old CreateEventPage.js

const Dashboard = () => {
    // The main dashboard component now just acts as the container for the form (Home Page)
    return (
        <>
            {/* 💡 RENDER THE FORM DIRECTLY */}
            <EventBookingForm /> 
        </>
    );
};

export default Dashboard;