import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Person as PersonIcon,
  LocationOn as LocationIcon,
  Assignment as TaskIcon,
  Business as BusinessIcon,
  TrendingUp as TrendingUpIcon,
  Description as DocumentIcon,
} from '@mui/icons-material';
import { DashboardStats as DashboardStatsType } from '../../types';
import { apiService } from '../../services/api';

const DashboardStats: React.FC = () => {
  const [stats, setStats] = useState<DashboardStatsType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const data = await apiService.getDashboardStats();
        setStats(data);
        setError('');
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard statistics');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!stats) {
    return null;
  }

  const statCards = [
    {
      title: 'Total Users',
      value: stats.totalUsers,
      icon: <PersonIcon color="primary" sx={{ fontSize: 40 }} />,
      color: 'primary',
    },
    {
      title: 'Land Parcels',
      value: stats.totalParcels,
      icon: <LocationIcon color="success" sx={{ fontSize: 40 }} />,
      color: 'success',
    },
    {
      title: 'Active Parcels',
      value: stats.activeParcels,
      icon: <LocationIcon color="info" sx={{ fontSize: 40 }} />,
      color: 'info',
    },
    {
      title: 'Pending Tasks',
      value: stats.pendingTasks,
      icon: <TaskIcon color="warning" sx={{ fontSize: 40 }} />,
      color: 'warning',
    },
    {
      title: 'Total Projects',
      value: stats.totalProjects,
      icon: <BusinessIcon color="secondary" sx={{ fontSize: 40 }} />,
      color: 'secondary',
    },
    {
      title: 'Active Projects',
      value: stats.activeProjects,
      icon: <TrendingUpIcon color="error" sx={{ fontSize: 40 }} />,
      color: 'error',
    },
    {
      title: 'Opportunities',
      value: stats.totalOpportunities,
      icon: <DocumentIcon color="primary" sx={{ fontSize: 40 }} />,
      color: 'primary',
    },
    {
      title: 'Proposals',
      value: stats.totalProposals,
      icon: <DocumentIcon color="success" sx={{ fontSize: 40 }} />,
      color: 'success',
    },
  ];

  return (
    <Grid container spacing={3}>
      {statCards.map((stat, index) => (
        <Grid size={{ xs: 12, sm: 6, md: 3 }} key={index}>
          <Card
            sx={{
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: 4,
              },
            }}
          >
            <CardContent sx={{ flexGrow: 1 }}>
              <Box display="flex" alignItems="center" mb={2}>
                {stat.icon}
                <Typography
                  variant="h6"
                  component="h2"
                  sx={{ ml: 1, fontWeight: 500 }}
                >
                  {stat.title}
                </Typography>
              </Box>
              <Typography
                variant="h3"
                component="div"
                color={`${stat.color}.main`}
                sx={{ fontWeight: 'bold' }}
              >
                {stat.value}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default DashboardStats;
