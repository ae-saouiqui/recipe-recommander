import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import style from './recipe.module.css'
import Wave from 'react-wavify';
import {motion} from 'framer-motion'
function RecipeInput() {
  const [recipe, setRecipe] = useState('');
  const navigate = useNavigate();
    const text = "Welcome to recipe Recommander".split(" ");

  const handleSubmit= async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:8000/recommnadations/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recipe }),
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();

      // Redirect with state carrying the recommendation data
      navigate('/recommendations', { state: { recommendations: data.recommendations } });
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to fetch recommendations');
    }
  };

  return (

    <>
    <header className={style.header}>
        <h1 style={{textAlign:'center',padding:'30px',fontSize:'50px',color:'#eee',backgroundColor:'#f79902'}}>
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
  <Wave
    fill='#f79902'
    paused={false}
    style={{
      display: 'flex',
      transform: 'rotate(180deg)'  // Rotate 90 degrees clockwise
    }}
    options={{
      height: 20,
      amplitude: 20,
      speed: 0.15,
      points: 3
    }}
  />
        
    </header>
    <form onSubmit={handleSubmit} className={style.form}>
      <textarea
        value={recipe}
        onChange={(e) => setRecipe(e.target.value)}
        placeholder="Enter your recipe here"
        rows={6}
        cols={50}
        className={style.textarea}
        />
      <br />
      <button type="submit" disabled={!recipe.trim()} style={style.button}>Get Recommendations</button>
    </form>
        </>
  );
}

export default RecipeInput;
