import { useState, useCallback, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../api/client';
import { useAuth } from '../contexts/AuthContext';
import Button from './Button';
import Input from './Input';
import './Auth.css';

/**
 * Register component demonstrating:
 * - Props (none, uses context instead)
 * - useState for form state
 * - useCallback for memoized handlers
 * - useContext via useAuth hook
 * - useNavigate from react-router-dom
 */
function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  // Handle form submission
  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      setError('');

      if (password !== confirmPassword) {
        setError('Passwords do not match');
        return;
      }

      setLoading(true);

      try {
        await authAPI.register(username, password);
        // After registration, automatically log in
        const loginResponse = await authAPI.login(username, password);
        login(loginResponse.access_token);
        // Use setTimeout to ensure state updates before navigation
        setTimeout(() => {
          navigate('/', { replace: true });
        }, 50);
      } catch (err) {
        setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        setLoading(false);
      }
    },
    [username, password, confirmPassword, login, navigate]
  );

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Register</h1>
        <form onSubmit={handleSubmit}>
          <Input
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            minLength={3}
            maxLength={50}
            error={error && !password ? error : ''}
          />
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
          />
          <Input
            label="Confirm Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            minLength={6}
            error={password !== confirmPassword && confirmPassword ? 'Passwords do not match' : ''}
          />
          {error && <div className="error-message">{error}</div>}
          <Button type="submit" variant="primary" disabled={loading} className="submit-button">
            {loading ? 'Registering...' : 'Register'}
          </Button>
        </form>
        <p className="auth-link">
          Already have an account? <Link to="/login">Login here</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
