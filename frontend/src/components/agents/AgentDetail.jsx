import React from 'react';
export default function AgentDetail({agent}){
  if(!agent) return <div>Select an agent</div>;
  return <div><h2>{agent.name}</h2><p>{agent.description}</p></div>;
}
