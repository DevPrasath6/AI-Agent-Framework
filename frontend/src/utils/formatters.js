// Import helper functions
import {
  formatDate,
  formatDuration,
  formatNumber,
  formatBytes
} from './helpers';

// Data formatting utilities specifically for display purposes

// Chart data formatters
export function formatChartData(data, xKey, yKey, label) {
  return data.map(item => ({
    [xKey]: item[xKey],
    [yKey]: item[yKey],
    label: item[label] || item[xKey]
  }));
}

export function formatTimeSeriesData(data, timeKey = 'timestamp', valueKey = 'value') {
  return data.map(item => ({
    time: new Date(item[timeKey]).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    }),
    value: Number(item[valueKey]),
    timestamp: item[timeKey]
  }));
}

// Status badge formatters
export function formatStatusBadge(status) {
  const statusConfig = {
    active: { label: 'Active', color: 'green' },
    inactive: { label: 'Inactive', color: 'gray' },
    training: { label: 'Training', color: 'blue' },
    error: { label: 'Error', color: 'red' },
    pending: { label: 'Pending', color: 'yellow' },
    running: { label: 'Running', color: 'blue' },
    completed: { label: 'Completed', color: 'green' },
    failed: { label: 'Failed', color: 'red' },
    paused: { label: 'Paused', color: 'yellow' },
    scheduled: { label: 'Scheduled', color: 'purple' }
  };

  return statusConfig[status] || { label: status, color: 'gray' };
}

// Table data formatters
export function formatTableData(data, columns) {
  return data.map(row => {
    const formattedRow = {};
    columns.forEach(column => {
      const value = row[column.key];

      if (column.formatter) {
        formattedRow[column.key] = column.formatter(value, row);
      } else if (column.type === 'date') {
        formattedRow[column.key] = formatDate(value);
      } else if (column.type === 'number') {
        formattedRow[column.key] = formatNumber(value);
      } else if (column.type === 'bytes') {
        formattedRow[column.key] = formatBytes(value);
      } else if (column.type === 'duration') {
        formattedRow[column.key] = formatDuration(value);
      } else {
        formattedRow[column.key] = value;
      }
    });
    return formattedRow;
  });
}

// API response formatters
export function formatApiResponse(response, options = {}) {
  const {
    dataKey = 'data',
    metaKey = 'meta',
    transformData = (data) => data
  } = options;

  return {
    data: transformData(response[dataKey] || response),
    meta: response[metaKey] || {},
    success: true
  };
}

export function formatPaginatedResponse(response) {
  return {
    data: response.results || response.data || [],
    pagination: {
      page: response.page || 1,
      pageSize: response.page_size || response.pageSize || 20,
      total: response.count || response.total || 0,
      totalPages: Math.ceil((response.count || response.total || 0) / (response.page_size || response.pageSize || 20))
    }
  };
}

// Form data formatters
export function formatFormData(data, schema) {
  const formatted = {};

  Object.keys(schema).forEach(key => {
    const field = schema[key];
    const value = data[key];

    if (field.type === 'number' && value !== undefined) {
      formatted[key] = Number(value);
    } else if (field.type === 'boolean' && value !== undefined) {
      formatted[key] = Boolean(value);
    } else if (field.type === 'array' && Array.isArray(value)) {
      formatted[key] = value;
    } else if (field.type === 'object' && typeof value === 'object') {
      formatted[key] = value;
    } else {
      formatted[key] = value;
    }
  });

  return formatted;
}

// Metric formatters
export function formatMetric(value, type = 'number', options = {}) {
  switch (type) {
    case 'percentage':
      return `${(value * 100).toFixed(options.decimals || 1)}%`;
    case 'currency':
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: options.currency || 'USD'
      }).format(value);
    case 'bytes':
      return formatBytes(value, options.decimals);
    case 'duration':
      return formatDuration(value);
    case 'number':
      return formatNumber(value, options.decimals);
    default:
      return value;
  }
}

// Color scale formatters for charts
export function getColorScale(values, colors = ['#ef4444', '#f97316', '#eab308', '#22c55e']) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min;

  return (value) => {
    if (range === 0) return colors[0];

    const normalized = (value - min) / range;
    const index = Math.floor(normalized * (colors.length - 1));
    return colors[Math.min(index, colors.length - 1)];
  };
}
