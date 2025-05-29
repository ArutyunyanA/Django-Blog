// Rick and Morty JS Theme - Portal Effects

document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    const links = document.querySelectorAll("a");

    links.forEach(link => {
        link.addEventListener("mouseenter", () => {
            link.style.transform = "scale(1.1)";
        });
        link.addEventListener("mouseleave", () => {
            link.style.transform = "scale(1)";
        });
    });

    // Portal click effect
    document.querySelectorAll("button, .btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const portal = document.createElement("div");
            portal.className = "portal-effect";
            portal.style.position = "fixed";
            portal.style.top = "50%";
            portal.style.left = "50%";
            portal.style.transform = "translate(-50%, -50%)";
            portal.style.width = "200px";
            portal.style.height = "200px";
            portal.style.borderRadius = "50%";
            portal.style.background = "radial-gradient(circle, #00ff90, #0b0c10)";
            portal.style.zIndex = "9999";
            portal.style.opacity = "0.8";
            portal.style.boxShadow = "0 0 60px #00ff90";
            portal.style.animation = "portalFade 1s ease-out forwards";

            body.appendChild(portal);
            setTimeout(() => portal.remove(), 1000);
        });
    });
});

// CSS animation from JS
const style = document.createElement('style');
style.innerHTML = `
@keyframes portalFade {
    0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0.9; }
    100% { transform: translate(-50%, -50%) scale(3); opacity: 0; }
}`;
document.head.appendChild(style);
document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".post-card");
    cards.forEach((card, i) => {
        card.style.opacity = 0;
        card.style.transform = "translateY(20px)";
        setTimeout(() => {
            card.style.transition = "all 0.6s ease-out";
            card.style.opacity = 1;
            card.style.transform = "translateY(0)";
        }, 100 * i);
    });
});


