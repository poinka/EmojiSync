import React from "react";
import "./AdSidebar.css";

const ads = [
  {
    title: "🤯 She Drank THIS Every Morning",
    text: "All celebrities did it too... You won't believe how they look now!",
    image: "/adPhoto.png",
    link: "https://example.com/miracle-drink"
  },
  {
    title: "🧓 Grandpa Maxim's Secret",
    text: "He ate this every night before sleep... and lived 110 years! (read more)",
    image: "/adPhoto.png",
    link: "https://example.com/maxim-secret"
  },
  {
    title: "🌴 1100% ROI on Bali Apartments",
    text: "Invest now, retire tomorrow. Only 3 spots left!",
    image: "/adPhoto.png",
    link: "https://example.com/bali-deal"
  },
  {
    title: "🚀 Scientists HATE Him",
    text: "He boosted his memory using one weird trick. Doctors shocked.",
    image: "/adPhoto.png",
    link: "https://example.com/memory-hack"
  },
  {
    title: "💸 She Made $9,000 in a Week",
    text: "Just by clicking on ads like this. Click to see how.",
    image: "/adPhoto.png",
    link: "https://example.com/easy-money"
  }
];


const AdSidebar = () => {
  return (
    <div className="ad-sidebar">
      {ads.map((ad, index) => (
        <a href={ad.link} target="_blank" rel="noopener noreferrer" className="ad-card" key={index}>
          <img src={ad.image} alt={ad.title} />
          <div className="ad-content">
            <h4>{ad.title}</h4>
            <p>{ad.text}</p>
          </div>
        </a>
      ))}
    </div>
  );
};

export default AdSidebar;
