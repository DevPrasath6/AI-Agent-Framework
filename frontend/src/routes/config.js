// Route configuration and constants
export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  AGENTS: '/agents',
  AGENT_DETAIL: '/agents/:id',
  WORKFLOWS: '/workflows',
  WORKFLOW_DETAIL: '/workflows/:id',
  MONITORING: '/monitoring',
  SETTINGS: '/settings',
  LOGIN: '/login',
  REGISTER: '/register',
  FORGOT_PASSWORD: '/forgot-password',
  PROFILE: '/profile'
};

// Generate route paths with parameters
export const generatePath = (route, params = {}) => {
  let path = route;
  Object.keys(params).forEach(key => {
    path = path.replace(`:${key}`, params[key]);
  });
  return path;
};

// Route metadata for navigation and breadcrumbs
export const ROUTE_METADATA = {
  [ROUTES.DASHBOARD]: {
    title: 'Dashboard',
    description: 'Overview of your AI agents and workflows',
    icon: 'HomeIcon',
    breadcrumb: ['Dashboard']
  },
  [ROUTES.AGENTS]: {
    title: 'Agents',
    description: 'Manage your AI agents',
    icon: 'CpuChipIcon',
    breadcrumb: ['Dashboard', 'Agents']
  },
  [ROUTES.AGENT_DETAIL]: {
    title: 'Agent Details',
    description: 'View and edit agent configuration',
    icon: 'CpuChipIcon',
    breadcrumb: ['Dashboard', 'Agents', 'Details']
  },
  [ROUTES.WORKFLOWS]: {
    title: 'Workflows',
    description: 'Create and manage workflows',
    icon: 'Cog6ToothIcon',
    breadcrumb: ['Dashboard', 'Workflows']
  },
  [ROUTES.WORKFLOW_DETAIL]: {
    title: 'Workflow Details',
    description: 'View and edit workflow configuration',
    icon: 'Cog6ToothIcon',
    breadcrumb: ['Dashboard', 'Workflows', 'Details']
  },
  [ROUTES.MONITORING]: {
    title: 'Monitoring',
    description: 'Monitor system performance and logs',
    icon: 'ChartBarIcon',
    breadcrumb: ['Dashboard', 'Monitoring']
  },
  [ROUTES.SETTINGS]: {
    title: 'Settings',
    description: 'Configure application settings',
    icon: 'CogIcon',
    breadcrumb: ['Dashboard', 'Settings']
  }
};

// Protected routes that require authentication
export const PROTECTED_ROUTES = [
  ROUTES.DASHBOARD,
  ROUTES.AGENTS,
  ROUTES.AGENT_DETAIL,
  ROUTES.WORKFLOWS,
  ROUTES.WORKFLOW_DETAIL,
  ROUTES.MONITORING,
  ROUTES.SETTINGS,
  ROUTES.PROFILE
];

// Public routes that don't require authentication
export const PUBLIC_ROUTES = [
  ROUTES.LOGIN,
  ROUTES.REGISTER,
  ROUTES.FORGOT_PASSWORD
];

// Navigation items for sidebar
export const NAVIGATION_ITEMS = [
  {
    name: 'Dashboard',
    path: ROUTES.DASHBOARD,
    icon: 'HomeIcon',
    exact: true
  },
  {
    name: 'Agents',
    path: ROUTES.AGENTS,
    icon: 'CpuChipIcon',
    badge: null // Can be used to show count
  },
  {
    name: 'Workflows',
    path: ROUTES.WORKFLOWS,
    icon: 'Cog6ToothIcon',
    badge: null
  },
  {
    name: 'Monitoring',
    path: ROUTES.MONITORING,
    icon: 'ChartBarIcon',
    badge: null
  },
  {
    name: 'Settings',
    path: ROUTES.SETTINGS,
    icon: 'CogIcon',
    badge: null
  }
];

// Helper function to check if route is protected
export const isProtectedRoute = (pathname) => {
  return PROTECTED_ROUTES.some(route => {
    if (route.includes(':')) {
      // Handle dynamic routes
      const routePattern = route.replace(/:[^/]+/g, '[^/]+');
      const regex = new RegExp(`^${routePattern}$`);
      return regex.test(pathname);
    }
    return pathname === route;
  });
};

// Helper function to get route metadata
export const getRouteMetadata = (pathname) => {
  // First try exact match
  if (ROUTE_METADATA[pathname]) {
    return ROUTE_METADATA[pathname];
  }

  // Then try pattern matching for dynamic routes
  const matchingRoute = Object.keys(ROUTE_METADATA).find(route => {
    if (route.includes(':')) {
      const routePattern = route.replace(/:[^/]+/g, '[^/]+');
      const regex = new RegExp(`^${routePattern}$`);
      return regex.test(pathname);
    }
    return false;
  });

  return matchingRoute ? ROUTE_METADATA[matchingRoute] : null;
};
