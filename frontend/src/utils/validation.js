import { VALIDATION } from './constants';

// Validation utility functions
export const validators = {
  required: (value) => {
    if (value === null || value === undefined) return 'This field is required';
    if (typeof value === 'string' && value.trim() === '') return 'This field is required';
    if (Array.isArray(value) && value.length === 0) return 'This field is required';
    return null;
  },

  email: (value) => {
    if (!value) return null;
    if (!VALIDATION.EMAIL.PATTERN.test(value)) {
      return 'Please enter a valid email address';
    }
    return null;
  },

  minLength: (min) => (value) => {
    if (!value) return null;
    if (value.length < min) {
      return `Must be at least ${min} characters long`;
    }
    return null;
  },

  maxLength: (max) => (value) => {
    if (!value) return null;
    if (value.length > max) {
      return `Must be no more than ${max} characters long`;
    }
    return null;
  },

  pattern: (regex, message = 'Invalid format') => (value) => {
    if (!value) return null;
    if (!regex.test(value)) {
      return message;
    }
    return null;
  },

  number: (value) => {
    if (!value) return null;
    if (isNaN(Number(value))) {
      return 'Must be a valid number';
    }
    return null;
  },

  integer: (value) => {
    if (!value) return null;
    if (!Number.isInteger(Number(value))) {
      return 'Must be a whole number';
    }
    return null;
  },

  min: (minimum) => (value) => {
    if (!value) return null;
    if (Number(value) < minimum) {
      return `Must be at least ${minimum}`;
    }
    return null;
  },

  max: (maximum) => (value) => {
    if (!value) return null;
    if (Number(value) > maximum) {
      return `Must be no more than ${maximum}`;
    }
    return null;
  },

  url: (value) => {
    if (!value) return null;
    try {
      new URL(value);
      return null;
    } catch {
      return 'Please enter a valid URL';
    }
  },

  json: (value) => {
    if (!value) return null;
    try {
      JSON.parse(value);
      return null;
    } catch {
      return 'Must be valid JSON';
    }
  },

  agentName: (value) => {
    const errors = [];

    if (!value) {
      errors.push('Agent name is required');
    } else {
      if (value.length < VALIDATION.AGENT_NAME.MIN_LENGTH) {
        errors.push(`Must be at least ${VALIDATION.AGENT_NAME.MIN_LENGTH} characters`);
      }
      if (value.length > VALIDATION.AGENT_NAME.MAX_LENGTH) {
        errors.push(`Must be no more than ${VALIDATION.AGENT_NAME.MAX_LENGTH} characters`);
      }
      if (!VALIDATION.AGENT_NAME.PATTERN.test(value)) {
        errors.push('Can only contain letters, numbers, hyphens, and underscores');
      }
    }

    return errors.length > 0 ? errors[0] : null;
  },

  workflowName: (value) => {
    const errors = [];

    if (!value) {
      errors.push('Workflow name is required');
    } else {
      if (value.length < VALIDATION.WORKFLOW_NAME.MIN_LENGTH) {
        errors.push(`Must be at least ${VALIDATION.WORKFLOW_NAME.MIN_LENGTH} characters`);
      }
      if (value.length > VALIDATION.WORKFLOW_NAME.MAX_LENGTH) {
        errors.push(`Must be no more than ${VALIDATION.WORKFLOW_NAME.MAX_LENGTH} characters`);
      }
      if (!VALIDATION.WORKFLOW_NAME.PATTERN.test(value)) {
        errors.push('Can only contain letters, numbers, spaces, hyphens, and underscores');
      }
    }

    return errors.length > 0 ? errors[0] : null;
  }
};

// Validate a single field with multiple validators
export function validateField(value, validatorArray = []) {
  for (const validator of validatorArray) {
    const error = validator(value);
    if (error) return error;
  }
  return null;
}

// Validate an entire form object
export function validateForm(values, schema) {
  const errors = {};

  Object.keys(schema).forEach(field => {
    const fieldValidators = schema[field];
    const fieldValue = values[field];
    const error = validateField(fieldValue, fieldValidators);

    if (error) {
      errors[field] = error;
    }
  });

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}

// Common validation schemas
export const validationSchemas = {
  agent: {
    name: [validators.required, validators.agentName],
    description: [validators.maxLength(500)],
    model: [validators.required],
    systemPrompt: [validators.required, validators.minLength(10)]
  },

  workflow: {
    name: [validators.required, validators.workflowName],
    description: [validators.maxLength(1000)],
    steps: [validators.required]
  },

  user: {
    email: [validators.required, validators.email],
    name: [validators.required, validators.minLength(2), validators.maxLength(50)],
    password: [validators.required, validators.minLength(8)]
  },

  settings: {
    apiUrl: [validators.url],
    timeout: [validators.number, validators.min(1000), validators.max(300000)],
    maxRetries: [validators.integer, validators.min(0), validators.max(10)]
  }
};
