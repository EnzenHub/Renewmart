import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';
import { CssBaseline, Box, CircularProgress } from '@mui/material';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/layout/Layout';
import AuthPage from './pages/AuthPage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import LandownerDashboardPage from './pages/LandownerDashboardPage';
import UsersPage from './pages/UsersPage';
import LandParcelsPage from './pages/LandParcelsPage';

// Centralized theme imported from ./theme

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }

  return <Layout>{children}</Layout>;
};

// Public Route Component (redirects to role home if already authenticated)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading, user } = useAuth();

  if (isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (isAuthenticated) {
    const roleHome = user?.user_type === 'landowner' ? '/landowner' : '/dashboard';
    return <Navigate to={roleHome} replace />;
  }

  return <>{children}</>;
};

// Placeholder components for other pages
const TasksPage: React.FC = () => (
  <div style={{ padding: '20px' }}>
    <h2>Tasks Management</h2>
    <p>Tasks management page will be implemented here.</p>
  </div>
);

const OpportunitiesPage: React.FC = () => (
  <div style={{ padding: '20px' }}>
    <h2>Investment Opportunities</h2>
    <p>Investment opportunities page will be implemented here.</p>
  </div>
);

const ProposalsPage: React.FC = () => (
  <div style={{ padding: '20px' }}>
    <h2>Investment Proposals</h2>
    <p>Investment proposals page will be implemented here.</p>
  </div>
);

const ProjectsPage: React.FC = () => (
  <div style={{ padding: '20px' }}>
    <h2>Development Projects</h2>
    <p>Development projects page will be implemented here.</p>
  </div>
);

const DocumentsPage: React.FC = () => (
  <div style={{ padding: '20px' }}>
    <h2>Documents</h2>
    <p>Documents management page will be implemented here.</p>
  </div>
);

const ApprovalsPage: React.FC = () => (
  <div style={{ padding: '20px' }}>
    <h2>Approvals</h2>
    <p>Approvals management page will be implemented here.</p>
  </div>
);

const NotificationsPage: React.FC = () => (
  <div style={{ padding: '20px' }}>
    <h2>Notifications</h2>
    <p>Notifications page will be implemented here.</p>
  </div>
);

const SettingsPage: React.FC = () => (
  <div style={{ padding: '20px' }}>
    <h2>Settings</h2>
    <p>Settings page will be implemented here.</p>
  </div>
);

const ProfilePage: React.FC = () => (
  <div style={{ padding: '20px' }}>
    <h2>Profile</h2>
    <p>User profile page will be implemented here.</p>
  </div>
);

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            {/* Public Routes */}
            <Route
              path="/auth"
              element={
                <PublicRoute>
                  <AuthPage />
                </PublicRoute>
              }
            />
            <Route
              path="/login"
              element={
                <PublicRoute>
                  <LoginPage />
                </PublicRoute>
              }
            />

            {/* Protected Routes */}
            <Route
              path="/landowner"
              element={
                <ProtectedRoute>
                  <LandownerDashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/users"
              element={
                <ProtectedRoute>
                  <UsersPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/land-parcels"
              element={
                <ProtectedRoute>
                  <LandParcelsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/tasks"
              element={
                <ProtectedRoute>
                  <TasksPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/opportunities"
              element={
                <ProtectedRoute>
                  <OpportunitiesPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/proposals"
              element={
                <ProtectedRoute>
                  <ProposalsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/projects"
              element={
                <ProtectedRoute>
                  <ProjectsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/documents"
              element={
                <ProtectedRoute>
                  <DocumentsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/approvals"
              element={
                <ProtectedRoute>
                  <ApprovalsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/notifications"
              element={
                <ProtectedRoute>
                  <NotificationsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/settings"
              element={
                <ProtectedRoute>
                  <SettingsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />

            {/* Default redirect to role home */}
            <Route
              path="/"
              element={
                <PublicRoute>
                  <Navigate to="/login" replace />
                </PublicRoute>
              }
            />

            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;