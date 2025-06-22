import React from "react";
import "./TranslateInputBox.css";
import { burstEmojis } from "../emojiBurst";

const TranslateInputBox = ({ value, onChange, onSubmit }) => {
  return (
    <div className="translate-box">
      <div className="translate-header">
        <span className="label">Emoji</span>
        <button className="submit-btn" onClick={(e) => {
            const rect = e.target.getBoundingClientRect();
            burstEmojis(rect.left + rect.width / 2, rect.top + rect.height / 2);
            onSubmit();
            }}
            >Convert</button>
        <span className="label">Text</span>
      </div>
      <div className="translate-body">
        <textarea
          className="translate-input"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Type your message..."
        />
        <div className="translate-preview">
          Result will appear in history
        </div>
      </div>
    </div>
  );
};

export default TranslateInputBox;
