import React, { useState } from 'react';
import { Box, Paper, Tabs, Tab } from '@mui/material';
import LoginForm from '../components/auth/LoginForm';
import RegisterForm from '../components/auth/RegisterForm';

const AuthPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleSwitchToRegister = () => {
    setActiveTab(1);
  };

  const handleSwitchToLogin = () => {
    setActiveTab(0);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 2,
      }}
    >
      <Paper
        elevation={10}
        sx={{
          width: '100%',
          maxWidth: 600,
          borderRadius: 2,
          overflow: 'hidden',
        }}
      >
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="fullWidth"
          sx={{
            borderBottom: 1,
            borderColor: 'divider',
            '& .MuiTab-root': {
              py: 2,
              fontSize: '1.1rem',
              fontWeight: 500,
            },
          }}
        >
          <Tab label="Sign In" />
          <Tab label="Sign Up" />
        </Tabs>
        
        <Box sx={{ p: 0 }}>
          {activeTab === 0 && (
            <LoginForm onSwitchToRegister={handleSwitchToRegister} />
          )}
          {activeTab === 1 && (
            <RegisterForm onSwitchToLogin={handleSwitchToLogin} />
          )}
        </Box>
      </Paper>
    </Box>
  );
};

export default AuthPage;
