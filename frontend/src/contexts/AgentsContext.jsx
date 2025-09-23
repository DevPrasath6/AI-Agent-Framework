import React, { createContext, useState } from 'react';
export const AgentsContext = createContext();
export function AgentsProvider({children}){ const [agents,setAgents]=useState([]); return <AgentsContext.Provider value={{agents,setAgents}}>{children}</AgentsContext.Provider>; }
