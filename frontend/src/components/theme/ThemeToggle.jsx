import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from '../../contexts/ThemeContext';
import {
    SunIcon,
    MoonIcon,
    ComputerDesktopIcon,
    ChevronDownIcon,
    CheckIcon
} from '@heroicons/react/24/outline';

const ThemeToggle = ({ position = 'fixed', showLabel = true }) => {
    const { theme, themeMode, setThemeMode, isDark, isSystem } = useTheme();
    const [isOpen, setIsOpen] = useState(false);

    const themeOptions = [
        {
            id: 'light',
            name: 'Light',
            icon: SunIcon,
            description: 'Light theme',
            gradient: 'from-orange-400 to-yellow-400'
        },
        {
            id: 'dark',
            name: 'Dark',
            icon: MoonIcon,
            description: 'Dark theme',
            gradient: 'from-slate-700 to-slate-900'
        },
        {
            id: 'system',
            name: 'System',
            icon: ComputerDesktopIcon,
            description: 'Follow system preference',
            gradient: 'from-blue-500 to-purple-600'
        }
    ];

    const currentOption = themeOptions.find(option => option.id === themeMode);
    const CurrentIcon = currentOption?.icon || SunIcon;

    const positionClasses = {
        fixed: 'fixed bottom-6 right-6 z-50',
        static: 'relative',
        header: 'relative'
    };

    return (
        <div className={`${positionClasses[position]} flex items-center space-x-2`}>
            {/* Theme Toggle Button */}
            <div className="relative">
                <motion.button
                    onClick={() => setIsOpen(!isOpen)}
                    className={`
                        relative p-3 rounded-full shadow-lg transition-all duration-300
                        ${isDark
                            ? 'bg-gray-800 hover:bg-gray-700 border border-gray-700'
                            : 'bg-white hover:bg-gray-50 border border-gray-200'
                        }
                        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                        ${isDark ? 'focus:ring-offset-gray-900' : 'focus:ring-offset-white'}
                    `}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    initial={{ opacity: 0, scale: 0 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{
                        type: "spring",
                        stiffness: 200,
                        damping: 20
                    }}
                >
                    {/* Background gradient animation */}
                    <motion.div
                        className={`absolute inset-0 rounded-full bg-gradient-to-r ${currentOption?.gradient} opacity-0`}
                        animate={{ opacity: isOpen ? 0.1 : 0 }}
                        transition={{ duration: 0.2 }}
                    />

                    {/* Icon with rotation animation */}
                    <motion.div
                        animate={{ rotate: isOpen ? 180 : 0 }}
                        transition={{ duration: 0.3 }}
                        className="relative z-10"
                    >
                        <CurrentIcon className={`w-5 h-5 ${
                            isDark ? 'text-gray-200' : 'text-gray-700'
                        }`} />
                    </motion.div>

                    {/* Dropdown indicator */}
                    <motion.div
                        className="absolute -bottom-1 -right-1"
                        animate={{ rotate: isOpen ? 180 : 0 }}
                        transition={{ duration: 0.2 }}
                    >
                        <ChevronDownIcon className={`w-3 h-3 ${
                            isDark ? 'text-gray-400' : 'text-gray-500'
                        }`} />
                    </motion.div>

                    {/* Active theme indicator */}
                    {isSystem && (
                        <motion.div
                            className="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full"
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{ delay: 0.2 }}
                        />
                    )}
                </motion.button>

                {/* Dropdown Menu */}
                <AnimatePresence>
                    {isOpen && (
                        <>
                            {/* Backdrop */}
                            <motion.div
                                className="fixed inset-0 z-40"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                onClick={() => setIsOpen(false)}
                            />

                            {/* Dropdown Panel */}
                            <motion.div
                                className={`
                                    absolute bottom-full mb-2 right-0 w-56 rounded-xl shadow-2xl border
                                    ${isDark
                                        ? 'bg-gray-800 border-gray-700'
                                        : 'bg-white border-gray-200'
                                    }
                                    z-50 overflow-hidden
                                `}
                                initial={{ opacity: 0, scale: 0.95, y: 10 }}
                                animate={{ opacity: 1, scale: 1, y: 0 }}
                                exit={{ opacity: 0, scale: 0.95, y: 10 }}
                                transition={{
                                    type: "spring",
                                    stiffness: 300,
                                    damping: 30
                                }}
                            >
                                <div className="p-2 space-y-1">
                                    {themeOptions.map((option, index) => {
                                        const Icon = option.icon;
                                        const isSelected = themeMode === option.id;

                                        return (
                                            <motion.button
                                                key={option.id}
                                                onClick={() => {
                                                    setThemeMode(option.id);
                                                    setIsOpen(false);
                                                }}
                                                className={`
                                                    relative w-full p-3 rounded-lg flex items-center space-x-3
                                                    text-left transition-all duration-200 group
                                                    ${isSelected
                                                        ? isDark
                                                            ? 'bg-gray-700 text-white'
                                                            : 'bg-blue-50 text-blue-900'
                                                        : isDark
                                                            ? 'hover:bg-gray-700 text-gray-200 hover:text-white'
                                                            : 'hover:bg-gray-50 text-gray-700 hover:text-gray-900'
                                                    }
                                                `}
                                                initial={{ opacity: 0, x: -20 }}
                                                animate={{ opacity: 1, x: 0 }}
                                                transition={{ delay: index * 0.05 }}
                                                whileHover={{ x: 4 }}
                                            >
                                                {/* Background gradient for selected item */}
                                                {isSelected && (
                                                    <motion.div
                                                        className={`absolute inset-0 bg-gradient-to-r ${option.gradient} opacity-10 rounded-lg`}
                                                        initial={{ opacity: 0 }}
                                                        animate={{ opacity: 0.1 }}
                                                        transition={{ duration: 0.3 }}
                                                    />
                                                )}

                                                {/* Icon with background */}
                                                <div className={`
                                                    relative p-2 rounded-lg bg-gradient-to-r ${option.gradient}
                                                    ${isSelected ? 'opacity-100' : 'opacity-70 group-hover:opacity-100'}
                                                    transition-opacity duration-200
                                                `}>
                                                    <Icon className="w-4 h-4 text-white" />
                                                </div>

                                                {/* Text content */}
                                                <div className="flex-1 relative z-10">
                                                    <div className="font-medium">{option.name}</div>
                                                    <div className={`text-xs ${
                                                        isSelected
                                                            ? isDark ? 'text-gray-300' : 'text-blue-700'
                                                            : isDark ? 'text-gray-400' : 'text-gray-500'
                                                    }`}>
                                                        {option.description}
                                                        {option.id === 'system' && (
                                                            <span className="ml-1">
                                                                (currently {theme})
                                                            </span>
                                                        )}
                                                    </div>
                                                </div>

                                                {/* Check icon for selected item */}
                                                <AnimatePresence>
                                                    {isSelected && (
                                                        <motion.div
                                                            initial={{ opacity: 0, scale: 0 }}
                                                            animate={{ opacity: 1, scale: 1 }}
                                                            exit={{ opacity: 0, scale: 0 }}
                                                            className="relative z-10"
                                                        >
                                                            <CheckIcon className={`w-4 h-4 ${
                                                                isDark ? 'text-blue-400' : 'text-blue-600'
                                                            }`} />
                                                        </motion.div>
                                                    )}
                                                </AnimatePresence>
                                            </motion.button>
                                        );
                                    })}
                                </div>

                                {/* Footer info */}
                                <div className={`
                                    px-4 py-2 border-t text-xs
                                    ${isDark
                                        ? 'border-gray-700 text-gray-400 bg-gray-900/50'
                                        : 'border-gray-200 text-gray-500 bg-gray-50/50'
                                    }
                                `}>
                                    <div className="flex items-center justify-between">
                                        <span>Theme preferences saved</span>
                                        <motion.div
                                            className="w-2 h-2 bg-green-500 rounded-full"
                                            animate={{ opacity: [1, 0.5, 1] }}
                                            transition={{ duration: 2, repeat: Infinity }}
                                        />
                                    </div>
                                </div>
                            </motion.div>
                        </>
                    )}
                </AnimatePresence>
            </div>

            {/* Optional Label */}
            {showLabel && position !== 'fixed' && (
                <motion.span
                    className={`text-sm font-medium ${
                        isDark ? 'text-gray-300' : 'text-gray-700'
                    }`}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    {currentOption?.name}
                </motion.span>
            )}

            {/* Quick toggle for fixed position */}
            {position === 'fixed' && (
                <motion.div
                    className={`
                        absolute -top-16 left-1/2 transform -translate-x-1/2
                        px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap
                        ${isDark
                            ? 'bg-gray-800 text-gray-200 border border-gray-700'
                            : 'bg-white text-gray-700 border border-gray-200'
                        }
                        shadow-lg pointer-events-none
                    `}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                >
                    Click to change theme
                </motion.div>
            )}
        </div>
    );
};

export default ThemeToggle;
