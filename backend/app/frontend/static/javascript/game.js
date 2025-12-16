// game.js - frontend logic for game.html
// Handles starting/resuming games, making guesses and rendering UI
document.addEventListener('DOMContentLoaded', ()=>{
// API base URL
  const API_BASE = '/api/games';
  const token = localStorage.getItem('access_token');
  const tokenType = localStorage.getItem('token_type') || 'Bearer';

// UI elements
  const newGameBtn = document.getElementById('newGameBtn');
  const wordBox = document.getElementById('wordBox');
  const keyboard = document.getElementById('keyboard');
  const attemptsEl = document.getElementById('attempts');
  const scoreEl = document.getElementById('score');
  const hintsEl = document.getElementById('hints');
  const gallows = document.getElementById('gallows');

  let currentGame = null; // will hold the last loaded game object

// Helper to get auth headers
  function authHeaders(){
    const h = {'Content-Type':'application/json'};
    const t = localStorage.getItem('access_token');
    // add Authorization header if token present
    if(t) h['Authorization'] = (localStorage.getItem('token_type') || 'Bearer') + ' ' + t;
    return h;
  }

  // Check backend for an unfinished game for the logged-in user
  async function checkForUnfinished(){
  // only check if logged in
    const t = localStorage.getItem('access_token');
    if(!t) return; // not logged in
    try{
    // fetch unfinished game
      const resp = await fetch(API_BASE + '/unfinished', { headers: authHeaders() });
      // handle response
      if(resp.status === 204) return; // no unfinished game
      // if 200, parse game and prompt user
      if(resp.status === 200){
      // parse game
        const game = await resp.json().catch(()=>null);
        if(game){
          // Ask user with a styled accessible modal
          const choice = await showResumeModal();
          // choice: 'resume' | 'cancel'
          if(choice === 'resume'){
          // load the game
            localStorage.setItem('current_game_id', game.id);
            loadGame(game);
          } else if(choice === 'new'){
            // start fresh (do nothing here; user may press Start New Game)
          }
        }
      }
      // for 401/403, simply ignore (user needs to login)
    } catch(err){
    // log error but do not block user
      console.warn('Failed to check unfinished game', err);
    }
  }

// Start a new game
  async function startNewGame(difficulty = 'easy'){
    // Require authentication for starting a new game
    if(!localStorage.getItem('access_token')){
      // prompt user to sign in and redirect to login page
      if(confirm('You must be signed in to start a new game. Go to the login page now?')){
        window.location.href = '/frontend/static/login.html';
      }
      return;
    }

    // disable button to prevent multiple clicks
    newGameBtn.disabled = true; newGameBtn.textContent = 'Starting...';
    try{
    // POST to create new game
      const resp = await fetch(API_BASE + '/new', {
        method: 'POST',
        headers: authHeaders(),
        // We only send difficulty level to backend
        body: JSON.stringify({ difficulty })
      });
      // handle response
      if(!resp.ok){
      // show error
        const err = await resp.json().catch(()=>({detail:resp.statusText}));
        alert('Failed to start game: ' + (err.detail || err.message || resp.status));
        return;
      }
      // parse game
      const game = await resp.json();
      // save current game id
      localStorage.setItem('current_game_id', game.id);
      // load game into UI
      loadGame(game);
    } catch(err){
    // network error
      console.error(err);
      alert('Network error starting game');
    } finally{
    // re-enable button
      newGameBtn.disabled = false; newGameBtn.textContent = 'Start New Game';
    }
  }

    // Resume a game by ID
  async function resumeGame(id){
    // try to GET the game
    try{
    // Require authentication for resuming a game
      const resp = await fetch(API_BASE + '/' + id, {headers: authHeaders()});
      // handle response
      if(!resp.ok){
        // fallback: try to start a fresh game instead
        console.warn('Resume failed, starting new game instead');
        // Start new game
        startNewGame();
        return;
      }
      // parse game
      const game = await resp.json();
      // load game into UI
      loadGame(game);
    } catch(err){
    // network error
      console.error(err);
      alert('Failed to resume game; starting a new one instead');
      // Start new game
      startNewGame();
    }
  }

// Render word slots
  function renderWordSlots(revealed){
    wordBox.innerHTML = '';
    // revealed is a string with letters and underscores
    for(const ch of revealed){
    // create a div for each letter/underscore
      const div = document.createElement('div');
      div.className = 'letter-slot';
      // hide underscores and spaces
      if(ch === '_' || ch === ' '){
        div.classList.add('hidden');
        div.textContent = ch === ' ' ? ' ' : '_';
      } else {
        div.textContent = ch;
      }
      // append to word box
      wordBox.appendChild(div);
    }
  }

// Render keyboard
  function renderKeyboard(guessedLetters=[]){
    keyboard.innerHTML = '';
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    // create buttons
    alphabet.forEach(letter => {
    // create button
      const btn = document.createElement('button');
      btn.className = 'key';
      btn.textContent = letter;
      // disable button if already guessed (use both attribute and class for accessibility)
      if((guessedLetters || []).includes(letter.toLowerCase())){
        btn.classList.add('disabled');
        btn.disabled = true;
        btn.setAttribute('aria-pressed', 'true');
      } else {
        btn.disabled = false;
        btn.setAttribute('aria-pressed', 'false');
      }
      // add click handler
      btn.addEventListener('click', ()=> onLetter(letter));
      // append to keyboard
      keyboard.appendChild(btn);
    });
  }

// Handle letter guess
  async function onLetter(letter){
    if(!currentGame) return;
    const gameId = currentGame.id;
    // disable button immediately
    const btns = Array.from(document.querySelectorAll('.key'));
    // find the button for this letter
    const btn = btns.find(b=>b.textContent === letter);
    if(btn) btn.classList.add('disabled');
    try{
    // POST guess to backend
      const resp = await fetch(API_BASE + '/' + gameId + '/guess', {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ letter })
      });
      // handle response
      if(!resp.ok){
        const err = await resp.json().catch(()=>({detail:resp.statusText}));
        showMessage('Guess failed: ' + (err.detail || resp.status));
        return;
      }
      // parse updated game
      const updated = await resp.json();
      // save current game id
      localStorage.setItem('current_game_id', updated.id);
      // load updated game into UI
      loadGame(updated);
    } catch(err){
    // network error
      console.error(err);
      alert('Network error sending guess');
    }
  }

// Update gallows display based on attempts left
  function updateGallows(attemptsLeft, initialAttempts = 6) {
    // Dynamically map wrong guesses to the available gallows stages (0-9).
    const MAX_STAGE = 9;
    // Calculate number of wrong guesses
    const wrongGuesses = Math.max(0, initialAttempts - attemptsLeft);

    // If there are no attempts, show the full gallows.
    if (initialAttempts === 0) {
        // avoid division by zero
        gallows.className = 'gallows stage-' + MAX_STAGE;
        return;
    }

    // Scale the number of wrong guesses to the available stages.
    // This ensures that the final wrong guess always shows the full hangman.
    const stage = Math.min(MAX_STAGE, Math.round((wrongGuesses / initialAttempts) * MAX_STAGE));
    // Update gallows class
    gallows.className = 'gallows stage-' + stage;
  }

// Load game into UI
  function loadGame(game){
    currentGame = game;
    // revealed should be provided by the backend; if not, fallback to a safe default
    const revealed = game.revealed || '_'.repeat(6);
    // render word slots
    renderWordSlots(revealed);
    // collect guessed letters from revealed and from game.guessed if present
    let guessed = [];
    // Check game.guessed first
    if(game.guessed) guessed = (typeof game.guessed === 'string' ? game.guessed.split('') : game.guessed);
    // try to infer guessed from revealed + word
    renderKeyboard(guessed);
    // update attempts, score, hints
    attemptsEl.textContent = game.attempts_left ?? game.initial_attempts ?? '?';
    scoreEl.textContent = game.score ?? 0;
    hintsEl.textContent = game.hints_used ?? 0;
    // update gallows
    updateGallows(game.attempts_left ?? 0, game.initial_attempts ?? 6);

    // populate word metadata (clue and topic) if present
    const wordMetaEl = document.getElementById('wordMeta');
    const wordClueEl = document.getElementById('wordClue');
    const wordTopicEl = document.getElementById('wordTopic');
    // only show if word data present
    if(game.word){
      if(wordClueEl) wordClueEl.textContent = 'Clue: ' + (game.word.clue || '—');
      if(wordTopicEl) wordTopicEl.textContent = 'Topic: ' + (game.word.topic || '—');
      if(wordMetaEl) wordMetaEl.style.display = 'block';
    } else {
    // hide metadata section
      if(wordMetaEl) wordMetaEl.style.display = 'none';
    }

    // show state
    if(game.state === 'lost'){
      // do NOT reveal the word text in the UI or in the console to avoid cheating
      let msg = 'Game over — you lost.';
      // add clue/topic if present
      if(game.word && (game.word.clue || game.word.topic)){
        const parts = [];
        // add clue/topic
        if(game.word.clue) parts.push(game.word.clue);
        // add topic
        if(game.word.topic) parts.push('topic: ' + game.word.topic);
        msg += ' Hint: ' + parts.join(' | ');
      }
      // show message Game over message
      showMessage(msg, 'Game Over');
    } else if(game.state === 'won'){
    // show winning message
      showMessage('Congratulations — you won!', 'You Won!');
    }
  }

  // wire up new/resume/save
  newGameBtn.addEventListener('click', (e)=>{ e.preventDefault(); showNewGameModal(); });

// Hint button handler
  const hintBtn = document.getElementById('hintBtn');
  // provide hint for current game
  if (hintBtn) {
  // add click listener
    hintBtn.addEventListener('click', async () => {
    // validate current game
      if (!currentGame) {
        showMessage('You must start a game to use a hint.');
        return;
      }
      // only allow hints in active games
      if (currentGame.state !== 'active') {
        showMessage('You can only use hints in an active game.');
        return;
      }
        // send POST to get hint
      try {
        const resp = await fetch(`${API_BASE}/${currentGame.id}/hint`, {
          method: 'POST',
          headers: authHeaders(),
        });
        // handle response
        if (!resp.ok) {
          const err = await resp.json().catch(() => ({ detail: resp.statusText }));
          showMessage('Hint failed: ' + (err.detail || resp.status));
          return;
        }

        // parse updated game
        const updatedGame = await resp.json();
        // Load updated game into UI
        loadGame(updatedGame);
      } catch (err) {
      // network error
        console.error(err);
        showMessage('Network error using hint.');
      }
    });
  }

  // on load, show resume if present
  // First, if user is logged in, check backend for an unfinished game and prompt to resume
  checkForUnfinished()
  // build empty keyboard until a game is loaded
  renderKeyboard([]);

  // expose simple logout
  if(localStorage.getItem('access_token')){
  // add sign out button
    const out = document.createElement('button'); out.className = 'btn secondary'; out.textContent = 'Sign out';
    // sign out handler
    out.addEventListener('click', ()=>{ localStorage.removeItem('access_token'); localStorage.removeItem('current_game_id'); location.href = '/frontend/static/index.html'; });
    // append to controls
    document.querySelector('.controls').appendChild(out);
  }

  // Modal helpers
  function showModalElement(){
  // show the resume modal
    const modal = document.getElementById('resumeModal');
    modal.setAttribute('aria-hidden', 'false');
    // save previously focused element
    showModalElement._prevActive = document.activeElement;
    // focus resume button
    const resumeBtn = document.getElementById('resumeModalResume');
    // focus it
    resumeBtn.focus();
  }

// hide the resume modal
  function hideModalElement(){
  // hide the resume modal
    const modal = document.getElementById('resumeModal');
    modal.setAttribute('aria-hidden', 'true');
    // restore focus
    try{ if(showModalElement._prevActive) showModalElement._prevActive.focus(); }catch(e){}
  }

// Show resume modal and return promise resolving to user choice
  function showResumeModal(){
    // returns Promise resolving to 'resume' or 'cancel'
    return new Promise((resolve)=>{
        // get modal elements
      const modal = document.getElementById('resumeModal');
      const resumeBtn = document.getElementById('resumeModalResume');
      const cancelBtn = document.getElementById('resumeModalCancel');

      // helper to find focusable elements inside modal
      function getFocusableElements(container){
        const selector = 'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';
        // filter out elements that are not visible
        return Array.from(container.querySelectorAll(selector)).filter(el => el.offsetParent !== null);
      }

        // Cleanup event listeners
      function cleanup(){
        // remove all event listeners
        resumeBtn.removeEventListener('click', onResume);
        cancelBtn.removeEventListener('click', onCancel);
        modal.querySelector('.modal-backdrop').removeEventListener('click', onCancel);
        // remove keydown listener
        document.removeEventListener('keydown', trapKeydown);
      }

        // Event handlers for buttons Resume game and Cancel game
      function onResume(e){ e.preventDefault(); hideModalElement(); cleanup(); resolve('resume'); }
      function onCancel(e){ e.preventDefault(); hideModalElement(); cleanup(); resolve('cancel'); }

      // Keydown handler to trap focus and handle Escape
      function trapKeydown(e){
        // handle Escape key to cancel
        if(e.key === 'Escape' || e.key === 'Esc'){
          e.preventDefault(); onCancel(e);
          return;
        }
        // handle Tab key to trap focus within modal
        if(e.key !== 'Tab') return;
        // get focusable elements
        const focusable = getFocusableElements(modal);
        // no focusable elements
        if(focusable.length === 0) return;
        // find currently focused element index
        const idx = focusable.indexOf(document.activeElement);
        // if not found, do nothing
        if(e.shiftKey){
          // Shift+Tab
          if(idx === 0 || document.activeElement === modal){
            // focus last element
            e.preventDefault(); focusable[focusable.length - 1].focus();
          }
        } else {
          // Tab
          if(idx === focusable.length - 1){
            // focus first element
            e.preventDefault(); focusable[0].focus();
          }
        }
      }

        // Attach event listeners
      resumeBtn.addEventListener('click', onResume);
      cancelBtn.addEventListener('click', onCancel);
      modal.querySelector('.modal-backdrop').addEventListener('click', onCancel);

      // Attach keydown trap and show modal
      document.addEventListener('keydown', trapKeydown);
      showModalElement();
    });
  }

    // Show new game modal with difficulty selection
  function showNewGameModal() {
    // if there is a current unfinished game, confirm with user
    if (currentGame && currentGame.state !== 'won' && currentGame.state !== 'lost') {
        // show confirmation modal
      const confirmModal = document.getElementById('confirmNewGameModal');
      confirmModal.setAttribute('aria-hidden', 'false');

        // get buttons
      const yesBtn = document.getElementById('confirmNewGameYes');
      const noBtn = document.getElementById('confirmNewGameNo');

        // cleanup function
      function cleanup() {
        yesBtn.removeEventListener('click', onYes);
        noBtn.removeEventListener('click', onNo);
        confirmModal.querySelector('.modal-backdrop').removeEventListener('click', onNo);
      }

        // event handler for Yes button
      function onYes() {
        cleanup();
        confirmModal.setAttribute('aria-hidden', 'true');
        // show difficulty modal
        _showDifficultyModal();
      }

        // event handler for No button
      function onNo() {
        cleanup();
        // hide confirmation modal
        confirmModal.setAttribute('aria-hidden', 'true');
      }

    // attach event listeners
      yesBtn.addEventListener('click', onYes);
      noBtn.addEventListener('click', onNo);
      confirmModal.querySelector('.modal-backdrop').addEventListener('click', onNo);

    } else {
    // no unfinished game, show difficulty modal directly
      _showDifficultyModal();
    }
  }

// Internal function to show difficulty selection modal
  function _showDifficultyModal() {
    // show the new game modal
    const modal = document.getElementById('newGameModal');
    modal.setAttribute('aria-hidden', 'false');

    // get buttons by their IDs
    const difficultyButtons = document.getElementById('newGameDifficultyButtons');
    const cancelBtn = document.getElementById('newGameCancel');

    // cleanup function to remove event listeners
    function cleanup() {
        // remove all event listeners
      difficultyButtons.removeEventListener('click', onDifficultySelect);
      cancelBtn.removeEventListener('click', onCancel);
      modal.querySelector('.modal-backdrop').removeEventListener('click', onCancel);
    }

    // event handler for difficulty selection
    function onDifficultySelect(e) {
      if (e.target.tagName === 'BUTTON' && e.target.dataset.difficulty) {
        const difficulty = e.target.dataset.difficulty;
        // hide modal dialog first
        hideModal();
        // start new game with selected difficulty
        startNewGame(difficulty);
      }
    }

    // event handler for cancel button
    function onCancel(e) {
        // prevent default action
      e.preventDefault();
      // Hide modal
      hideModal();
    }

    // function to hide modal and cleanup
    function hideModal() {
        // cleanup and hide modal
      cleanup();
      modal.setAttribute('aria-hidden', 'true');
    }

    // attach event listeners
    difficultyButtons.addEventListener('click', onDifficultySelect);
    cancelBtn.addEventListener('click', onCancel);
    modal.querySelector('.modal-backdrop').addEventListener('click', onCancel);
  }

    // Show a simple message modal
  function showMessage(message, title = 'Notification') {
  // get modal elements
    const modal = document.getElementById('messageModal');
    // safety check
    if (!modal) {
      console.error('Message modal not found in DOM. Falling back to alert.');
      // Show alert as fallback
      alert(`${title}: ${message}`);
      return;
    }
    // set title and message
    const titleEl = document.getElementById('messageModalTitle');
    const textEl = document.getElementById('messageModalText');
    const okBtn = document.getElementById('messageModalOk');

    // set content
    if (titleEl) titleEl.textContent = title;
    if (textEl) textEl.textContent = message;

    // show modal
    modal.setAttribute('aria-hidden', 'false');
    // focus OK button
    if (okBtn) okBtn.focus(); // For accessibility

    // OK button handler to hide modal
    function onOk() {
      modal.setAttribute('aria-hidden', 'true');
      if (okBtn) okBtn.removeEventListener('click', onOk);
      // remove backdrop listener
      const backdrop = modal.querySelector('.modal-backdrop');
      if (backdrop) backdrop.removeEventListener('click', onOk);
    }

    // attach OK button and backdrop listeners
    if (okBtn) okBtn.addEventListener('click', onOk);
    // backdrop click also closes modal
    const backdrop = modal.querySelector('.modal-backdrop');
    if (backdrop) backdrop.addEventListener('click', onOk);
  }
});
