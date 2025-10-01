import React from 'react';
import { motion } from 'framer-motion';

const Button = ({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  leftIcon,
  rightIcon,
  className = '',
  ...props
}) => {
  const baseClasses = "inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 whitespace-nowrap text-center";

  const variants = {
    primary: "bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 focus:ring-blue-500 shadow-lg hover:shadow-xl active:scale-[0.98]",
    secondary: "bg-blue-50 text-blue-700 border border-blue-200 hover:bg-blue-100 hover:border-blue-300 focus:ring-blue-500 active:scale-[0.98]",
    danger: "bg-gradient-to-r from-red-600 to-red-700 text-white hover:from-red-700 hover:to-red-800 focus:ring-red-500 shadow-lg hover:shadow-xl active:scale-[0.98]",
    success: "bg-gradient-to-r from-green-600 to-green-700 text-white hover:from-green-700 hover:to-green-800 focus:ring-green-500 shadow-lg hover:shadow-xl active:scale-[0.98]",
    outline: "bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 hover:border-gray-400 focus:ring-blue-500 active:scale-[0.98]",
    ghost: "bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-blue-500 active:scale-[0.98]",
    white: "bg-white text-blue-600 border-transparent hover:bg-gray-50 focus:ring-blue-500 shadow-lg hover:shadow-xl font-semibold active:scale-[0.98]"
  };

  const sizes = {
    xs: "px-2.5 py-1.5 text-xs min-h-[28px]",
    sm: "px-3 py-2 text-sm min-h-[32px]",
    md: "px-4 py-2.5 text-sm min-h-[36px]",
    lg: "px-6 py-3 text-base min-h-[44px]",
    xl: "px-8 py-4 text-lg min-h-[52px]"
  };

  const disabledClasses = disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer";
  const loadingClasses = loading ? "cursor-wait" : "";

  const classes = `${baseClasses} ${variants[variant]} ${sizes[size]} ${disabledClasses} ${loadingClasses} ${className}`;

  return (
    <motion.button
      whileHover={!disabled && !loading ? { scale: 1.02 } : {}}
      whileTap={!disabled && !loading ? { scale: 0.98 } : {}}
      className={classes}
      onClick={onClick}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      )}
      {!loading && leftIcon && <span className="mr-2 flex items-center">{leftIcon}</span>}
      <span className="flex items-center justify-center text-center w-full">
        {children}
      </span>
      {!loading && rightIcon && <span className="ml-2 flex items-center">{rightIcon}</span>}
    </motion.button>
  );
};

export default Button;
