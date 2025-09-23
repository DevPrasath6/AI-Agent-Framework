import React from 'react';
import { AgentsProvider } from '../contexts/AgentsContext';
import AgentList from '../components/agents/AgentList';
import useAgents from '../hooks/useAgents';
export default function AgentsPage(){
  return (
    <AgentsProvider>
      <AgentsPageInner />
    </AgentsProvider>
  );
}
function AgentsPageInner(){
  const { agents } = useAgents();
  return <div className='card'><h2>Agents</h2><AgentList agents={agents} /></div>;
}
