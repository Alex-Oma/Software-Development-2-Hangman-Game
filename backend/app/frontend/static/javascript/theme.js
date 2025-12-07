// theme.js - shared theme handling for light/dark mode across pages
(function(){
  const ROOT_ID = 'app';
  const TOGGLE_ID = 'toggleTheme';
  const STORAGE_KEY = 'theme';

  function getAppEl(){
    return document.getElementById(ROOT_ID);
  }

  function getToggleEl(){
    return document.getElementById(TOGGLE_ID);
  }

  function getThemeRoot(){
    return document.documentElement; // <html>
  }

  function applyThemeClass(theme){
    const root = getThemeRoot();
    if(!root) return;
    if(theme === 'dark'){
      root.classList.remove('theme-light');
      root.classList.add('theme-dark');
    } else if(theme === 'light'){
      root.classList.remove('theme-dark');
      root.classList.add('theme-light');
    }

    // Also update the #app element classes to avoid conflicts when pages
    // pre-set theme classes on the app container.
    const app = getAppEl();
    if(app){
      app.classList.remove('theme-light','theme-dark');
      app.classList.add(theme === 'dark' ? 'theme-dark' : 'theme-light');
    }

    // update aria-pressed on toggle if present
    const toggle = getToggleEl();
    if(toggle){
      const pressed = theme === 'dark';
      toggle.setAttribute('aria-pressed', pressed ? 'true' : 'false');
    }
  }

  function initTheme(){
    const root = getThemeRoot();
    if(!root) return;
    const stored = localStorage.getItem(STORAGE_KEY);
    if(stored === 'dark' || stored === 'light'){
      applyThemeClass(stored);
      return;
    }
    // fallback to system preference
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyThemeClass(prefersDark ? 'dark' : 'light');
  }

  function createToggleContents(button){
    if(!button) return;
    // if already decorated, skip
    if(button.querySelector('.theme-toggle-icon')) return;

    // inline SVGs for sun and moon (kept simple)
    const sunSvg = `<svg class="sun" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.5" fill="none"/><g stroke="currentColor" stroke-width="1.4"><path d="M12 2v2"/><path d="M12 20v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M4.93 19.07l1.41-1.41"/><path d="M17.66 6.34l1.41-1.41"/></g></svg>`;
    const moonSvg = `<svg class="moon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke="currentColor" stroke-width="1.4" fill="none"/></svg>`;

    const wrapper = document.createElement('span');
    wrapper.className = 'toggle-icon-wrapper';
    // create an icon-only button (SVGs are aria-hidden) and rely on the button's aria-label for accessibility
    wrapper.innerHTML = `<span class="theme-toggle-icon">${sunSvg}${moonSvg}</span>`;

    // clear existing content but preserve accessible name if present
    const existingText = button.getAttribute('aria-label') || button.textContent.trim();
    if(!button.getAttribute('aria-label')){
      button.setAttribute('aria-label', existingText || 'Toggle theme');
    }
    // replace content
    button.innerHTML = '';
    button.appendChild(wrapper);
  }

  function toggleTheme(){
    const root = getThemeRoot();
    if(!root) return;
    const isLight = root.classList.contains('theme-light');
    const next = isLight ? 'dark' : 'light';
    applyThemeClass(next);
    localStorage.setItem(STORAGE_KEY, next);
  }

  function handleToggleClick(event){
    const target = event.target.closest ? event.target.closest('#' + TOGGLE_ID) : null;
    if(target){
      // ensure toggle contents exist
      createToggleContents(target);
      toggleTheme();
      target.focus();
    }
  }

  function attachToggleHandler(){
    // Decorate the button if present now
    const btn = getToggleEl();
    if(btn) createToggleContents(btn);

    // Ensure clicks anywhere on the document that hit the toggle are handled
    // This guards against the button being replaced by other scripts.
    document.addEventListener('click', handleToggleClick);

    // Keyboard activation: delegate to keydown on document and check target
    document.addEventListener('keydown', function(e){
      const active = document.activeElement;
      if(!active) return;
      if(active.id === TOGGLE_ID && (e.key === 'Enter' || e.key === ' ')){
        e.preventDefault();
        // ensure contents and toggle
        createToggleContents(active);
        toggleTheme();
      }
    });

    // set initial aria-pressed if button exists
    const currentBtn = getToggleEl();
    if(currentBtn){
      const root = getThemeRoot();
      const pressed = root && root.classList.contains('theme-dark');
      currentBtn.setAttribute('aria-pressed', pressed ? 'true' : 'false');
      currentBtn.setAttribute('role','button');
      if(!currentBtn.hasAttribute('tabindex')) currentBtn.setAttribute('tabindex','0');
    }
  }

  // expose minimal API for pages that want to call programmatically
  window.hangmanTheme = {
    initTheme,
    toggleTheme,
    applyThemeClass,
  };

  // auto-init when script loads
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', ()=>{ initTheme(); attachToggleHandler(); });
  } else {
    initTheme(); attachToggleHandler();
  }
})();
