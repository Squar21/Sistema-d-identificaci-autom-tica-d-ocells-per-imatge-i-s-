import { createRoot } from 'react-dom/client';
import App from './App';

// Selecciona l'element arrel del teu DOM
const rootElement = document.getElementById('root');

// Crea una arrel React
const root = createRoot(rootElement);

// Renderitza l'aplicació
root.render(
  // <React.StrictMode> és opcional però recomanat per a desenvolupament
  <App />
);