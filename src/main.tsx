import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './App';
import { DatasetLinks, RealResearch } from './RealResearch';
import { VcapResearch } from './VcapResearch';
import './real-research.css';

const dataset = new URLSearchParams(location.search).get('dataset');
createRoot(document.getElementById('root')!).render(<StrictMode>
  <DatasetLinks />
  {dataset === 'vcap' ? <VcapResearch /> : dataset === 'nhanes' || dataset === 'hrs' ? <RealResearch dataset={dataset} /> : <App />}
</StrictMode>);
