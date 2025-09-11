# RenewMart Frontend

A comprehensive React frontend application for the RenewMart land development management platform.

## 🚀 **Features**

### ✅ **Authentication System**
- **Login/Register**: Complete authentication with JWT tokens
- **Token Management**: Automatic token refresh and storage
- **Protected Routes**: Route protection based on authentication status
- **User Context**: Global authentication state management

### ✅ **Dashboard & Navigation**
- **Responsive Layout**: Material-UI based responsive design
- **Sidebar Navigation**: Easy navigation between different modules
- **Dashboard Stats**: Real-time statistics and overview
- **User Profile**: User profile management in header

### ✅ **User Management**
- **User CRUD**: Create, read, update, delete users
- **Role Management**: Support for all user types (Admin, Governance, PM, Advisor, Analyst, Investor, Landowner)
- **User Status**: Active/inactive user management
- **User Search**: Filter and search functionality

### ✅ **Land Parcel Management**
- **Parcel CRUD**: Complete land parcel management
- **Status Tracking**: Track parcel development status
- **Feasibility Studies**: Assign and track feasibility studies
- **Geographic Data**: Coordinate and location management

### ✅ **API Integration**
- **Complete API Service**: Full integration with backend APIs
- **Error Handling**: Comprehensive error handling and user feedback
- **Loading States**: Loading indicators for better UX
- **Token Refresh**: Automatic token refresh on expiration

## 🛠️ **Technology Stack**

- **React 19**: Latest React with hooks and functional components
- **TypeScript**: Full type safety throughout the application
- **Material-UI v7**: Modern UI components and theming
- **React Router v7**: Client-side routing and navigation
- **Context API**: State management for authentication
- **Fetch API**: HTTP client for API communication

## 📁 **Project Structure**

```
frontend/src/
├── components/           # Reusable UI components
│   ├── auth/            # Authentication components
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── dashboard/       # Dashboard components
│   │   └── DashboardStats.tsx
│   └── layout/          # Layout components
│       └── Layout.tsx
├── contexts/            # React contexts
│   └── AuthContext.tsx  # Authentication context
├── pages/               # Page components
│   ├── AuthPage.tsx
│   ├── DashboardPage.tsx
│   ├── UsersPage.tsx
│   └── LandParcelsPage.tsx
├── services/            # API services
│   └── api.ts          # Main API service
├── types/               # TypeScript type definitions
│   └── index.ts        # All type definitions
├── utils/               # Utility functions
├── hooks/               # Custom React hooks
└── App.tsx             # Main application component
```

## 🚀 **Getting Started**

### **Prerequisites**
- Node.js 16+ 
- npm or yarn
- Backend server running on http://localhost:8001

### **Installation**
```bash
# Install dependencies
npm install

# Start development server
npm start
```

The application will be available at http://localhost:3000

### **Available Scripts**
- `npm start`: Start development server
- `npm build`: Build for production
- `npm test`: Run tests
- `npm eject`: Eject from Create React App

## 🔐 **Authentication Flow**

1. **Login/Register**: Users can login or register new accounts
2. **Token Storage**: JWT tokens are stored in localStorage
3. **Automatic Refresh**: Tokens are automatically refreshed before expiration
4. **Protected Routes**: All main application routes require authentication
5. **Logout**: Secure logout with token cleanup

## 📱 **Responsive Design**

- **Mobile First**: Designed for mobile devices first
- **Breakpoints**: Responsive breakpoints for tablet and desktop
- **Material-UI Grid**: Responsive grid system
- **Touch Friendly**: Touch-friendly interface elements

## 🎨 **UI/UX Features**

- **Material Design**: Following Material Design principles
- **Dark/Light Theme**: Theme support (can be extended)
- **Loading States**: Loading indicators for all async operations
- **Error Handling**: User-friendly error messages
- **Form Validation**: Client-side form validation
- **Accessibility**: ARIA labels and keyboard navigation

## 🔌 **API Integration**

### **Authentication APIs**
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/refresh` - Token refresh
- `POST /auth/logout` - User logout

### **User Management APIs**
- `GET /users/` - Get all users
- `POST /users/` - Create user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### **Land Parcel APIs**
- `GET /land-parcels/` - Get all parcels
- `POST /land-parcels/` - Create parcel
- `PUT /land-parcels/{id}` - Update parcel
- `DELETE /land-parcels/{id}` - Delete parcel
- `POST /land-parcels/{id}/feasibility` - Assign feasibility study

## 🧪 **Testing**

The application includes:
- **TypeScript**: Compile-time type checking
- **ESLint**: Code quality and style checking
- **React Testing Library**: Component testing (ready to use)

## 🚀 **Production Build**

```bash
# Build for production
npm run build

# The build folder contains the production build
```

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the frontend root:
```
REACT_APP_API_BASE_URL=http://localhost:8001/api/v1
REACT_APP_APP_NAME=RenewMart
```

### **API Configuration**
The API base URL is configured in `src/services/api.ts`:
```typescript
const API_BASE_URL = 'http://localhost:8001/api/v1';
```

## 📊 **Features Implemented**

### ✅ **Completed Features**
- [x] Authentication system (login/register/logout)
- [x] Protected routing
- [x] User management (CRUD operations)
- [x] Land parcel management (CRUD operations)
- [x] Dashboard with statistics
- [x] Responsive design
- [x] API integration
- [x] Error handling
- [x] Loading states
- [x] TypeScript support

### 🚧 **Ready for Extension**
- [ ] Task management interface
- [ ] Investment opportunities interface
- [ ] Investment proposals interface
- [ ] Development projects interface
- [ ] Document management interface
- [ ] Approval workflow interface
- [ ] Notification system interface
- [ ] Settings and configuration
- [ ] Advanced search and filtering
- [ ] Data export functionality

## 🎯 **Usage**

1. **Start the application**: `npm start`
2. **Register a new account** or **login** with existing credentials
3. **Navigate** through the application using the sidebar
4. **Manage users** in the Users section
5. **Manage land parcels** in the Land Parcels section
6. **View dashboard statistics** on the main dashboard

## 🔒 **Security Features**

- **JWT Authentication**: Secure token-based authentication
- **Token Refresh**: Automatic token refresh to maintain security
- **Protected Routes**: All sensitive routes are protected
- **Input Validation**: Client-side form validation
- **XSS Protection**: React's built-in XSS protection
- **CSRF Protection**: Token-based CSRF protection

## 📈 **Performance**

- **Code Splitting**: Ready for code splitting implementation
- **Lazy Loading**: Components can be lazy loaded
- **Optimized Builds**: Production builds are optimized
- **Material-UI**: Optimized component library
- **React 19**: Latest React performance improvements

## 🎉 **Ready for Production!**

The RenewMart frontend is now **fully functional** and ready for production use with:

- ✅ **Complete authentication system**
- ✅ **User and land parcel management**
- ✅ **Responsive design**
- ✅ **API integration**
- ✅ **Error handling**
- ✅ **TypeScript support**

**The frontend is ready to work with the backend API and can be extended with additional features as needed!** 🚀