import React from 'react';
import useMonitoring from '../hooks/useMonitoring';
import LogTable from '../components/monitoring/LogTable';
export default function MonitoringPage(){ const { logs, fetch } = useMonitoring(); return (<div className='card'><h2>Monitoring</h2><button onClick={fetch}>Refresh</button><LogTable logs={logs} /></div>); }
