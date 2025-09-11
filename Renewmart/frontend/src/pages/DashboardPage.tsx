import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import DashboardStats from '../components/dashboard/DashboardStats';

const DashboardPage: React.FC = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Welcome to RenewMart - Your Land Development Management Platform
        </Typography>
      </Box>

      <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          System Overview
        </Typography>
        <DashboardStats />
      </Paper>

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
        <Paper elevation={1} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Recent Activity
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Recent system activity will be displayed here.
          </Typography>
        </Paper>

        <Paper elevation={1} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Quick Actions
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Quick action buttons will be displayed here.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default DashboardPage;
