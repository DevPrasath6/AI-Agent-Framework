import { useState } from 'react';
import monitoringApi from '../api/monitoringApi';
export default function useMonitoring(){ const [logs,setLogs]=useState([]); const fetch = ()=> monitoringApi.logs().then(r=>setLogs(r.data)).catch(()=>{}); return { logs, fetch }; }
