import '@mantine/core/styles.css';

import { MantineProvider } from '@mantine/core';
import { BrowserRouter, Routes, Route } from 'react-router';
import CalculatorPage from '../pages/calculator';
import CatalogPage from '../pages/catalog';

function App() {
  return (
    <MantineProvider>
      <BrowserRouter>
        <Routes>
          <Route index element={<CalculatorPage />} />
          <Route path="catalog" element={<CatalogPage />} />
        </Routes>
      </BrowserRouter>
    </MantineProvider>
  );
}

export default App;
