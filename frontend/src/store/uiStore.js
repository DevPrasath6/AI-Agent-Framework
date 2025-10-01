import { create } from 'zustand';

export const useUIStore = create((set) => ({
  sidebarOpen: true,
  currentPage: 'Dashboard',
  theme: 'light',

  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setCurrentPage: (page) => set({ currentPage: page }),
  toggleTheme: () => set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
}));

export const useAgentStore = create((set, get) => ({
  agents: [],
  loading: false,
  error: null,

  setAgents: (agents) => set({ agents }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),

  addAgent: (agent) => set((state) => ({
    agents: [...state.agents, agent]
  })),

  updateAgent: (id, updates) => set((state) => ({
    agents: state.agents.map((agent) =>
      agent.id === id ? { ...agent, ...updates } : agent
    )
  })),

  removeAgent: (id) => set((state) => ({
    agents: state.agents.filter((agent) => agent.id !== id)
  })),
}));

export const useWorkflowStore = create((set, get) => ({
  workflows: [],
  runs: [],
  loading: false,
  error: null,

  setWorkflows: (workflows) => set({ workflows }),
  setRuns: (runs) => set({ runs }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),

  addWorkflow: (workflow) => set((state) => ({
    workflows: [...state.workflows, workflow]
  })),

  updateWorkflow: (id, updates) => set((state) => ({
    workflows: state.workflows.map((workflow) =>
      workflow.id === id ? { ...workflow, ...updates } : workflow
    )
  })),

  removeWorkflow: (id) => set((state) => ({
    workflows: state.workflows.filter((workflow) => workflow.id !== id)
  })),

  addRun: (run) => set((state) => ({
    runs: [...state.runs, run]
  })),

  updateRun: (id, updates) => set((state) => ({
    runs: state.runs.map((run) =>
      run.id === id ? { ...run, ...updates } : run
    )
  })),
}));
