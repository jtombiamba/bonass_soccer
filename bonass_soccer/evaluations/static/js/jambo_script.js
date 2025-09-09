DJANGO_STATIC_URL = `{{ STATIC_URL }}`;
let gameState = {
    deck: [],
    playerHand: [],
    playedCards: [],
    currentTurn: 'player',
    score: 0
};

const SUITS = ['hearts', 'diamonds', 'clubs', 'spades'];
const RANKS = ['7', '8', '9', '10', 'jack', 'queen', 'king', 'ace'];
const RANKS_v2 = ['3', '4', '5', '6', '7', '8', '9', '10'];
const CARD_VALUES = {
    '7': 0, '8': 0, '9': 0, '10': 10,
    'jack': 2, 'queen': 3, 'king': 4, 'ace': 11
};

function initializeDeck() {
    let deck = [];
    for (let suit of SUITS) {
        for (let rank of RANKS_v2) {
            deck.push({
                suit: suit,
                rank: rank,
                image: `/static/img/cards/card_${rank}.png`,
                //image: `{% static 'img/cards/card_' %}${rank}.png`,
                // image: `images/cards/${rank}_of_${suit}.png`,
                // value: CARD_VALUES[rank]
                value: CARD_VALUES['3']
            });
        }
    }
    return deck.sort(() => Math.random() - 0.5);
}

function dealCards() {
    gameState.deck = initializeDeck();
    gameState.playerHand = gameState.deck.splice(0, 5);
    renderHand();
}

function renderHand() {
    const handDiv = document.getElementById('playerHand');
    handDiv.innerHTML = '';

    gameState.playerHand.forEach((card, index) => {
        const cardElement = document.createElement('img');
        cardElement.className = 'card';
        cardElement.src = card.image;
        cardElement.style.left = `${index * 110}px`;
        cardElement.draggable = true;

        cardElement.addEventListener('dragstart', dragStart);
        cardElement.addEventListener('click', playCard);
        handDiv.appendChild(cardElement);
    });
}

function dragStart(e) {
    const index = [...e.target.parentElement.children].indexOf(e.target);
    e.dataTransfer.setData('text/plain', index);
}

function playCard(e) {
    const index = [...e.target.parentElement.children].indexOf(e.target);
    const card = gameState.playerHand[index];

    if (isValidPlay(card)) {
        gameState.playedCards.push(card);
        gameState.playerHand.splice(index, 1);
        gameState.score += card.value;

        updateGameState();
        saveGameState();
        renderHand();
        renderPlayedCards();
        updateScore();

        // Computer plays after short delay
        setTimeout(computerPlay, 1000);
    }
}

function isValidPlay(card) {
    console.log('game state played card = ', gameState.playedCards.length);
    if (gameState.playedCards.length === 0) return true;

    const firstSuit = gameState.playedCards[0].suit;
    const hasSuit = gameState.playerHand.some(c => c.suit === firstSuit);

    return !hasSuit || card.suit === firstSuit;
}

function computerPlay() {
    const playableCards = gameState.deck.filter(card =>
        isValidPlay(card)
    );

    if (playableCards.length > 0) {
        const randomIndex = Math.floor(Math.random() * playableCards.length);
        const playedCard = playableCards[randomIndex];

        gameState.playedCards.push(playedCard);
        gameState.deck = gameState.deck.filter(c => c !== playedCard);
        saveGameState();
        renderPlayedCards();
    }
}

function renderPlayedCards() {
    const playArea = document.getElementById('playArea');
    playArea.innerHTML = '';

    gameState.playedCards.forEach((card, index) => {
        const cardElement = document.createElement('img');
        cardElement.className = 'card';
        cardElement.src = card.image;
        cardElement.style.transform = `rotate(${index * 10}deg)`;
        playArea.appendChild(cardElement);
    });
}

function updateScore() {
    document.getElementById('score').textContent = gameState.score;
}

function saveGameState() {
    localStorage.setItem('beloteGameState', JSON.stringify(gameState));
}

function updateGameState() {
    console.log('update game state defined');
}

function loadGameState() {
    const savedState = localStorage.getItem('beloteGameState');
    if (savedState) {
        gameState = JSON.parse(savedState);
        renderHand();
        renderPlayedCards();
        updateScore();
    }
}

function newGame() {
    localStorage.removeItem('beloteGameState');
    gameState = {
        deck: [],
        playerHand: [],
        playedCards: [],
        currentTurn: 'player',
        score: 0
    };
    dealCards();
}

// Initialize game
document.addEventListener('DOMContentLoaded', () => {
    loadGameState();
    if (!gameState.playerHand.length) dealCards();

    // Add drop zone handling
    document.getElementById('playArea').addEventListener('dragover', e => {
        e.preventDefault();
    });

    document.getElementById('playArea').addEventListener('drop', e => {
        e.preventDefault();
        const index = e.dataTransfer.getData('text/plain');
        playCard({ target: document.querySelectorAll('.card')[index] });
    });
});