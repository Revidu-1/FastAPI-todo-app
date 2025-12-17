import { createContext, useContext, useState, useEffect, useCallback } from 'react';

// Create AuthContext
const AuthContext = createContext(null);

// Custom hook to use AuthContext
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// AuthProvider component
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  // Check authentication status on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    if (storedToken) {
      setToken(storedToken);
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  // Login function using useCallback to memoize
  const login = useCallback((newToken) => {
    localStorage.setItem('access_token', newToken);
    setToken(newToken);
    setIsAuthenticated(true);
  }, []);

  // Logout function using useCallback
  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    setToken(null);
    setIsAuthenticated(false);
  }, []);

  const value = {
    isAuthenticated,
    loading,
    token,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

