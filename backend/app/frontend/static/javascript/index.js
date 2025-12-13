// Extracted from index.html - helper that updates header to show account if logged in
(function(){
  'use strict';
  try{
    const token = localStorage.getItem('access_token');
    const controls = document.querySelector('.controls');
    if(token && controls){
      // replace sign-in/register with account quick info
      const account = document.createElement('div');
      account.style.display = 'flex'; account.style.gap = '8px'; account.style.alignItems = 'center';

      const btn = document.createElement('a');
      btn.className = 'btn'; btn.href = '/frontend/static/game.html'; btn.textContent = 'Resume Game';

      const out = document.createElement('button');
      out.className = 'btn secondary'; out.textContent = 'Sign out';
      out.addEventListener('click', ()=>{ localStorage.removeItem('access_token'); location.reload(); });

      account.appendChild(btn); account.appendChild(out);

      // re-render controls: keep toggleTheme and add account UI
      const toggle = document.getElementById('toggleTheme');
      controls.innerHTML = '';
      if(toggle) controls.appendChild(toggle);
      controls.appendChild(account);
    }
  } catch(e){
    // fail silently in UI helper
    console.error('index helper error', e);
  }
})();

