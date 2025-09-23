import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';
export default function MetricsChart({data=[]}){
  const canvasRef = useRef();
  useEffect(()=>{ if(!canvasRef.current) return; const ctx = canvasRef.current.getContext('2d'); new Chart(ctx,{type:'line',data:{labels:data.map((d,i)=>i),datasets:[{label:'metric',data:data}]}}); },[data]);
  return <canvas ref={canvasRef} />;
}
