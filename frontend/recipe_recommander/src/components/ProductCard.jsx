import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleUp,faCircleDown } from "@fortawesome/free-solid-svg-icons";
import { hover, transform } from "motion";
const ProductCard = ({ product }) => {
  const [showAllCategories, setShowAllCategories] = useState(false);
  const [showAllIngredients, setShowAllIngredients] = useState(false);
    const [isHovered, setIsHovered] = useState(false);

  const maxItemsToShow = 3;

  // Styles for scrollable containers with limited height
  const scrollContainerStyle = {
    maxHeight: "48px", // about 3 lines, adjust as needed
    overflowY: "auto",
    margin: "4px 0",
  };

  const renderList = (items, showAll) => {
    if (!items || items.length === 0) return null;

    if (showAll || items.length <= maxItemsToShow) {
      return items.join(", ");
    } else {
      return items.slice(0, maxItemsToShow).join(", ") + ", ...";
    }
  };

  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "8px",
        padding: "10px",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
        height: "560px",
        display:"flex",
        flexDirection:"column",
        marginTop:"10px",
    transition: "transform 0.3s ease",
    transform: isHovered ? "translateZ(10px)" : "none",
      }}
            onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Image */}
      {product.image_url ? (
        <img
          src={product.image_url}
          alt={product.product_name || "Product Image"}
          style={{
            width: "100%",
            borderRadius: "6px",
            objectFit: "cover",
            height: "180px",
          }}
        />
      ) : (
        <div
          style={{
            width: "100%",
            height: "180px",
            backgroundColor: "#eee",
            borderRadius: "6px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#888",
            fontStyle: "italic",
          }}
        >
          No Image
        </div>
      )}

      {/* Product Name */}
      <h2 style={{ fontSize: "1.2rem", margin: "12px 0 8px" }}>
        {product.product_name || "Unnamed Product"}
      </h2>

      {/* Categories with scroll and toggle */}
      {product.categories && product.categories.length > 0 && (
        <div style={{ color: "#555", fontSize: "0.9rem",height:"100px"}}>
          <strong>Categories:</strong>
          <div style={showAllCategories ? {} : scrollContainerStyle}>
            {renderList(product.categories, showAllCategories)}
          </div>
          {product.categories.length > maxItemsToShow && (
            <button
              onClick={() => setShowAllCategories(!showAllCategories)}
              style={{
                background: "none",
                border: "none",
                color: "#007bff",
                cursor: "pointer",
                padding: 0,
                backgroundColor:"transparent",
                fontSize: "16px",
                transform:"translate(120px,-20px)",
              }}
              aria-label="Toggle categories list"
            >
              <FontAwesomeIcon icon={showAllCategories ? faCircleDown : faCircleUp}/>
            </button>
          )}
        </div>
      )}

      {/* Additives */}
      <p style={{ margin: "0 0", fontSize: "0.9rem" }}>
        <strong>Additives:</strong> {product.additives}
      </p>

      {/* Allergens */}
      {product.allergens && (
        <p style={{ margin: "0 0", fontSize: "0.9rem", color: "#b33" }}>
          <strong>Allergens:</strong> {product.allergens}
        </p>
      )}

      {/* Ingredients Tags with scroll and toggle */}
      {product.ingredients_tags && product.ingredients_tags.length > 0 && (
        <div style={{ margin: "0 0", fontSize: "0.9rem", color: "#555" }}>
          <strong>Ingredients Tags:</strong>
          <div style={showAllIngredients ? {} : scrollContainerStyle}>
            {renderList(product.ingredients_tags, showAllIngredients)}
          </div>
          {product.ingredients_tags.length > maxItemsToShow && (
            <button
              onClick={() => setShowAllIngredients(!showAllIngredients)}
              style={{
                marginTop: "4px",
                background: "none",
                border: "none",
                color: "#007bff",
                cursor: "pointer",
                padding: 0,
                fontSize: "16px",
                transform:"translate(120px,-40px)"
                
              }}
              aria-label="Toggle ingredients list"
            >
                <FontAwesomeIcon icon={showAllIngredients ? faCircleUp : faCircleDown}/>
            </button>
          )}
        </div>
      )}

      {/* Scores */}
      <div style={{ display: "flex", gap: "12px",marginTop:"0"}}>
        {product.ecoscore && (
          <span
            style={{
              padding: "4px 8px",
              backgroundColor: "#d4edda",
              borderRadius: "4px",
              fontWeight: "600",
              fontSize: "0.9rem",
            }}
          >
            Eco: {product.ecoscore.toUpperCase()}
          </span>
        )}
        {product.nutriscore_grade && (
          <span
            style={{
              padding: "4px 8px",
              backgroundColor: "#fff3cd",
              borderRadius: "4px",
              fontWeight: "600",
              fontSize: "0.9rem",
            }}
          >
            Nutri: {product.nutriscore_grade.toUpperCase()}
          </span>
        )}
        {product.nova_group !== undefined && product.nova_group !== null && (
          <span
            style={{
              padding: "4px 8px",
              backgroundColor: "#f8d7da",
              borderRadius: "4px",
              fontWeight: "600",
              fontSize: "0.9rem",
            }}
          >
            NOVA: {product.nova_group}
          </span>
        )}
      </div>
    </div>
  );
};

export default ProductCard;
