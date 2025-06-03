import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import ProductListWithFilters from '../components/ProductListWithFilter';
function Recommendations() {
  const navigate = useNavigate();
  const location = useLocation();
  const recommendations = location.state?.recommendations;

  useEffect(() => {
    if (!recommendations) {
      navigate('/', { replace: true });  // Redirect to root route
    }
  }, [recommendations, navigate]);

  if (!recommendations) return null;

  return (
    <ProductListWithFilters products={recommendations}/>
  );
}
export default Recommendations;