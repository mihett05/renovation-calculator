import '@mantine/core/styles.css';
import { MantineProvider } from '@mantine/core';
import { Provider } from 'react-redux';
import { BrowserRouter, Route, Routes } from 'react-router';
import { store } from '~/shared/store/store';
import CalculatorPage from '../pages/calculator';
import CatalogPage from '../pages/catalog';

function App() {
  return (
    <Provider store={store}>
      <MantineProvider>
        <BrowserRouter>
          <Routes>
            <Route index element={<CalculatorPage />} />
            <Route path="catalog" element={<CatalogPage />} />
          </Routes>
        </BrowserRouter>
      </MantineProvider>
    </Provider>
  );
}

export default App;
