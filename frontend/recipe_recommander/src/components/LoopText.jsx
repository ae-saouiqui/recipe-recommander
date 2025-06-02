import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const text = "Welcome to Recipe Recommander".split(" ");

export default function LoopingText() {
  // Toggle key to reset animation
  const [animateKey, setAnimateKey] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setAnimateKey((k) => k + 1); // trigger re-render with new key
    }, 3000); // total animation length + some buffer

    return () => clearInterval(interval);
  }, []);

  return (
    <h1 key={animateKey} style={{ display: "flex", overflow: "hidden" }}>
      {text.map((el, i) => (
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{
            duration: 0.25,
            delay: i / 10,
          }}
          key={i}
          style={{ marginRight: "0.05em"}}
        >
          {el +" "}
        </motion.span>
      ))}
    </h1>
  );
}
