import React from 'react';
export default function LogTable({logs=[]}){ return (<div><h3>Logs</h3><pre>{JSON.stringify(logs,null,2)}</pre></div>); }
