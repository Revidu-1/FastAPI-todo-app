import { memo } from 'react';
import './Button.css';

/**
 * Reusable Button component demonstrating:
 * - Props (children, onClick, variant, disabled, etc.)
 * - memo() for performance optimization
 */
const Button = memo(({ 
  children, 
  onClick, 
  variant = 'primary', 
  disabled = false,
  type = 'button',
  className = '',
  ...props 
}) => {
  return (
    <button
      type={type}
      className={`btn btn-${variant} ${className}`}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
});

Button.displayName = 'Button';

export default Button;




