import React, { useState } from "react";
import HistoryAccordion  from "./components/HistoryAccordion";
import AdSidebar from "./components/AdSidebar";
import AdDumbPopup from "./components/AdDumbPopup";
import TranslateInputBox from "./components/TranslateInputBox";

import "./index.css";
import mockHistory from "./mockData";

import ReactDOM from "react-dom/client";

const App = () => {
  const [input, setInput] = useState("");
const [cards, setCards] = useState(mockHistory);

  const handleSubmit = () => {
    if (input.trim()) {
      const newEntry = {
        input,
        output: `Echo: ${input}`,
      };
      setCards([newEntry, ...cards]);

      console.log("New entry to write to mockData.js:", {
        message: input,
        emoji: newEntry.output
      });

      setInput("");
    }
  };


  return (
  <div className="app-layout">
    <AdSidebar />
    {/* <AdDumbPopup /> */}

    <div className="main-content">
      <div className="input-section">
        <TranslateInputBox value={input} onChange={setInput} onSubmit={handleSubmit} />
      </div>

      <div className="history-heading">
        ↓ Your recent messages ↓
      </div>

      <div className="history-grid">
        <HistoryAccordion history={cards} />
      </div>
    </div>
  </div>
);
};

export default App;
