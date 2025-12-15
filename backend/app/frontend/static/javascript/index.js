// Extracted from index.html - helper that updates header to show account if logged in
(function(){
  'use strict';
  try{
  // check for token in localStorage
    const token = localStorage.getItem('access_token');
    const controls = document.querySelector('.controls');
    // if token exists and controls container found
    if(token && controls){
      // replace sign-in/register with account quick info
      const account = document.createElement('div');
      account.style.display = 'flex'; account.style.gap = '8px'; account.style.alignItems = 'center';

        // resume game button
      const btn = document.createElement('a');
      btn.className = 'btn'; btn.href = '/frontend/static/game.html'; btn.textContent = 'Resume Game';

        // sign out button
      const out = document.createElement('button');
      out.className = 'btn secondary'; out.textContent = 'Sign out';
      out.addEventListener('click', ()=>{ localStorage.removeItem('access_token'); location.reload(); });

        // append to account container
      account.appendChild(btn); account.appendChild(out);

      // re-render controls: keep toggleTheme and add account UI
      const toggle = document.getElementById('toggleTheme');
      controls.innerHTML = '';
      // append toggle if exists
      if(toggle) controls.appendChild(toggle);
      // append account info
      controls.appendChild(account);
    }
  } catch(e){
    // fail silently in UI helper
    console.error('index helper error', e);
  }
})();

