import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout, loading } = useAuth();
  const navigate = useNavigate();

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return navigate('/login');
  }

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Welcome, {user.email}!</h1>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </header>

      <main className="dashboard-content">
        <div className="card">
          <h2>Your Account</h2>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Account created:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
        </div>

        <div className="card">
          <h2>Appointments</h2>
          <p>Your appointments will appear here once you book them.</p>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
