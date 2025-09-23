import { useState, useEffect } from 'react';
import workflowsApi from '../api/workflowsApi';
export default function useWorkflows(){
  const [workflows, setWorkflows] = useState([]);
  useEffect(()=>{ workflowsApi.list().then(r=> setWorkflows(r.data)).catch(()=>{}); },[]);
  return { workflows, setWorkflows };
}
