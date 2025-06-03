import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import style from "./recipe.module.css";
import Wave from "react-wavify";
import { motion } from "framer-motion";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";

function RecipeInput() {
  const [recipe, setRecipe] = useState("");
  const [country, setCountry] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const text = "Welcome to recipe Recommander".split(" ");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Start loading
    try {
      const response = await fetch("http://127.0.0.1:8000/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipe: recipe, country: country }),
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();

      navigate("/recommendations", { state: { recommendations: data } });
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to fetch recommendations");
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <>
      <header className={style.header}>
        <div className={style.titleContainer}>
          <h1
            style={{
              textAlign: "center",
              padding: "30px",
              fontSize: "50px",
              color: "#eee",
            }}
          >
            {text.map((el, i) => (
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{
                  duration: 0.25,
                  delay: i / 10,
                }}
                key={i}
              >
                {el}{" "}
              </motion.span>
            ))}
          </h1>
        </div>
        <Wave
          fill="#f79902"
          paused={false}
          style={{
            display: "flex",
            transform: "rotate(180deg)", // Rotate 90 degrees clockwise
          }}
          options={{
            height: 100,
            amplitude: 100,
            speed: 0.15,
            points: 3,
          }}
        />
      </header>

      <form onSubmit={handleSubmit} className={style.form}>
        <div className={style.countryContainer}>
          <label className={style.labelA}>Select Counrty</label>
          <select
            className={style.select}
            onChange={(e) => setCountry(e.target.value)}
            value={country}
          >
            <option value="">All</option>
            {[
              "France",
              "United-Kingdom",
              "Italy",
              "United-states",
              "Germany",
              "Japan",
              "Canada",
            ].map((grade) => (
              <option key={grade} value={grade.toLowerCase()}>
                {grade}
              </option>
            ))}
          </select>
        </div>

        <textarea
          value={recipe}
          onChange={(e) => setRecipe(e.target.value)}
          placeholder="Enter your recipe here"
          rows={6}
          cols={50}
          className={style.textarea}
        />
        <br />

        <button
          type="submit"
          disabled={loading || !recipe.trim() || !country.trim()}
          style={style.button}
        >
          <FontAwesomeIcon icon={faSearch} />
        </button>

        {/* Loading indicator */}
        {loading && (
          <p style={{ color: "#f79902", marginTop: "15px", fontWeight: "bold" }}>
            Loading, please wait...
          </p>
        )}
      </form>
    </>
  );
}

export default RecipeInput;
