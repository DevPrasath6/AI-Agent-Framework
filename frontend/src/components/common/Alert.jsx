import React from 'react';
import { motion } from 'framer-motion';
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XCircleIcon
} from '@heroicons/react/24/outline';

const Alert = ({
  type = 'info',
  title,
  message,
  onClose,
  className = '',
  icon: CustomIcon
}) => {
  const types = {
    success: {
      containerClass: 'bg-green-50 border-green-200 text-green-800',
      iconClass: 'text-green-400',
      icon: CheckCircleIcon
    },
    error: {
      containerClass: 'bg-red-50 border-red-200 text-red-800',
      iconClass: 'text-red-400',
      icon: XCircleIcon
    },
    warning: {
      containerClass: 'bg-yellow-50 border-yellow-200 text-yellow-800',
      iconClass: 'text-yellow-400',
      icon: ExclamationTriangleIcon
    },
    info: {
      containerClass: 'bg-blue-50 border-blue-200 text-blue-800',
      iconClass: 'text-blue-400',
      icon: InformationCircleIcon
    }
  };

  const config = types[type];
  const Icon = CustomIcon || config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: -20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      className={`rounded-lg border p-4 ${config.containerClass} ${className}`}
    >
      <div className="flex">
        <div className="flex-shrink-0">
          <Icon className={`h-5 w-5 ${config.iconClass}`} />
        </div>
        <div className="ml-3 flex-1">
          {title && (
            <h3 className="text-sm font-medium">
              {title}
            </h3>
          )}
          {message && (
            <div className={`text-sm ${title ? 'mt-1' : ''}`}>
              {message}
            </div>
          )}
        </div>
        {onClose && (
          <div className="ml-auto pl-3">
            <div className="-mx-1.5 -my-1.5">
              <button
                onClick={onClose}
                className={`inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 ${config.iconClass} hover:bg-black hover:bg-opacity-10`}
              >
                <span className="sr-only">Dismiss</span>
                <XCircleIcon className="h-5 w-5" />
              </button>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default Alert;
