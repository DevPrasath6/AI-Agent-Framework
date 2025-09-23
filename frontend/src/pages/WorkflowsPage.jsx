import React from 'react';
import useWorkflows from '../hooks/useWorkflows';
import WorkflowList from '../components/workflows/WorkflowList';
export default function WorkflowsPage(){ const { workflows } = useWorkflows(); return <div className='card'><h2>Workflows</h2><WorkflowList workflows={workflows} /></div>; }
