import React, { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext({
    theme: 'light',
    toggleTheme: () => {},
    isDark: false,
    isSystem: false,
    setThemeMode: () => {},
});

export const useTheme = () => {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
};

export const ThemeProvider = ({ children }) => {
    const [themeMode, setThemeMode] = useState(() => {
        // Check localStorage first, fallback to system preference
        const savedMode = localStorage.getItem('theme-mode');
        if (savedMode && ['light', 'dark', 'system'].includes(savedMode)) {
            return savedMode;
        }
        return 'system';
    });

    const [theme, setTheme] = useState('light');
    const [isSystem, setIsSystem] = useState(themeMode === 'system');

    // Get system preference
    const getSystemTheme = () => {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    // Update theme based on mode
    const updateTheme = React.useCallback((mode) => {
        let newTheme;
        if (mode === 'system') {
            newTheme = getSystemTheme();
            setIsSystem(true);
        } else {
            newTheme = mode;
            setIsSystem(false);
        }
        setTheme(newTheme);

        // Update document class and CSS variables
        const root = document.documentElement;

        if (newTheme === 'dark') {
            root.classList.add('dark');
            root.style.setProperty('--theme-transition', 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)');
        } else {
            root.classList.remove('dark');
            root.style.setProperty('--theme-transition', 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)');
        }

        // Update meta theme-color for mobile browsers
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', newTheme === 'dark' ? '#1f2937' : '#ffffff');
        }
    }, []);

    // Initialize theme on mount
    useEffect(() => {
        updateTheme(themeMode);

        // Listen for system theme changes
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        const handleSystemThemeChange = () => {
            if (themeMode === 'system') {
                updateTheme('system');
            }
        };

        mediaQuery.addEventListener('change', handleSystemThemeChange);
        return () => mediaQuery.removeEventListener('change', handleSystemThemeChange);
    }, [themeMode, updateTheme]);

    // Save theme mode to localStorage when it changes
    useEffect(() => {
        localStorage.setItem('theme-mode', themeMode);
        updateTheme(themeMode);
    }, [themeMode, updateTheme]);

    const toggleTheme = () => {
        const modes = ['light', 'dark', 'system'];
        const currentIndex = modes.indexOf(themeMode);
        const nextIndex = (currentIndex + 1) % modes.length;
        setThemeMode(modes[nextIndex]);
    };

    const setSpecificThemeMode = (mode) => {
        if (['light', 'dark', 'system'].includes(mode)) {
            setThemeMode(mode);
        }
    };

    const value = {
        theme,
        themeMode,
        toggleTheme,
        setThemeMode: setSpecificThemeMode,
        isDark: theme === 'dark',
        isSystem,
        systemTheme: getSystemTheme(),
    };

    return (
        <ThemeContext.Provider value={value}>
            {children}
        </ThemeContext.Provider>
    );
};

export default ThemeContext;
