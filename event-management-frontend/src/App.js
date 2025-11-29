import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

// --- New Import ---
import Layout from './components/Layout'; 

// --- Component Imports ---
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import AdminPanel from './pages/AdminPanel';
import EventBookingForm from './pages/EventBookingForm'; 
import BookingsPage from './pages/BookingsPage'; // Ensure this is imported
import AdminBookingsPage from './pages/AdminBookingsPage';


const RoleBasedRedirect = () => {
    const { isAuthenticated, isAdmin } = useAuth();
    
    if (!isAuthenticated) return <Navigate to="/login" replace />;
    
    // 💡 FIX: Admins go directly to All Bookings page
    if (isAdmin) return <Navigate to="/admin/bookings" replace />;
    
    // Clients go to their standard dashboard
    return <Navigate to="/dashboard" replace />;
};


// 💡 1. Protected Route: Renders content inside the Layout
const ProtectedRoute = ({ element: Element }) => {
    const { isAuthenticated } = useAuth();
    if (!isAuthenticated) return <Navigate to="/login" replace />;
    
    // 💡 FIX: Return the component wrapped in the Layout
    return (
        <Layout>
            <Element />
        </Layout>
    );
};

// 💡 2. Admin Route: Renders admin content inside the Layout
const AdminRoute = ({ element: Element }) => {
    const { isAuthenticated, isAdmin } = useAuth();
    if (!isAuthenticated) return <Navigate to="/login" replace />;
    if (!isAdmin) return (
        <Layout>
            <h1 style={{ padding: '20px', color: 'darkred' }}>403 Forbidden: Admin Access Required.</h1>
        </Layout>
    );
    // 💡 FIX: Return the component wrapped in the Layout
    return (
        <Layout>
            <Element />
        </Layout>
    );
};

function App() {
    return (
        <Routes>
            {/* PUBLIC ROUTES (No Layout) */}
            {/* NOTE: We must ensure LoginPage itself uses the Header component if needed */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            <Route path="/" element={<RoleBasedRedirect />} />
            
            {/* PROTECTED ROUTES (All use Layout) */}
            <Route path="/dashboard" element={<ProtectedRoute element={Dashboard} />} />
            <Route path="/create-event" element={<ProtectedRoute element={EventBookingForm} />} />
            <Route path="/my-bookings" element={<ProtectedRoute element={BookingsPage} />} />

            {/* ADMIN-ONLY ROUTES (Also use Layout) */}
            <Route path="/admin/clients" element={<AdminRoute element={AdminPanel} />} />
            <Route path="/admin/bookings" element={<AdminRoute element={AdminBookingsPage} />} />

            {/* Default route */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Routes>
    );
}

export default App;

// import React from 'react';
// import { Routes, Route, Navigate } from 'react-router-dom';
// import { useAuth } from './AuthContext';

// // --- Component Imports ---
// import LoginPage from './pages/LoginPage';
// import RegisterPage from './pages/RegisterPage'; // 💡 NEW IMPORT
// import Dashboard from './pages/Dashboard';
// import AdminPanel from './pages/AdminPanel';
// import EventBookingForm from './pages/EventBookingForm'; 
// import BookingsPage from './pages/BookingsPage';

// // 💡 1. Component that requires any valid token (Client or Admin)
// const ProtectedRoute = ({ element: Element }) => {
//     const { isAuthenticated } = useAuth();
//     return isAuthenticated ? <Element /> : <Navigate to="/login" replace />;
// };

// // 💡 2. Component that requires the Admin role
// const AdminRoute = ({ element: Element }) => {
//     const { isAuthenticated, isAdmin } = useAuth();
//     if (!isAuthenticated) return <Navigate to="/login" replace />;
//     if (!isAdmin) return <h1>403 Forbidden: Admin Access Required.</h1>;
//     return <Element />;
// };

// function App() {
//     return (
//         <Routes>
//             {/* PUBLIC ROUTES */}
//             <Route path="/login" element={<LoginPage />} />
//             <Route path="/register" element={<RegisterPage />} /> {/* 💡 NEW ROUTE */}
            
//             {/* PROTECTED ROUTES */}
//             <Route path="/dashboard" element={<ProtectedRoute element={Dashboard} />} />
//             <Route path="/create-event" element={<ProtectedRoute element={EventBookingForm} />} />
//             <Route path="/my-bookings" element={<ProtectedRoute element={BookingsPage} />} />

//             {/* ADMIN-ONLY ROUTES */}
//             <Route path="/admin/clients" element={<AdminRoute element={AdminPanel} />} />

//             {/* Default route */}
//             <Route path="/" element={<Navigate to="/dashboard" replace />} />
//         </Routes>
//     );
// }

// export default App;