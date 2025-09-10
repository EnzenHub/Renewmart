import React from 'react';
import { Box } from '@mui/material';
import RegisterForm from '../components/auth/RegisterForm';

const AuthPage: React.FC = () => {
  // This page now exclusively shows the Create Account (Register) flow

  return (
    <Box
      sx={{
        minHeight: '100vh',
        backgroundImage: 'url(/bglogin.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 2,
      }}
    >
      <RegisterForm onSwitchToLogin={() => { }} />
    </Box>
  );
};

export default AuthPage;
