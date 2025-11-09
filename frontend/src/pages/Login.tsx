/**
 * Login Page - Authentication page
 */
import { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Lock, Mail, AlertCircle, Eye, EyeOff } from 'lucide-react';

const HARDCODED_USERNAME = 'kaustubha';
const HARDCODED_PASSWORD = 'PMGod67';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 800));

    if (username === HARDCODED_USERNAME && password === HARDCODED_PASSWORD) {
      // Store auth state
      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('username', username);
      
      // Navigate to home
      navigate('/');
    } else {
      setError('Invalid username or password');
      setIsLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    // Google OAuth would go here
    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('username', 'google_user');
    navigate('/');
  };

  const handleOutlookLogin = () => {
    // Outlook OAuth would go here
    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('username', 'outlook_user');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-dark flex items-center justify-center p-6">
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-5" 
           style={{
             backgroundImage: `linear-gradient(rgba(173, 181, 189, 0.1) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(173, 181, 189, 0.1) 1px, transparent 1px)`,
             backgroundSize: '40px 40px'
           }} 
      />
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative w-full max-w-md"
      >
        {/* Card */}
        <div className="card border-2 border-dark-border p-8">
          {/* Logo/Title */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-display font-bold gradient-text mb-2">
              ProdigyPM
            </h1>
            <p className="text-gray-400">
              AI Co-Pilot for Product Managers
            </p>
          </div>

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Username/Email */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-2">
                Username or Email
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-500" />
                </div>
                <input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="input pl-10 w-full"
                  placeholder="Enter your username or email"
                  required
                  autoComplete="username"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-500" />
                </div>
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input pl-10 pr-10 w-full"
                  placeholder="Enter your password"
                  required
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-500 hover:text-gray-300" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-500 hover:text-gray-300" />
                  )}
                </button>
              </div>
            </div>

            {/* Forgot Password */}
            <div className="flex items-center justify-end">
              <button
                type="button"
                className="text-sm text-gray-400 hover:text-neon-cyan transition-colors"
              >
                Forgot username or password?
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/30 rounded-lg"
              >
                <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
                <p className="text-sm text-red-400">{error}</p>
              </motion.div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="btn btn-primary w-full text-lg py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-dark border-t-transparent rounded-full animate-spin" />
                  <span>Signing in...</span>
                </>
              ) : (
                <span>Sign In</span>
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-dark-border"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-dark-card text-gray-400">Or continue with</span>
            </div>
          </div>

          {/* Social Login Buttons */}
          <div className="space-y-3">
            <button
              type="button"
              onClick={handleGoogleLogin}
              className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-dark-border rounded-lg bg-dark-lighter hover:bg-dark-border transition-colors text-gray-300"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              <span>Sign in with Google</span>
            </button>

            <button
              type="button"
              onClick={handleOutlookLogin}
              className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-dark-border rounded-lg bg-dark-lighter hover:bg-dark-border transition-colors text-gray-300"
            >
              <svg className="w-6 h-6" viewBox="0 0 48 48" fill="none">
                {/* Main blue rounded square with O */}
                <rect x="8" y="8" width="20" height="20" rx="3" fill="#0078D4"/>
                <text x="18" y="22" fontSize="14" fontWeight="bold" fill="white" textAnchor="middle">O</text>
                
                {/* Envelope/Calendar background - darker blue bar */}
                <rect x="20" y="12" width="20" height="3" rx="0.5" fill="#003D7A"/>
                
                {/* Grid pattern (calendar) */}
                <rect x="20" y="16" width="4" height="4" rx="0.5" fill="#005A9E"/>
                <rect x="25" y="16" width="4" height="4" rx="0.5" fill="#005A9E"/>
                <rect x="30" y="16" width="4" height="4" rx="0.5" fill="#41A5EE"/>
                <rect x="35" y="16" width="4" height="4" rx="0.5" fill="#41A5EE"/>
                
                {/* Envelope body */}
                <rect x="20" y="21" width="19" height="12" rx="1" fill="#0078D4"/>
                
                {/* Envelope flap (open) - V shape */}
                <path d="M 20 21 L 29.5 27 L 39 21" stroke="#003D7A" strokeWidth="2" fill="none"/>
                <path d="M 20 21 L 29.5 26 L 39 21 L 39 23 L 29.5 28 L 20 23 Z" fill="#005A9E"/>
              </svg>
              <span>Sign in with Outlook</span>
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500">
            ProdigyPM v1.0.0
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default Login;
