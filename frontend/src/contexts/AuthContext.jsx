import React, { createContext, useContext, useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import apiService from '../services/apiService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [showLoginAnimation, setShowLoginAnimation] = useState(false);

  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = async () => {
    setLoading(true);
    try {
      // Check if we have a stored token
      const token = localStorage.getItem('authToken');
      if (token) {
        // Verify token by fetching current user
        const userData = await apiService.getCurrentUser();
        const formattedUser = {
          id: userData.id,
          email: userData.email,
          name: `${userData.first_name} ${userData.last_name}`,
          firstName: userData.first_name,
          lastName: userData.last_name,
          avatar: userData.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
          emailVerified: userData.email_verified,
          profile: userData.profile
        };
        setUser(formattedUser);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('Error initializing auth:', error);
      // Clear invalid token
      apiService.setToken(null);
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    setLoading(true);
    setShowLoginAnimation(true);

    try {
      const response = await apiService.login({
        email: credentials.email,
        password: credentials.password
      });

      const userData = {
        id: response.user.id,
        email: response.user.email,
        name: `${response.user.first_name} ${response.user.last_name}`,
        firstName: response.user.first_name,
        lastName: response.user.last_name,
        avatar: response.user.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
        emailVerified: response.user.email_verified,
        profile: response.user.profile
      };

      setUser(userData);
      setIsAuthenticated(true);
      setLoading(false);

      // Keep animation showing for a bit longer
      setTimeout(() => {
        setShowLoginAnimation(false);
      }, 2000);

      return { success: true, user: userData };
    } catch (error) {
      setLoading(false);
      setShowLoginAnimation(false);
      // If error comes from API service, pass structured payload back
      if (error && error.payload) {
        return { success: false, errors: error.payload };
      }
      return { success: false, errors: { detail: error.message || 'Login failed' } };
    }
  };

  const logout = async () => {
    try {
      await apiService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const register = async (userData) => {
    setLoading(true);
    setShowLoginAnimation(true);

    try {
      const response = await apiService.register({
        email: userData.email,
        firstName: userData.firstName,
        lastName: userData.lastName,
        password: userData.password,
        confirmPassword: userData.confirmPassword
      });

      const newUser = {
        id: response.user.id,
        email: response.user.email,
        name: `${response.user.first_name} ${response.user.last_name}`,
        firstName: response.user.first_name,
        lastName: response.user.last_name,
        avatar: response.user.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
        emailVerified: response.user.email_verified,
        profile: response.user.profile
      };

      setUser(newUser);
      setIsAuthenticated(true);
      setLoading(false);

      setTimeout(() => {
        setShowLoginAnimation(false);
      }, 2000);

      return { success: true, user: newUser };
    } catch (error) {
      setLoading(false);
      setShowLoginAnimation(false);
      // If error comes from API service, pass structured payload back
      if (error && error.payload) {
        return { success: false, errors: error.payload };
      }
      return { success: false, errors: { detail: error.message || 'Registration failed' } };
    }
  };

  const updateProfile = async (profileData) => {
    try {
      const response = await apiService.updateProfile(profileData);
      const updatedUser = {
        ...user,
        name: `${response.first_name} ${response.last_name}`,
        firstName: response.first_name,
        lastName: response.last_name,
        avatar: response.avatar || user.avatar,
        profile: response.profile
      };
      setUser(updatedUser);
      return { success: true, user: updatedUser };
    } catch (error) {
      console.error('Profile update error:', error);
      return { success: false, error: error.message };
    }
  };

  const changePassword = async (passwordData) => {
    try {
      await apiService.changePassword(passwordData);
      return { success: true };
    } catch (error) {
      console.error('Password change error:', error);
      return { success: false, error: error.message };
    }
  };

  // Login Success Animation Component
  const LoginSuccessAnimation = () => (
    <AnimatePresence>
      {showLoginAnimation && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 bg-gradient-to-br from-purple-900 via-blue-900 to-slate-900 flex items-center justify-center"
        >
          <motion.div
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
            className="text-center"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: [0, 1.2, 1] }}
              transition={{ delay: 0.5, duration: 0.6 }}
              className="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <motion.path
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ delay: 1, duration: 0.5 }}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </motion.div>

            <motion.h2
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.8 }}
              className="text-3xl font-bold text-white mb-2"
            >
              Welcome back!
            </motion.h2>

            <motion.p
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 1 }}
              className="text-blue-200"
            >
              Redirecting to your dashboard...
            </motion.p>

            <motion.div
              initial={{ width: 0 }}
              animate={{ width: "100%" }}
              transition={{ delay: 1.2, duration: 0.8 }}
              className="h-1 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full mt-6 max-w-xs mx-auto"
            />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    register,
    updateProfile,
    changePassword,
    showLoginAnimation
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
      <LoginSuccessAnimation />
    </AuthContext.Provider>
  );
};
