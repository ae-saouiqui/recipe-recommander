import React, { useState, useMemo } from "react";
import ProductCard from "./ProductCard"; // your exact card component path

const ProductListWithFilters = ({ products = [] }) => {
  const [nutriFilter, setNutriFilter] = useState("");
  const [ecoFilter, setEcoFilter] = useState("");
  const [onlyAdditives, setOnlyAdditives] = useState(false);
  const [allergensFilter, setAllergensFilter] = useState("");

  const filteredProducts = useMemo(() => {
    return products.filter((p) => {
      // NutriScore filter
      if (nutriFilter && p.nutriscore_grade?.toUpperCase() !== nutriFilter) {
        return false;
      }
      // EcoScore filter
      if (ecoFilter && p.ecoscore?.toUpperCase() !== ecoFilter) {
        return false;
      }
      // Additives filter: if onlyAdditives is true, show only additives=1
      if (onlyAdditives && p.additives !== 1) {
        return false;
      }
      // Allergens filter (case-insensitive substring match)
      if (allergensFilter) {
        const allergensStr = p.allergens?.toLowerCase() || "";
        if (allergensStr.includes(allergensFilter.toLowerCase())) {
          return false;
        }
      }
      return true;
    });
  }, [products, nutriFilter, ecoFilter, onlyAdditives, allergensFilter]);

  return (
    <div style={{ padding: 0,width:"100%",boxSizing:"border-box",margin:"0 !imporant"}}>
      {/* Filters */}
      <div style={{ display: "flex", justifyContent:"space-evenly",width:"100%", margin:"0 !important", flexWrap: "wrap", alignItems: "center",padding:"50px"}}>
        {/* NutriScore */}
        <label >
          <span style={{padding:10,background:"crimson",borderRadius:10,color:"white"}}>
            NutriScore:
            </span>
          <select value={nutriFilter} onChange={e => setNutriFilter(e.target.value)} style={{ marginLeft: 10 ,backgroundColor:"transparent",outline:"none",border:"none",fontSize:20}}>
            <option value="">All</option>
            {["A", "B", "C", "D", "E"].map((grade) => (
              <option key={grade} value={grade}>{grade}</option>
            ))}
          </select>
        </label>

        {/* EcoScore */}
        <label>
          <span style={{padding:10,background:"crimson",borderRadius:10,color:"white"}}>EcoScore:</span>
          <select value={ecoFilter} onChange={e => setEcoFilter(e.target.value)} style={{ marginLeft: 10 ,backgroundColor:"transparent",outline:"none",border:"none",fontSize:20}}>
            <option value="">All</option>
            {["A", "B", "C", "D", "E"].map((grade) => (
              <option key={grade} value={grade}>{grade}</option>
            ))}
          </select>
        </label>

        {/* Additives */}
        <label style={{ display: "flex", alignItems: "center", gap: 4, cursor: "pointer" }}>
          <input
            type="checkbox"
            checked={onlyAdditives}
            onChange={e => setOnlyAdditives(e.target.checked)}
          />
          Only products with additives
        </label>

        {/* Allergens */}
        <label>
          Allergens:
          <input
            type="text"
            placeholder="Search allergens"
            value={allergensFilter}
            onChange={e => setAllergensFilter(e.target.value)}
            style={{ marginLeft: 6,padding:20,borderRadius:40,boxShadow: "0 2px 8px rgba(0,0,0,0.1)",outline:"none",border:"none"}}
          />
        </label>
      </div>

      {/* Products Grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "24px",
          perspectiveOrigin: "center center",
          perspective: "1000px",
          width: "100%",
          height: "100vh",
          overflowY: "scroll",
          justifyContent: "space-between",
          padding: "0 100px",
        }}
      >
        {filteredProducts.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};

export default ProductListWithFilters;
