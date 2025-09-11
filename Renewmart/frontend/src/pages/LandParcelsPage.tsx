import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  CircularProgress,
  Card,
  CardContent,
} from '@mui/material';
import Grid from '@mui/material/Grid';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  LocationOn as LocationIcon,
  Assignment as AssignmentIcon,
} from '@mui/icons-material';
import { LandParcel, ParcelStatus, User } from '../types';
import { apiService } from '../services/api';

const LandParcelsPage: React.FC = () => {
  const [parcels, setParcels] = useState<LandParcel[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [openDialog, setOpenDialog] = useState(false);
  const [editingParcel, setEditingParcel] = useState<LandParcel | null>(null);
  const [formData, setFormData] = useState<Partial<LandParcel>>({
    name: '',
    address: '',
    size_acres: 0,
    coordinates: { lat: 0, lng: 0 },
    description: '',
    landowner_id: 1,
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [parcelsData, usersData] = await Promise.all([
        apiService.getLandParcels(),
        apiService.getUsers(),
      ]);
      setParcels(parcelsData);
      setUsers(usersData);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (parcel?: LandParcel) => {
    if (parcel) {
      setEditingParcel(parcel);
      setFormData(parcel);
    } else {
      setEditingParcel(null);
      setFormData({
        name: '',
        address: '',
        size_acres: 0,
        coordinates: { lat: 0, lng: 0 },
        description: '',
        landowner_id: 1,
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingParcel(null);
    setFormData({
      name: '',
      address: '',
      size_acres: 0,
      coordinates: { lat: 0, lng: 0 },
      description: '',
      landowner_id: 1,
    });
  };

  const handleSave = async () => {
    try {
      if (editingParcel) {
        await apiService.updateLandParcel(editingParcel.id, formData);
      } else {
        await apiService.createLandParcel(formData as any);
      }
      await fetchData();
      handleCloseDialog();
    } catch (err: any) {
      setError(err.message || 'Failed to save land parcel');
    }
  };

  const handleDelete = async (parcelId: number) => {
    if (window.confirm('Are you sure you want to delete this land parcel?')) {
      try {
        await apiService.deleteLandParcel(parcelId);
        await fetchData();
      } catch (err: any) {
        setError(err.message || 'Failed to delete land parcel');
      }
    }
  };

  const handleAssignFeasibility = async (parcelId: number) => {
    // In a real app, this would open a dialog to select analyst and due date
    try {
      await apiService.assignFeasibilityStudy(parcelId, 1, new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString());
      await fetchData();
    } catch (err: any) {
      setError(err.message || 'Failed to assign feasibility study');
    }
  };

  const getStatusColor = (status: ParcelStatus) => {
    const colors: Record<ParcelStatus, 'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning'> = {
      [ParcelStatus.REGISTERED]: 'default',
      [ParcelStatus.FEASIBILITY_ASSIGNED]: 'info',
      [ParcelStatus.FEASIBILITY_IN_PROGRESS]: 'warning',
      [ParcelStatus.FEASIBILITY_COMPLETED]: 'primary',
      [ParcelStatus.FEASIBILITY_APPROVED]: 'success',
      [ParcelStatus.FEASIBILITY_REJECTED]: 'error',
      [ParcelStatus.READY_FOR_PROPOSAL]: 'info',
      [ParcelStatus.IN_PROPOSAL]: 'warning',
      [ParcelStatus.PROPOSAL_APPROVED]: 'success',
      [ParcelStatus.PROPOSAL_REJECTED]: 'error',
      [ParcelStatus.IN_DEVELOPMENT]: 'primary',
      [ParcelStatus.READY_TO_BUILD]: 'success',
    };
    return colors[status] || 'default';
  };

  const getLandownerName = (landownerId: number) => {
    const landowner = users.find(user => user.id === landownerId);
    return landowner ? landowner.name : 'Unknown';
  };

  if (loading) {
    return (
      <Container maxWidth="xl">
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Land Parcels
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Manage land parcels and their development status
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add Parcel
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <LocationIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Total Parcels</Typography>
              </Box>
              <Typography variant="h4" color="primary">
                {parcels.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <AssignmentIcon color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">Active Parcels</Typography>
              </Box>
              <Typography variant="h4" color="success.main">
                {parcels.filter(p => p.status === ParcelStatus.FEASIBILITY_IN_PROGRESS || p.status === ParcelStatus.IN_DEVELOPMENT).length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <LocationIcon color="info" sx={{ mr: 1 }} />
                <Typography variant="h6">Ready to Build</Typography>
              </Box>
              <Typography variant="h4" color="info.main">
                {parcels.filter(p => p.status === ParcelStatus.READY_TO_BUILD).length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <LocationIcon color="warning" sx={{ mr: 1 }} />
                <Typography variant="h6">Pending Review</Typography>
              </Box>
              <Typography variant="h4" color="warning.main">
                {parcels.filter(p => p.status === ParcelStatus.FEASIBILITY_COMPLETED || p.status === ParcelStatus.IN_PROPOSAL).length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper elevation={1}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Address</TableCell>
                <TableCell>Size (Acres)</TableCell>
                <TableCell>Landowner</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Feasibility</TableCell>
                <TableCell>Created</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {parcels.map((parcel) => (
                <TableRow key={parcel.id}>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <LocationIcon sx={{ mr: 1, color: 'text.secondary' }} />
                      {parcel.name}
                    </Box>
                  </TableCell>
                  <TableCell>{parcel.address}</TableCell>
                  <TableCell>{parcel.size_acres}</TableCell>
                  <TableCell>{getLandownerName(parcel.landowner_id)}</TableCell>
                  <TableCell>
                    <Chip
                      label={parcel.status.replace('_', ' ').toUpperCase()}
                      color={getStatusColor(parcel.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={parcel.feasibility_completed ? 'Completed' : 'Pending'}
                      color={parcel.feasibility_completed ? 'success' : 'warning'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(parcel.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => handleOpenDialog(parcel)}
                    >
                      <EditIcon />
                    </IconButton>
                    {parcel.status === ParcelStatus.REGISTERED && (
                      <IconButton
                        size="small"
                        onClick={() => handleAssignFeasibility(parcel.id)}
                        color="primary"
                        title="Assign Feasibility Study"
                      >
                        <AssignmentIcon />
                      </IconButton>
                    )}
                    <IconButton
                      size="small"
                      onClick={() => handleDelete(parcel.id)}
                      color="error"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingParcel ? 'Edit Land Parcel' : 'Add New Land Parcel'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                fullWidth
                label="Name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                fullWidth
                label="Size (Acres)"
                type="number"
                value={formData.size_acres}
                onChange={(e) => setFormData({ ...formData, size_acres: parseFloat(e.target.value) || 0 })}
              />
            </Grid>
            <Grid size={12}>
              <TextField
                fullWidth
                label="Address"
                value={formData.address}
                onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                fullWidth
                label="Latitude"
                type="number"
                value={formData.coordinates?.lat}
                onChange={(e) => setFormData({ 
                  ...formData, 
                  coordinates: { 
                    ...formData.coordinates!, 
                    lat: parseFloat(e.target.value) || 0 
                  } 
                })}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                fullWidth
                label="Longitude"
                type="number"
                value={formData.coordinates?.lng}
                onChange={(e) => setFormData({ 
                  ...formData, 
                  coordinates: { 
                    ...formData.coordinates!, 
                    lng: parseFloat(e.target.value) || 0 
                  } 
                })}
              />
            </Grid>
            <Grid size={12}>
              <TextField
                fullWidth
                label="Description"
                multiline
                rows={3}
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSave} variant="contained">
            {editingParcel ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default LandParcelsPage;
