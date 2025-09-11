import React from 'react';
import { Box } from '@mui/material';
import LoginForm from '../components/auth/LoginForm';

const LoginPage: React.FC = () => {
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
            <LoginForm onSwitchToRegister={() => { }} />
        </Box>
    );
};

export default LoginPage;
