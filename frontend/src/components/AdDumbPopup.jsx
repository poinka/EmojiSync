import React, { useEffect, useState } from "react";
import "./AdDumbPopup.css";

const ads = [
  {
    title: "🤯 She Drank THIS Every Morning",
    text: "You won't believe how they look now!",
    image: "/adPhoto.png",
    link: "https://github.com/poinka/EmojiSync"
  },
  {
    title: "🧓 Grandpa Maxim's Secret",
    text: "Lived to 110. What was he hiding?",
    image: "/adPhoto.png",
    link: "https://github.com/poinka/EmojiSync"
  },
  {
    title: "🌴 Bali Apartment – 1100% ROI",
    text: "Only 3 left! Invest or cry.",
    image: "/adPhoto.png",
    link: "https://github.com/poinka/EmojiSync"
  }
];

const DumbPopupAd = () => {
  const [adIndex, setAdIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setAdIndex((prev) => (prev + 1) % ads.length);
    }, 8000); // Меняем рекламу каждые 8 секунд
    return () => clearInterval(interval);
  }, []);

  const ad = ads[adIndex];

  return (
    <a
      href={ad.link}
      target="_blank"
      rel="noopener noreferrer"
      className="popup-ad"
    >
      <img src={ad.image} alt={ad.title} />
      <div className="popup-text">
        <strong>{ad.title}</strong>
        <p>{ad.text}</p>
      </div>
    </a>
  );
};

export default DumbPopupAd;
