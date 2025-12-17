import { forwardRef } from 'react';
import './Input.css';

/**
 * Reusable Input component demonstrating:
 * - Props (value, onChange, placeholder, type, etc.)
 * - forwardRef to access DOM element
 */
const Input = forwardRef(({ 
  label,
  value,
  onChange,
  placeholder,
  type = 'text',
  error,
  required = false,
  className = '',
  ...props 
}, ref) => {
  return (
    <div className={`input-group ${className}`}>
      {label && (
        <label className="input-label">
          {label}
          {required && <span className="required">*</span>}
        </label>
      )}
      <input
        ref={ref}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={`input-field ${error ? 'input-error' : ''}`}
        required={required}
        {...props}
      />
      {error && <span className="error-text">{error}</span>}
    </div>
  );
});

Input.displayName = 'Input';

export default Input;

