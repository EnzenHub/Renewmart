import React, { useEffect, useState } from 'react';
import { Box, Grid, Paper, Typography } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import apiService from '../services/api';
import { LandParcel, Task } from '../types';

const StatCard: React.FC<{ title: string; value: number; color?: string }> = ({ title, value, color = '#1976d2' }) => (
    <Paper elevation={1} sx={{ p: 3 }}>
        <Typography variant="subtitle1" color="text.secondary">
            {title}
        </Typography>
        <Typography variant="h3" sx={{ color, fontWeight: 600 }}>
            {value}
        </Typography>
    </Paper>
);

const LandownerDashboardPage: React.FC = () => {
    const { user } = useAuth();
    const [parcels, setParcels] = useState<LandParcel[]>([]);
    const [tasks, setTasks] = useState<Task[]>([]);

    useEffect(() => {
        const load = async () => {
            if (!user) return;
            const [myParcels, myTasks] = await Promise.all([
                apiService.getLandParcels(0, 1000, undefined, user.id),
                apiService.getTasks(0, 1000, undefined, user.id),
            ]);
            setParcels(myParcels);
            setTasks(myTasks);
        };
        load();
    }, [user]);

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Welcome, {user?.name} (Landowner)
            </Typography>
            <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                Your land development overview
            </Typography>

            <Grid container spacing={3} sx={{ mt: 1 }}>
                <Grid size={{ xs: 12, md: 4 }}>
                    <StatCard title="My Land Parcels" value={parcels.length} />
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                    <StatCard title="Active Parcels" value={parcels.filter(p => ['feasibility_in_progress', 'in_development'].includes(p.status)).length} color="#2e7d32" />
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                    <StatCard title="My Pending Tasks" value={tasks.filter(t => ['pending', 'assigned'].includes(t.status)).length} color="#ed6c02" />
                </Grid>
            </Grid>

            <Paper elevation={1} sx={{ p: 3, mt: 4 }}>
                <Typography variant="h6" gutterBottom>
                    Next steps
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    - Register a new land parcel, track feasibility progress, and upload required documents.
                </Typography>
            </Paper>
        </Box>
    );
};

export default LandownerDashboardPage;


