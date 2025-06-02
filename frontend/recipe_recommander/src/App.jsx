import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RecipeInput from './pages/RecipeInput';
import Recommendations from './pages/Recommandation';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<RecipeInput />} />
        <Route path="/recommendations" element={<Recommendations />} />
      </Routes>
    </Router>
  );
}

export default App;
