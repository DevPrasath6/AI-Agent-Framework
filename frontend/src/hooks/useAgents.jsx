import { useContext, useEffect } from 'react';
import { AgentsContext } from '../contexts/AgentsContext';
import { agentsApi } from '../api';
export default function useAgents(){
  const { agents, setAgents } = useContext(AgentsContext);
  useEffect(()=>{ agentsApi.list().then(r=> setAgents(r.data)).catch(()=>{}); },[]);
  return { agents, setAgents };
}
