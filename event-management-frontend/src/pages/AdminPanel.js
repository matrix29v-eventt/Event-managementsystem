import React, { useState, useEffect } from 'react';
import axiosInstance from '../axiosInstance';
import Header from '../components/Header'; // Assuming Header is in components/

const AdminPanel = () => {
    const [clientList, setClientList] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAllClients = async () => {
            try {
                // 💡 This route is protected by role_required("admin") on the backend
                const response = await axiosInstance.get('/clients/'); 
                setClientList(response.data);
            } catch (error) {
                // This will catch the 403 Forbidden error if a client somehow bypassed the AdminRoute component barrier
                console.error("Access denied by backend:", error.response);
            } finally {
                setLoading(false);
            }
        };
        fetchAllClients();
    }, []);

    return (
        <div>
            
            <div style={{ padding: '20px' }}>
                <h1>Admin Client Management</h1>
                <h3>Total Clients: {clientList.length}</h3>
                
                {loading ? (
                    <p>Loading clients...</p>
                ) : (
                    <table border="1" style={{ width: '100%' }}>
                        <thead>
                            <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th></tr>
                        </thead>
                        <tbody>
                            {clientList.map(client => (
                                <tr key={client.id}>
                                    <td>{client.id}</td>
                                    <td>{client.name}</td>
                                    <td>{client.email}</td>
                                    <td>{client.role}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default AdminPanel;