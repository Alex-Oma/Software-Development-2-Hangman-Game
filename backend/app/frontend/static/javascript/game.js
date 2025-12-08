// game.js - extracted frontend logic for game.html
// Handles starting/resuming games, making guesses and rendering UI
document.addEventListener('DOMContentLoaded', ()=>{
  const API_BASE = '/api/games';
  const token = localStorage.getItem('access_token');
  const tokenType = localStorage.getItem('token_type') || 'Bearer';

  const newGameBtn = document.getElementById('newGameBtn');
  const resumeBtn = document.getElementById('resumeBtn');
  const loginBtn = document.getElementById('loginBtn');
  const registerBtn = document.getElementById('registerBtn');
  const saveBtn = document.getElementById('saveBtn');

  const wordBox = document.getElementById('wordBox');
  const keyboard = document.getElementById('keyboard');
  const attemptsEl = document.getElementById('attempts');
  const scoreEl = document.getElementById('score');
  const hintsEl = document.getElementById('hints');
  const gallows = document.getElementById('gallows');

  let currentGame = null; // will hold the last loaded game object

  function authHeaders(){
    const h = {'Content-Type':'application/json'};
    const t = localStorage.getItem('access_token');
    if(t) h['Authorization'] = (localStorage.getItem('token_type') || 'Bearer') + ' ' + t;
    return h;
  }

  // Check backend for an unfinished game for the logged-in user
  async function checkForUnfinished(){
    const t = localStorage.getItem('access_token');
    if(!t) return; // not logged in
    try{
      const resp = await fetch(API_BASE + '/unfinished', { headers: authHeaders() });
      if(resp.status === 204) return; // no unfinished game
      if(resp.status === 200){
        const game = await resp.json().catch(()=>null);
        if(game){
          // Ask user with a styled accessible modal
          const choice = await showResumeModal();
          // choice: 'resume' | 'new' | 'cancel'
          if(choice === 'resume'){
            localStorage.setItem('current_game_id', game.id);
            loadGame(game);
            saveBtn.style.display = 'inline-block';
          } else if(choice === 'new'){
            // start fresh (do nothing here; user may press Start New Game)
          }
        }
      }
      // for 401/403, simply ignore (user needs to login)
    } catch(err){
      console.warn('Failed to check unfinished game', err);
    }
  }

  function showResumeIfSaved(){
    const id = localStorage.getItem('current_game_id');
    if(id){
      resumeBtn.style.display = 'inline-block';
      resumeBtn.href = '#';
      resumeBtn.addEventListener('click', (e)=>{ e.preventDefault(); resumeGame(id); });
    } else {
      resumeBtn.style.display = 'none';
    }
  }

  async function startNewGame(){
    // Require authentication for starting a new game
    if(!localStorage.getItem('access_token')){
      // prompt user to sign in and redirect to login page
      if(confirm('You must be signed in to start a new game. Go to the login page now?')){
        window.location.href = '/frontend/static/login.html';
      }
      return;
    }
    const topic = document.getElementById('topic').value;
    const difficulty = document.getElementById('difficulty').value;
    newGameBtn.disabled = true; newGameBtn.textContent = 'Starting...';
    try{
      const resp = await fetch(API_BASE + '/new', {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ topic, difficulty })
      });
      if(!resp.ok){
        const err = await resp.json().catch(()=>({detail:resp.statusText}));
        alert('Failed to start game: ' + (err.detail || err.message || resp.status));
        return;
      }
      const game = await resp.json();
      localStorage.setItem('current_game_id', game.id);
      loadGame(game);
    } catch(err){
      console.error(err);
      alert('Network error starting game');
    } finally{
      newGameBtn.disabled = false; newGameBtn.textContent = 'Start New Game';
      showResumeIfSaved();
      saveBtn.style.display = 'inline-block';
    }
  }

  async function resumeGame(id){
    // try to GET the game; backend may or may not expose GET endpoint
    try{
      const resp = await fetch(API_BASE + '/' + id, {headers: authHeaders()});
      if(!resp.ok){
        // fallback: try to start a fresh game instead
        console.warn('Resume failed, starting new game instead');
        startNewGame();
        return;
      }
      const game = await resp.json();
      loadGame(game);
    } catch(err){
      console.error(err);
      alert('Failed to resume game; starting a new one instead');
      startNewGame();
    }
  }

  function renderWordSlots(revealed){
    wordBox.innerHTML = '';
    for(const ch of revealed){
      const div = document.createElement('div');
      div.className = 'letter-slot';
      if(ch === '_' || ch === ' '){
        div.classList.add('hidden');
        div.textContent = ch === ' ' ? ' ' : '_';
      } else {
        div.textContent = ch;
      }
      wordBox.appendChild(div);
    }
  }

  function renderKeyboard(guessedLetters=[]){
    keyboard.innerHTML = '';
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    alphabet.forEach(letter => {
      const btn = document.createElement('button');
      btn.className = 'key';
      btn.textContent = letter;
      if(guessedLetters.includes(letter.toLowerCase())) btn.classList.add('disabled');
      btn.addEventListener('click', ()=> onLetter(letter));
      keyboard.appendChild(btn);
    });
  }

  async function onLetter(letter){
    if(!currentGame) return;
    const gameId = currentGame.id;
    // disable button immediately
    const btns = Array.from(document.querySelectorAll('.key'));
    const btn = btns.find(b=>b.textContent === letter);
    if(btn) btn.classList.add('disabled');
    try{
      const resp = await fetch(API_BASE + '/' + gameId + '/guess', {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ letter })
      });
      if(!resp.ok){
        const err = await resp.json().catch(()=>({detail:resp.statusText}));
        alert('Guess failed: ' + (err.detail || resp.status));
        return;
      }
      const updated = await resp.json();
      localStorage.setItem('current_game_id', updated.id);
      loadGame(updated);
    } catch(err){
      console.error(err);
      alert('Network error sending guess');
    }
  }

  function updateGallows(attemptsLeft){
    // map attemptsLeft to stage 0..8 (assume initial attempts 8)
    const maxStage = 8;
    const stage = Math.max(0, Math.min(maxStage, maxStage - attemptsLeft));
    gallows.className = 'gallows stage-' + stage;
  }

  function loadGame(game){
    currentGame = game;
    // revealed might be present, or build from word length
    const revealed = game.revealed || (game.word && game.word.text ? '_'.repeat(game.word.text.length) : '_'.repeat(6));
    renderWordSlots(revealed);
    // collect guessed letters from revealed and from game.guessed if present
    let guessed = [];
    if(game.guessed) guessed = game.guessed;
    // try to infer guessed from revealed + word
    renderKeyboard(guessed);
    attemptsEl.textContent = game.attempts_left ?? '?';
    scoreEl.textContent = game.score ?? 0;
    hintsEl.textContent = game.hints ?? 0;
    updateGallows(game.attempts_left ?? 0);

    // show state
    if(game.state === 'lost'){
      alert('Game over — you lost. The word was: ' + (game.word ? game.word.text : ''));
    } else if(game.state === 'won'){
      alert('Congratulations — you won!');
    }
  }

  // wire up new/resume/save
  newGameBtn.addEventListener('click', (e)=>{ e.preventDefault(); startNewGame(); });
  saveBtn.addEventListener('click', ()=>{ // just clear from localstorage and hide
    if(currentGame) localStorage.setItem('current_game_id', currentGame.id);
    alert('Game saved. You can resume later from this device.');
  });

  // on load, show resume if present
  // First, if user is logged in, check backend for an unfinished game and prompt to resume
  checkForUnfinished().then(()=>{
    // after checking with the backend, also present any local saved resume option
    showResumeIfSaved();
  });

  // build empty keyboard until a game is loaded
  renderKeyboard([]);

  // if there is a saved id and user clicks resume, resumeGame will be called via showResumeIfSaved wiring

  // expose simple logout
  if(localStorage.getItem('access_token')){
    loginBtn.style.display = 'none';
    registerBtn.style.display = 'none';
    const out = document.createElement('button'); out.className = 'btn secondary'; out.textContent = 'Sign out';
    out.addEventListener('click', ()=>{ localStorage.removeItem('access_token'); localStorage.removeItem('current_game_id'); location.href = '/frontend/static/index.html'; });
    document.querySelector('.controls').appendChild(out);
  }

  // Modal helpers
  function showModalElement(){
    const modal = document.getElementById('resumeModal');
    modal.setAttribute('aria-hidden', 'false');
    // save previously focused element
    showModalElement._prevActive = document.activeElement;
    const resumeBtn = document.getElementById('resumeModalResume');
    resumeBtn.focus();
  }

  function hideModalElement(){
    const modal = document.getElementById('resumeModal');
    modal.setAttribute('aria-hidden', 'true');
    // restore focus
    try{ if(showModalElement._prevActive) showModalElement._prevActive.focus(); }catch(e){}
  }

  function showResumeModal(){
    return new Promise((resolve)=>{
      const modal = document.getElementById('resumeModal');
      const resumeBtn = document.getElementById('resumeModalResume');
      const newBtn = document.getElementById('resumeModalNew');
      const cancelBtn = document.getElementById('resumeModalCancel');

      // helper to find focusable elements inside modal
      function getFocusableElements(container){
        const selector = 'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';
        return Array.from(container.querySelectorAll(selector)).filter(el => el.offsetParent !== null);
      }

      function cleanup(){
        resumeBtn.removeEventListener('click', onResume);
        newBtn.removeEventListener('click', onNew);
        cancelBtn.removeEventListener('click', onCancel);
        modal.querySelector('.modal-backdrop').removeEventListener('click', onCancel);
        document.removeEventListener('keydown', trapKeydown);
      }

      function onResume(e){ e.preventDefault(); hideModalElement(); cleanup(); resolve('resume'); }
      function onNew(e){ e.preventDefault(); hideModalElement(); cleanup(); resolve('new'); }
      function onCancel(e){ e.preventDefault(); hideModalElement(); cleanup(); resolve('cancel'); }

      // Keydown handler to trap focus and handle Escape
      function trapKeydown(e){
        if(e.key === 'Escape' || e.key === 'Esc'){
          e.preventDefault(); onCancel(e);
          return;
        }
        if(e.key !== 'Tab') return;
        const focusable = getFocusableElements(modal);
        if(focusable.length === 0) return;
        const idx = focusable.indexOf(document.activeElement);
        if(e.shiftKey){
          // Shift+Tab
          if(idx === 0 || document.activeElement === modal){
            e.preventDefault(); focusable[focusable.length - 1].focus();
          }
        } else {
          // Tab
          if(idx === focusable.length - 1){
            e.preventDefault(); focusable[0].focus();
          }
        }
      }

      resumeBtn.addEventListener('click', onResume);
      newBtn.addEventListener('click', onNew);
      cancelBtn.addEventListener('click', onCancel);
      modal.querySelector('.modal-backdrop').addEventListener('click', onCancel);

      // Attach keydown trap and show modal
      document.addEventListener('keydown', trapKeydown);
      showModalElement();
    });
  }

});
