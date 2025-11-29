// // import React, { createContext, useState, useContext } from 'react';
// // import { jwtDecode } from 'jwt-decode'; // 💡 NEW: Import jwtDecode

// // const AuthContext = createContext(null);

// // export const AuthProvider = ({ children }) => {
// //     const storedToken = localStorage.getItem('access_token');
// //     const [token, setToken] = useState(storedToken);
    
// //     // 💡 FIX: Initialize role by decoding the stored token if it exists
// //     const initialRole = storedToken ? jwtDecode(storedToken).role : null;
// //     const [userRole, setUserRole] = useState(initialRole);

// //     const login = (jwtToken) => {
// //         // Decode the token to get the role directly from the source
// //         const payload = jwtDecode(jwtToken);
// //         const role = payload.role; 

// //         setToken(jwtToken);
// //         setUserRole(role);
// //         localStorage.setItem('access_token', jwtToken);
// //     };

// //     const logout = () => {
// //         setToken(null);
// //         setUserRole(null);
// //         localStorage.removeItem('access_token');
// //     };

// //     const isAuthenticated = !!token;
// //     const isAdmin = userRole === 'admin';

// //     return (
// //         <AuthContext.Provider value={{ token, isAuthenticated, userRole, isAdmin, login, logout }}>
// //             {children}
// //         </AuthContext.Provider>
// //     );
// // };

// // export const useAuth = () => useContext(AuthContext);

// import React, { createContext, useState, useContext } from 'react';
// // 💡 IMPORTANT: Remove any import for 'jwt-decode'

// const AuthContext = createContext(null);

// export const AuthProvider = ({ children }) => {
//     const [token, setToken] = useState(localStorage.getItem('access_token'));
    
//     // Role will now be set only during the login function call
//     const [userRole, setUserRole] = useState(null); 

//     // 💡 FIX: Login now accepts the 'role' argument directly
//     const login = (jwtToken, role) => { 
//         setToken(jwtToken);
//         setUserRole(role); // Use the role passed from LoginPage
//         localStorage.setItem('access_token', jwtToken);
//     };

//     const logout = () => {
//         setToken(null);
//         setUserRole(null);
//         localStorage.removeItem('access_token');
//     };

//     const isAuthenticated = !!token;
//     const isAdmin = userRole === 'admin';

//     return (
//         <AuthContext.Provider value={{ token, isAuthenticated, userRole, isAdmin, login, logout }}>
//             {children}
//         </AuthContext.Provider>
//     );
// };

// export const useAuth = () => useContext(AuthContext);

import React, { createContext, useState, useContext } from 'react';
// Note: jwt-decode is not needed for the temporary lab fix
// If using jwt-decode, you MUST install it: npm install jwt-decode

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('access_token'));
    const [userRole, setUserRole] = useState(null);
    const [userId, setUserId] = useState(null); // 💡 NEW STATE: Stores client's database ID

    // 💡 FIX: Login now accepts the 'role' AND 'id' arguments
    const login = (jwtToken, role, id) => { 
        setToken(jwtToken);
        setUserRole(role); 
        setUserId(id); // Store the ID
        localStorage.setItem('access_token', jwtToken);
    };

    const logout = () => {
        setToken(null);
        setUserRole(null);
        setUserId(null); // Clear ID on logout
        localStorage.removeItem('access_token');
    };

    const isAuthenticated = !!token;
    const isAdmin = userRole === 'admin';

    return (
        <AuthContext.Provider value={{ token, isAuthenticated, userRole, isAdmin, login, logout, userId }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);