import React from 'react';
export default function AgentList({agents=[]}){
  return (
    <div>
      <h3>Agents</h3>
      <ul>
        {agents.map(a => <li key={a.id}>{a.name}</li>)}
      </ul>
    </div>
  );
}
