import React from 'react';
import { Link } from 'react-router-dom';
export default function Navbar(){
  return (
    <nav>
      <Link to='/'>Home</Link>
      <Link to='/agents'>Agents</Link>
      <Link to='/workflows'>Workflows</Link>
      <Link to='/monitoring'>Monitoring</Link>
    </nav>
  );
}
