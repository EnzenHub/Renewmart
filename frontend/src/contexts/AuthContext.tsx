import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, UserLogin, UserCreate, AuthResponse } from '../types';
import { apiService } from '../services/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: UserLogin) => Promise<void>;
  register: (userData: UserCreate) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user && apiService.isAuthenticated();

  // Initialize auth state on app load
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        if (apiService.isAuthenticated()) {
          // Try to refresh token to get current user info
          const refreshed = await apiService.refreshToken();
          if (refreshed) {
            // Get user info from the stored token or make a request
            // For now, we'll store user info in localStorage after login
            const storedUser = localStorage.getItem('user');
            if (storedUser) {
              setUser(JSON.parse(storedUser));
            }
          } else {
            // Token refresh failed, clear auth state
            apiService.clearToken();
            localStorage.removeItem('user');
          }
        }
      } catch (error) {
        console.error('Auth initialization failed:', error);
        apiService.clearToken();
        localStorage.removeItem('user');
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (credentials: UserLogin): Promise<void> => {
    try {
      setIsLoading(true);
      const response: AuthResponse = await apiService.login(credentials);
      
      setUser(response.user);
      localStorage.setItem('user', JSON.stringify(response.user));
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData: UserCreate): Promise<void> => {
    try {
      setIsLoading(true);
      await apiService.register(userData);
      // After successful registration, automatically log in
      await login({
        username: userData.email,
        password: userData.password,
      });
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (): Promise<void> => {
    try {
      await apiService.logout();
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setUser(null);
      localStorage.removeItem('user');
    }
  };

  const refreshToken = async (): Promise<boolean> => {
    try {
      return await apiService.refreshToken();
    } catch (error) {
      console.error('Token refresh failed:', error);
      return false;
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    refreshToken,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
