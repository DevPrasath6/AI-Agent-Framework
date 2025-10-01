import React from 'react';
import { motion } from 'framer-motion';

const Card = ({
  children,
  className = '',
  variant = 'default',
  padding = 'md',
  shadow = 'soft',
  hover = false,
  onClick,
  ...props
}) => {
  const baseClasses = "bg-white rounded-xl border border-gray-100 transition-all duration-200";

  const variants = {
    default: "bg-white",
    glass: "bg-white/80 backdrop-blur-sm",
    gradient: "bg-gradient-to-br from-white to-gray-50"
  };

  const paddings = {
    none: "p-0",
    sm: "p-4",
    md: "p-6",
    lg: "p-8",
    xl: "p-10"
  };

  const shadows = {
    none: "",
    soft: "shadow-soft",
    md: "shadow-md",
    lg: "shadow-lg",
    xl: "shadow-xl"
  };

  const hoverClasses = hover ? "hover:shadow-lg hover:-translate-y-1 cursor-pointer" : "";
  const clickableClasses = onClick ? "cursor-pointer" : "";

  const classes = `${baseClasses} ${variants[variant]} ${paddings[padding]} ${shadows[shadow]} ${hoverClasses} ${clickableClasses} ${className}`;

  const cardProps = {
    className: classes,
    onClick,
    ...props
  };

  if (hover || onClick) {
    return (
      <motion.div
        whileHover={{ y: -2, scale: 1.01 }}
        whileTap={onClick ? { scale: 0.99 } : {}}
        transition={{ type: 'spring', damping: 25, stiffness: 300 }}
        {...cardProps}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <div {...cardProps}>
      {children}
    </div>
  );
};

export default Card;
