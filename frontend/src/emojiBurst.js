const EMOJIS = ["💜", "🔮", "✨", "🌸", "🪄", "💫", "🌺", "🦄"];

export function burstEmojis(x, y) {
  const container = document.body;

  for (let i = 0; i < 14; i++) {
    const emoji = document.createElement("div");
    emoji.className = "emoji-burst";
    emoji.innerText = EMOJIS[Math.floor(Math.random() * EMOJIS.length)];

    const spreadX = Math.random() * 160 - 80; 
    const offsetY = Math.random() * 20 - 10;   

    emoji.style.left = `${x + spreadX}px`;
    emoji.style.top = `${y - 30 + offsetY}px`; 

    container.appendChild(emoji);

    setTimeout(() => {
      container.removeChild(emoji);
    }, 2000);
  }
}

