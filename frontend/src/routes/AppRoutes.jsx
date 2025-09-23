import React, { Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import Footer from '../components/layout/Footer';
import Home from '../pages/Home';
import AgentsPage from '../pages/AgentsPage';
import WorkflowsPage from '../pages/WorkflowsPage';
import MonitoringPage from '../pages/MonitoringPage';
import NotFound from '../pages/NotFound';

export default function AppRoutes(){
  return (
    <div className='app-root'>
      <Navbar />
      <main>
        <Suspense fallback={<div>Loading...</div>}>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/agents' element={<AgentsPage />} />
            <Route path='/workflows' element={<WorkflowsPage />} />
            <Route path='/monitoring' element={<MonitoringPage />} />
            <Route path='*' element={<NotFound />} />
          </Routes>
        </Suspense>
      </main>
      <Footer />
    </div>
  );
}
