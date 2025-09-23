import React from 'react';
export default function WorkflowList({workflows=[]}){
  return (<div><h3>Workflows</h3><ul>{workflows.map(w=> <li key={w.id}>{w.name}</li>)}</ul></div>);
}
