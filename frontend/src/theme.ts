import { createTheme } from '@mui/material/styles';

// Brand palette from the provided image
// Primary: Neon Violet (#AD96DC)
// Accent: Lumen Green (#8DE971)
// Background: Iridescent Pearl (#F6F2F4)
// Secondary: Lumen Green (#8DE971)
// Tertiary accents (for infographics only): #ECF166, #74D1EA, #FF7276

export const theme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#AD96DC',
            contrastText: '#030304',
        },
        secondary: {
            main: '#8DE971',
        },
        success: {
            main: '#8DE971',
            contrastText: '#1f2937',
        },
        background: {
            default: '#F6F2F4',
            paper: '#FFFFFF',
        },
        text: {
            primary: '#1f2937',
            secondary: '#4b5563',
        },
        warning: { main: '#ECF166' },
        info: { main: '#74D1EA' },
        error: { main: '#FF7276' },
    },
    typography: {
        fontFamily: 'Inter, Roboto, Helvetica, Arial, sans-serif',
        h1: { fontWeight: 700 },
        h2: { fontWeight: 700 },
        h3: { fontWeight: 700 },
        button: { textTransform: 'none', fontWeight: 600 },
    },
    components: {
        MuiAppBar: {
            styleOverrides: {
                root: {
                    // Use primary main by default (no black)
                    backgroundColor: '#AD96DC',
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 10,
                },
                containedPrimary: {
                    backgroundColor: '#8DE971',
                    color: '#1f2937',
                    '&:hover': {
                        backgroundColor: '#7adf63',
                    },
                },
            },
        },
        MuiPaper: {
            styleOverrides: {
                root: {
                    borderRadius: 12,
                },
            },
        },
        MuiTabs: {
            styleOverrides: {
                indicator: {
                    backgroundColor: '#8DE971',
                    height: 3,
                },
            },
        },
        MuiTab: {
            styleOverrides: {
                root: {
                    '&.Mui-selected': {
                        color: '#030304',
                        backgroundColor: 'rgba(141, 233, 113, 0.15)',
                    },
                },
            },
        },
        MuiChip: {
            styleOverrides: {
                colorPrimary: {
                    backgroundColor: 'rgba(141, 233, 113, 0.2)',
                    color: '#030304',
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    borderRadius: 14,
                    boxShadow: '0 6px 24px rgba(3,3,4,0.06)'
                },
            },
        },
    },
});

export default theme;


