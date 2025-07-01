import React, { useState } from "react";
import "./TranslateInputBox.css";
import { burstEmojis } from "../emojiBurst";

const TranslateInputBox = ({ value, onChange }) => {
  const [result, setResult] = useState(""); 

  const handleSubmit = async () => {
    try {
      const res = await fetch("http://localhost:8000/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: value })
      });
      const data = await res.json();
      setResult(data); 
    } catch (e) {
      setResult({author: "Error", transformed: e.message});
    }
  };

  return (
    <div className="translate-box">
      <div className="translate-header">
        <span className="label">Emoji</span>
        <button
          className="submit-btn"
          onClick={e => {
            const rect = e.target.getBoundingClientRect();
            burstEmojis(rect.left + rect.width / 2, rect.top + rect.height / 2);
            handleSubmit();
          }}
        >
          Convert
        </button>
        <span className="label">Text</span>
      </div>
      <div className="translate-body">
        <textarea
          className="translate-input"
          value={value}
          onChange={e => onChange(e.target.value)}
          placeholder="Type your message..."
        />
        <div className="translate-preview">
          {result ? (
            <div>
              <span className="translate-result">{result.author}</span>: {result.transformed}
            </div>
          ) : (
            <div className="translate-hint">
              Press Convert to transform your text.
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default TranslateInputBox;
