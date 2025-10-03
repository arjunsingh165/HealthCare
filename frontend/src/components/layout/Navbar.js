import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { 
  UserIcon, 
  CalendarIcon, 
  ChatBubbleLeftIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  Bars3Icon,
  XMarkIcon,
  HeartIcon,
  UserGroupIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMobileMenuOpen(false);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  const getDashboardLink = () => {
    if (user?.role === 'admin') return '/admin';
    return '/dashboard';
  };

  const getProfileLink = () => {
    if (user?.role === 'doctor') return '/doctor/profile';
    return '/profile';
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white shadow-lg border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2" onClick={closeMobileMenu}>
            <HeartIcon className="h-8 w-8 text-health-primary" />
            <span className="text-xl font-bold text-health-dark">HealthCare Pro</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-600 hover:text-health-primary transition-colors">
              Home
            </Link>
            <Link to="/doctors" className="text-gray-600 hover:text-health-primary transition-colors">
              Find Doctors
            </Link>
            
            {isAuthenticated ? (
              <div className="flex items-center space-x-6">
                <Link 
                  to={getDashboardLink()} 
                  className="text-gray-600 hover:text-health-primary transition-colors flex items-center space-x-1"
                >
                  <ChartBarIcon className="h-4 w-4" />
                  <span>Dashboard</span>
                </Link>
                
                {(user?.role === 'patient' || user?.role === 'doctor') && (
                  <Link 
                    to="/appointments" 
                    className="text-gray-600 hover:text-health-primary transition-colors flex items-center space-x-1"
                  >
                    <CalendarIcon className="h-4 w-4" />
                    <span>Appointments</span>
                  </Link>
                )}

                {/* Profile Dropdown */}
                <div className="relative group">
                  <button className="flex items-center space-x-2 text-gray-600 hover:text-health-primary transition-colors">
                    <UserIcon className="h-5 w-5" />
                    <span className="font-medium">{user?.first_name || user?.email}</span>
                  </button>
                  
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300">
                    <div className="py-2">
                      <div className="px-4 py-2 border-b border-gray-100">
                        <p className="text-sm font-medium text-gray-900">{user?.full_name}</p>
                        <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
                      </div>
                      
                      <Link 
                        to={getProfileLink()} 
                        className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        <UserIcon className="h-4 w-4" />
                        <span>Profile</span>
                      </Link>
                      
                      <Link 
                        to="/settings" 
                        className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                      >
                        <Cog6ToothIcon className="h-4 w-4" />
                        <span>Settings</span>
                      </Link>
                      
                      <button 
                        onClick={handleLogout}
                        className="flex items-center space-x-2 w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                      >
                        <ArrowRightOnRectangleIcon className="h-4 w-4" />
                        <span>Logout</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link 
                  to="/login" 
                  className="text-gray-600 hover:text-health-primary transition-colors"
                >
                  Login
                </Link>
                <Link 
                  to="/register" 
                  className="health-button"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button 
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="text-gray-600 hover:text-health-primary"
            >
              {isMobileMenuOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden bg-white border-t border-gray-100">
            <div className="py-4 space-y-4">
              <Link 
                to="/" 
                className="block text-gray-600 hover:text-health-primary transition-colors"
                onClick={closeMobileMenu}
              >
                Home
              </Link>
              <Link 
                to="/doctors" 
                className="block text-gray-600 hover:text-health-primary transition-colors"
                onClick={closeMobileMenu}
              >
                Find Doctors
              </Link>
              
              {isAuthenticated ? (
                <div className="space-y-4 border-t border-gray-100 pt-4">
                  <div className="pb-2">
                    <p className="text-sm font-medium text-gray-900">{user?.full_name}</p>
                    <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
                  </div>
                  
                  <Link 
                    to={getDashboardLink()} 
                    className="block text-gray-600 hover:text-health-primary transition-colors"
                    onClick={closeMobileMenu}
                  >
                    Dashboard
                  </Link>
                  
                  {(user?.role === 'patient' || user?.role === 'doctor') && (
                    <Link 
                      to="/appointments" 
                      className="block text-gray-600 hover:text-health-primary transition-colors"
                      onClick={closeMobileMenu}
                    >
                      Appointments
                    </Link>
                  )}
                  
                  <Link 
                    to={getProfileLink()} 
                    className="block text-gray-600 hover:text-health-primary transition-colors"
                    onClick={closeMobileMenu}
                  >
                    Profile
                  </Link>
                  
                  <button 
                    onClick={handleLogout}
                    className="block text-red-600 hover:text-red-700 transition-colors w-full text-left"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <div className="space-y-4 border-t border-gray-100 pt-4">
                  <Link 
                    to="/login" 
                    className="block text-gray-600 hover:text-health-primary transition-colors"
                    onClick={closeMobileMenu}
                  >
                    Login
                  </Link>
                  <Link 
                    to="/register" 
                    className="block health-button inline-block"
                    onClick={closeMobileMenu}
                  >
                    Sign Up
                  </Link>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;